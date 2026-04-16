"""BLE device manager for DG-Lab Coyote (V2 and V3)."""

import asyncio
import logging
from dataclasses import dataclass, field

from bleak import BleakClient, BleakScanner

from .protocol import (
    BATTERY_UUID,
    DEVICE_NAME_PREFIX,
    NOTIFY_UUID,
    STRENGTH_ABSOLUTE,
    STRENGTH_DECREASE,
    STRENGTH_INCREASE,
    STRENGTH_MAX,
    STRENGTH_MIN,
    STRENGTH_NONE,
    WAVE_FREQ_ZERO,
    WAVE_INACTIVE,
    WRITE_UUID,
    V2_BATTERY_UUID,
    V2_DEVICE_NAME,
    V2_PWM_A34_UUID,
    V2_PWM_AB2_UUID,
    V2_PWM_B34_UUID,
    build_b0,
    build_bf,
    build_v2_pwm_ab2,
    build_v2_pwm_wave,
    encode_frequency,
    parse_b1,
    parse_v2_pwm_ab2,
    v2_strength_from_user,
    v2_strength_to_user,
)
from .waves import WaveFrame

logger = logging.getLogger(__name__)


@dataclass
class DeviceState:
    """Current device state."""
    connected: bool = False
    address: str = ""
    name: str = ""
    version: str = "v3"   # "v2" or "v3"
    strength_a: int = 0
    strength_b: int = 0
    limit_a: int = 200
    limit_b: int = 200
    battery: int = -1

    # Pending strength changes (accumulated between write loop ticks)
    _pending_strength_a: int = 0
    _pending_strength_b: int = 0
    _absolute_a: int | None = None
    _absolute_b: int | None = None

    # Wave playback state per channel
    wave_a: list[WaveFrame] = field(default_factory=list)
    wave_b: list[WaveFrame] = field(default_factory=list)
    wave_a_index: int = 0
    wave_b_index: int = 0
    wave_a_loop: bool = True
    wave_b_loop: bool = True

    # V3 sequence tracking
    _seq: int = 0
    _awaiting_seq: int | None = None


class CoyoteDevice:
    """Manages BLE connection and communication with Coyote V2 and V3."""

    def __init__(self) -> None:
        self.state = DeviceState()
        self._client: BleakClient | None = None
        self._loop_task: asyncio.Task | None = None
        self._stop_event = asyncio.Event()

    async def scan(self, timeout: float = 5.0) -> list[dict]:
        """Scan for nearby Coyote devices (V2 and V3).

        Returns list of {name, address, version} dicts.
        """
        devices = await BleakScanner.discover(timeout=timeout)
        results = []
        for d in devices:
            name = d.name or ""
            if name.startswith(DEVICE_NAME_PREFIX):
                results.append({"name": name, "address": d.address, "version": "v3"})
            elif name == V2_DEVICE_NAME:
                results.append({"name": name, "address": d.address, "version": "v2"})
        return results

    async def connect(self, address: str, version: str = "v3") -> None:
        """Connect to a Coyote device by address.

        Args:
            address: BLE device address from scan results.
            version: Device protocol version — "v2" or "v3" (default "v3").
        """
        if version not in ("v2", "v3"):
            raise ValueError(f"Unknown version '{version}'. Must be 'v2' or 'v3'.")
        if self.state.connected:
            raise RuntimeError("Already connected. Disconnect first.")

        self._client = BleakClient(address)
        await self._client.connect()

        if not self._client.is_connected:
            raise RuntimeError(f"Failed to connect to {address}")

        self.state.connected = True
        self.state.address = address
        self.state.version = version

        # Read battery level
        battery_uuid = BATTERY_UUID if version == "v3" else V2_BATTERY_UUID
        try:
            battery_data = await self._client.read_gatt_char(battery_uuid)
            if battery_data:
                self.state.battery = battery_data[0]
        except Exception:
            logger.debug("Could not read battery level")

        self._stop_event.clear()

        if version == "v3":
            await self._client.start_notify(NOTIFY_UUID, self._on_notify)
            await self._write_bf()
            self._loop_task = asyncio.create_task(self._b0_loop())
        else:  # v2
            await self._client.start_notify(V2_PWM_AB2_UUID, self._on_notify_v2)
            self._loop_task = asyncio.create_task(self._v2_loop())

        logger.info("Connected to %s (%s)", address, version)

    async def disconnect(self) -> None:
        """Disconnect from the device."""
        if self._loop_task:
            self._stop_event.set()
            self._loop_task.cancel()
            try:
                await self._loop_task
            except asyncio.CancelledError:
                pass
            self._loop_task = None

        if self._client and self._client.is_connected:
            await self._client.disconnect()

        self.state = DeviceState()
        self._client = None
        logger.info("Disconnected")

    # --- Strength control ---

    def set_strength(self, channel: str, value: int) -> None:
        """Set absolute strength for a channel (0~200)."""
        value = max(STRENGTH_MIN, min(STRENGTH_MAX, value))
        if channel.upper() == "A":
            self.state._absolute_a = value
        elif channel.upper() == "B":
            self.state._absolute_b = value
        else:
            raise ValueError(f"Invalid channel: {channel}")

    def add_strength(self, channel: str, delta: int) -> None:
        """Add/subtract strength for a channel."""
        if channel.upper() == "A":
            self.state._absolute_a = None  # cancel any pending absolute
            self.state._pending_strength_a += delta
        elif channel.upper() == "B":
            self.state._absolute_b = None
            self.state._pending_strength_b += delta
        else:
            raise ValueError(f"Invalid channel: {channel}")

    async def set_strength_limit(self, limit_a: int, limit_b: int) -> None:
        """Set strength soft limits.

        V3: persisted on device via BF command.
        V2: software-enforced cap applied in the write loop.
        """
        self.state.limit_a = max(0, min(200, limit_a))
        self.state.limit_b = max(0, min(200, limit_b))
        if self.state.version == "v3":
            await self._write_bf()

    # --- Wave control ---

    def send_wave(
        self,
        channel: str,
        frames: list[WaveFrame],
        loop: bool = True,
    ) -> None:
        """Start playing waveform frames on a channel."""
        if channel.upper() == "A":
            self.state.wave_a = frames
            self.state.wave_a_index = 0
            self.state.wave_a_loop = loop
        elif channel.upper() == "B":
            self.state.wave_b = frames
            self.state.wave_b_index = 0
            self.state.wave_b_loop = loop
        else:
            raise ValueError(f"Invalid channel: {channel}")

    def stop_wave(self, channel: str | None = None) -> None:
        """Stop waveform on a channel (or both if None)."""
        if channel is None or channel.upper() == "A":
            self.state.wave_a = []
            self.state.wave_a_index = 0
        if channel is None or channel.upper() == "B":
            self.state.wave_b = []
            self.state.wave_b_index = 0

    # --- V3 internal ---

    def _on_notify(self, _sender: int, data: bytearray) -> None:
        """Handle B1 notifications from a V3 device."""
        result = parse_b1(bytes(data))
        if result:
            self.state.strength_a = result["strength_a"]
            self.state.strength_b = result["strength_b"]
            if (
                self.state._awaiting_seq is not None
                and result["seq"] == self.state._awaiting_seq
            ):
                self.state._awaiting_seq = None
            logger.debug(
                "B1: seq=%d A=%d B=%d",
                result["seq"],
                result["strength_a"],
                result["strength_b"],
            )

    async def _write_bf(self) -> None:
        """Write BF instruction to set limits and balance params (V3 only)."""
        if not self._client or not self._client.is_connected:
            return
        data = build_bf(self.state.limit_a, self.state.limit_b)
        await self._client.write_gatt_char(WRITE_UUID, data)
        logger.debug("BF written: limit_a=%d limit_b=%d", self.state.limit_a, self.state.limit_b)

    def _build_next_b0(self) -> bytes:
        """Build the next B0 instruction from current state (V3)."""
        seq = 0
        strength_mode = 0
        sa = 0
        sb = 0

        # Handle strength changes (only if not awaiting response)
        if self.state._awaiting_seq is None:
            # A channel
            if self.state._absolute_a is not None:
                mode_a = STRENGTH_ABSOLUTE
                sa = self.state._absolute_a
                self.state._absolute_a = None
                self.state._seq = (self.state._seq % 15) + 1
                seq = self.state._seq
            elif self.state._pending_strength_a != 0:
                delta = self.state._pending_strength_a
                if delta > 0:
                    mode_a = STRENGTH_INCREASE
                    sa = delta
                else:
                    mode_a = STRENGTH_DECREASE
                    sa = -delta
                self.state._pending_strength_a = 0
                self.state._seq = (self.state._seq % 15) + 1
                seq = self.state._seq
            else:
                mode_a = STRENGTH_NONE

            # B channel
            if self.state._absolute_b is not None:
                mode_b = STRENGTH_ABSOLUTE
                sb = self.state._absolute_b
                self.state._absolute_b = None
                if seq == 0:
                    self.state._seq = (self.state._seq % 15) + 1
                    seq = self.state._seq
            elif self.state._pending_strength_b != 0:
                delta = self.state._pending_strength_b
                if delta > 0:
                    mode_b = STRENGTH_INCREASE
                    sb = delta
                else:
                    mode_b = STRENGTH_DECREASE
                    sb = -delta
                self.state._pending_strength_b = 0
                if seq == 0:
                    self.state._seq = (self.state._seq % 15) + 1
                    seq = self.state._seq
            else:
                mode_b = STRENGTH_NONE

            strength_mode = (mode_a << 2) | mode_b

            if seq > 0:
                self.state._awaiting_seq = seq
        else:
            mode_a = STRENGTH_NONE
            mode_b = STRENGTH_NONE

        # Wave data for A channel — encode raw period_ms to V3 format at write time
        if self.state.wave_a:
            idx = self.state.wave_a_index
            frame = self.state.wave_a[idx]
            wave_freq_a = tuple(encode_frequency(f) for f in frame.freq)
            wave_int_a = frame.intensity
            next_idx = idx + 1
            if next_idx >= len(self.state.wave_a):
                if self.state.wave_a_loop:
                    next_idx = 0
                else:
                    self.state.wave_a = []
                    next_idx = 0
            self.state.wave_a_index = next_idx
        else:
            wave_freq_a = WAVE_FREQ_ZERO
            wave_int_a = WAVE_INACTIVE

        # Wave data for B channel
        if self.state.wave_b:
            idx = self.state.wave_b_index
            frame = self.state.wave_b[idx]
            wave_freq_b = tuple(encode_frequency(f) for f in frame.freq)
            wave_int_b = frame.intensity
            next_idx = idx + 1
            if next_idx >= len(self.state.wave_b):
                if self.state.wave_b_loop:
                    next_idx = 0
                else:
                    self.state.wave_b = []
                    next_idx = 0
            self.state.wave_b_index = next_idx
        else:
            wave_freq_b = WAVE_FREQ_ZERO
            wave_int_b = WAVE_INACTIVE

        return build_b0(
            seq=seq,
            strength_mode=strength_mode,
            strength_a=sa,
            strength_b=sb,
            wave_freq_a=wave_freq_a,
            wave_int_a=wave_int_a,
            wave_freq_b=wave_freq_b,
            wave_int_b=wave_int_b,
        )

    async def _b0_loop(self) -> None:
        """100ms periodic loop to send B0 instructions (V3)."""
        while not self._stop_event.is_set():
            try:
                if self._client and self._client.is_connected:
                    data = self._build_next_b0()
                    await self._client.write_gatt_char(WRITE_UUID, data)
                else:
                    break
            except Exception as e:
                logger.error("B0 loop error: %s", e)
                break
            await asyncio.sleep(0.1)

        if self.state.connected:
            self.state.connected = False
            logger.warning("Connection lost in B0 loop")

    # --- V2 internal ---

    def _on_notify_v2(self, _sender: int, data: bytearray) -> None:
        """Handle PWM_AB2 notifications from a V2 device."""
        result = parse_v2_pwm_ab2(bytes(data))
        if result:
            self.state.strength_a = v2_strength_to_user(result["strength_a"])
            self.state.strength_b = v2_strength_to_user(result["strength_b"])
            logger.debug(
                "V2 AB2 notify: A=%d B=%d (raw)",
                result["strength_a"],
                result["strength_b"],
            )

    def _resolve_v2_strength(self, channel: str) -> int:
        """Compute effective user-facing strength for a V2 channel, consuming pending changes."""
        if channel == "A":
            limit = self.state.limit_a
            if self.state._absolute_a is not None:
                target = self.state._absolute_a
                self.state._absolute_a = None
            else:
                target = self.state.strength_a + self.state._pending_strength_a
                self.state._pending_strength_a = 0
        else:
            limit = self.state.limit_b
            if self.state._absolute_b is not None:
                target = self.state._absolute_b
                self.state._absolute_b = None
            else:
                target = self.state.strength_b + self.state._pending_strength_b
                self.state._pending_strength_b = 0
        return max(STRENGTH_MIN, min(limit, target))

    def _get_v2_wave_bytes(self, channel: str) -> bytes:
        """Get the 3-byte V2 waveform packet for the current frame of a channel."""
        if channel == "A":
            wave = self.state.wave_a
            idx_attr, loop_attr = "wave_a_index", "wave_a_loop"
        else:
            wave = self.state.wave_b
            idx_attr, loop_attr = "wave_b_index", "wave_b_loop"

        if not wave:
            return build_v2_pwm_wave(10, 0)  # zero-intensity: no stimulation

        idx = getattr(self.state, idx_attr)
        frame = wave[idx]
        # WaveFrame.freq stores raw period_ms; intensity stores 0-100 pct
        period_ms = frame.freq[0]
        intensity_pct = frame.intensity[0]

        next_idx = idx + 1
        if next_idx >= len(wave):
            if getattr(self.state, loop_attr):
                next_idx = 0
            else:
                if channel == "A":
                    self.state.wave_a = []
                else:
                    self.state.wave_b = []
                next_idx = 0
        setattr(self.state, idx_attr, next_idx)

        return build_v2_pwm_wave(period_ms, intensity_pct)

    async def _v2_write_once(self) -> None:
        """Write one tick of V2 control data (strength + waveforms)."""
        sa_user = self._resolve_v2_strength("A")
        sb_user = self._resolve_v2_strength("B")

        ab2 = build_v2_pwm_ab2(
            v2_strength_from_user(sa_user),
            v2_strength_from_user(sb_user),
        )
        await self._client.write_gatt_char(V2_PWM_AB2_UUID, ab2)

        # PWM_B34 carries channel A waveform; PWM_A34 carries channel B waveform
        await self._client.write_gatt_char(V2_PWM_B34_UUID, self._get_v2_wave_bytes("A"))
        await self._client.write_gatt_char(V2_PWM_A34_UUID, self._get_v2_wave_bytes("B"))

    async def _v2_loop(self) -> None:
        """100ms periodic loop to send V2 control packets."""
        while not self._stop_event.is_set():
            try:
                if self._client and self._client.is_connected:
                    await self._v2_write_once()
                else:
                    break
            except Exception as e:
                logger.error("V2 loop error: %s", e)
                break
            await asyncio.sleep(0.1)

        if self.state.connected:
            self.state.connected = False
            logger.warning("Connection lost in V2 loop")

    # --- Status ---

    def get_status(self) -> dict:
        """Get current device status."""
        return {
            "connected": self.state.connected,
            "version": self.state.version,
            "address": self.state.address,
            "strength_a": self.state.strength_a,
            "strength_b": self.state.strength_b,
            "limit_a": self.state.limit_a,
            "limit_b": self.state.limit_b,
            "battery": self.state.battery,
            "wave_a_active": len(self.state.wave_a) > 0,
            "wave_b_active": len(self.state.wave_b) > 0,
        }
