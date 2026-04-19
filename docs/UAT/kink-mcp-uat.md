# kink-mcp UAT Test Plan

## Context

This UAT validates all user-facing functionality of kink-mcp: MCP tools, MCP resources, the web UI, alias system, wave library, pain limit system, persistence, and auto-reconnect. Tests require physical device interaction — the human user confirms device behavior in response to AI commands.

**Test agent role:** Execute MCP tool calls, read MCP resources, and operate the web UI via the chrome plugin MCP.  
**Human role:** Confirm audible/physical device responses, operate the web UI where required for setup, and provide feedback.

**Hardware:**
- 2× Lovense toys (referenced as Lovense-1, Lovense-2)
- 2× DG-Lab Coyote V2 (referenced as Coyote-1, Coyote-2)

**Key test constraints:**
- Coyote: use **100% strength only** so the device makes an audible click/buzz for verification
- Test **one Coyote channel at a time** (unless explicitly testing sync)
- Alias sync across devices: assign same alias on two **different** Coyote devices
- Test agent uses chrome plugin to interact with the web UI autonomously where noted
- `design_wave()` plays immediately on an alias — it does **not** save to the wave library

**Test grouping by device connection:**
- **Phase 0–2**: No devices connected
- **Phase 3–13**: One Coyote (Coyote-1) + One Lovense (Lovense-1)
- **Phase 14–16**: All four devices (Coyote-1, Coyote-2, Lovense-1, Lovense-2)

---

> **Note to test agent — Skipped tests:**  
> If a test's preconditions are not met (required device unavailable, prior test left system in unrecoverable state, or feature prerequisite not set up), **skip the test and mark it SKIP** in the tracking table. Record the reason in the Bug Report Log as `SKIP-<ID>: <reason>`. Continue with the next test. Do not attempt to work around unmet preconditions.

---

## Critical Bug Protocol

If the MCP server becomes **unresponsive**, **stuck in a loop**, **crashes**, or is otherwise **unusable**, the test is immediately aborted:

1. Mark the triggering test as `FAIL` and file a `BUG-<ID>` with Severity: **Critical**
2. Stop all further testing — do not attempt to continue
3. Report the critical bug to the human; a dedicated bug-fix session with a specialized agent will follow
4. **After bug fix:** Re-run **only** the test that triggered the critical bug to confirm it is resolved, then resume the normal test sequence from that point forward

---

## Bug Report Template

Each failed test gets a bug report entry appended to the **Bug Report Log** at the bottom of this document:

```
BUG-<ID>: <Short title>
Test: <test ID that triggered it>
Conditions: <exact inputs, state, steps that triggered the bug>
Expected: <what should have happened>
Actual: <what actually happened>
Severity: Low / Medium / High / Critical
```

---

## Test Status Tracking

Update this table as each test is executed. Status values: `PASS` / `FAIL` / `SKIP` / `PENDING`

| ID   | Phase / Group                          | Description                                   | Status  | Notes |
|------|----------------------------------------|-----------------------------------------------|---------|-------|
| T-00 | Phase 0 — No Devices                  | Read ui://url, open Web UI                    | PENDING |       |
| T-01 | Phase 0 — No Devices                  | waves://library resource                      | PENDING |       |
| T-02 | Phase 0 — No Devices                  | waves://guide resource                        | PENDING |       |
| T-03 | Phase 1 — No Devices                  | devices://status (no devices)                 | PENDING |       |
| T-04 | Phase 1 — No Devices                  | get_status (no devices)                       | PENDING |       |
| T-05 | Phase 2 — Web UI Setup                | Scan for devices                              | PENDING |       |
| T-06 | Phase 2 — Web UI Setup                | Connect Coyote-1 (two channels)               | PENDING |       |
| T-07 | Phase 2 — Web UI Setup                | Connect Lovense-1                             | PENDING |       |
| T-08 | Phase 2 — Web UI Setup                | Alias rename via UI                           | PENDING |       |
| T-09 | Phase 2 — Web UI Setup                | Pain limit slider (right_thigh only)          | PENDING |       |
| T-10 | Phase 2 — Web UI Setup                | Disconnect device via UI                      | PENDING |       |
| T-11 | Phase 2 — Web UI Setup                | Retry — reconnect offline device              | PENDING |       |
| T-12 | Phase 2 — Web UI Setup                | LLM toggle — expose set_pain_limit            | PENDING |       |
| T-13 | Phase 3 — MCP Resources               | devices://status (with devices)               | PENDING |       |
| T-14 | Phase 4 — get_status                  | With active devices                           | PENDING |       |
| T-15 | Phase 5 — set_strength                | Basic command (100%, no limit channel)        | PENDING |       |
| T-16 | Phase 5 — set_strength                | Strength 0 (off)                              | PENDING |       |
| T-17 | Phase 5 — set_strength                | Invalid value > 100                           | PENDING |       |
| T-18 | Phase 5 — set_strength                | Invalid value < 0                             | PENDING |       |
| T-19 | Phase 5 — set_strength                | Unknown alias                                 | PENDING |       |
| T-20 | Phase 5 — set_strength                | Pain limit enforcement (right_thigh, 50% cap) | PENDING |       |
| T-21 | Phase 5 — set_strength                | No waveform warning                           | PENDING |       |
| T-22 | Phase 6 — adjust_strength             | Positive delta                                | PENDING |       |
| T-23 | Phase 6 — adjust_strength             | Negative delta                                | PENDING |       |
| T-24 | Phase 6 — adjust_strength             | Clamping at 0                                 | PENDING |       |
| T-25 | Phase 6 — adjust_strength             | Clamping at 100                               | PENDING |       |
| T-26 | Phase 7 — play_wave                   | All 6 built-in presets                        | PENDING |       |
| T-27 | Phase 7 — play_wave                   | loop=1 (single cycle)                         | PENDING |       |
| T-28 | Phase 7 — play_wave                   | loop=3 (fixed cycles)                         | PENDING |       |
| T-29 | Phase 7 — play_wave                   | loop=0 (infinite)                             | PENDING |       |
| T-30 | Phase 7 — play_wave                   | With strength parameter                       | PENDING |       |
| T-31 | Phase 7 — play_wave                   | Unknown preset (error case)                   | PENDING |       |
| T-32 | Phase 8 — stop_wave                   | Specific alias                                | PENDING |       |
| T-33 | Phase 8 — stop_wave                   | All channels (no alias)                       | PENDING |       |
| T-34 | Phase 9 — design_wave                 | Basic custom wave                             | PENDING |       |
| T-35 | Phase 9 — design_wave                 | Freq clamping                                 | PENDING |       |
| T-36 | Phase 9 — design_wave                 | Empty steps (error case)                      | PENDING |       |
| T-37 | Phase 10 — vibrate (Lovense)          | Basic on                                      | PENDING |       |
| T-38 | Phase 10 — vibrate (Lovense)          | Full range test                               | PENDING |       |
| T-39 | Phase 10 — vibrate (Lovense)          | Invalid values                                | PENDING |       |
| T-40 | Phase 10 — vibrate (Lovense)          | Unknown alias                                 | PENDING |       |
| T-41 | Phase 10 — vibrate (Lovense)          | Wrong device type (Coyote alias)              | PENDING |       |
| T-42 | Phase 11 — Session Timer              | First activity starts timer                   | PENDING |       |
| T-43 | Phase 11 — Session Timer              | Per-alias activity timestamp                  | PENDING |       |
| T-44 | Phase 12 — Edge Cases                 | Commands on disconnected device               | PENDING |       |
| T-45 | Phase 12 — Edge Cases                 | Rapid sequential commands                     | PENDING |       |
| T-46 | Phase 12 — Edge Cases                 | Replace wave while another is active          | PENDING |       |
| T-47 | Phase 13 — set_pain_limit (MCP tool)  | Set via MCP tool                              | PENDING |       |
| T-48 | Phase 13 — set_pain_limit (MCP tool)  | Boundary values (0 and 100)                   | PENDING |       |
| T-49 | Phase 13 — set_pain_limit (MCP tool)  | Invalid values                                | PENDING |       |
| T-50 | Phase 13 — Persistence                | Config & aliases after restart                | PENDING |       |
| T-51 | Phase 13 — Persistence                | Offline device on restart                     | PENDING |       |
| T-52 | Phase 13 — Persistence                | Manual retry after device power-on            | PENDING |       |
| T-53 | Phase 14 — All Devices: Sync          | Connect Coyote-2 and Lovense-2                | PENDING |       |
| T-54 | Phase 14 — All Devices: Sync          | Same-device channel sync (Coyote-1)           | PENDING |       |
| T-55 | Phase 14 — All Devices: Sync          | Cross-device sync (Coyote-1 + Coyote-2)       | PENDING |       |
| T-56 | Phase 14 — All Devices: Sync          | Independent channels on same device           | PENDING |       |
| T-57 | Phase 14 — All Devices: Sync          | Alias rename during active session            | PENDING |       |
| T-58 | Phase 15 — Two Lovense                | Independent control                           | PENDING |       |
| T-59 | Phase 15 — Two Lovense                | Shared alias sync                             | PENDING |       |
| T-60 | Phase 16 — Mixed Session              | Simultaneous Coyote + Lovense (all 4)         | PENDING |       |
| T-61 | Phase 17 — UX Report                  | Agent self-assessment & recommendations       | PENDING |       |

**Summary:** PASS: 0 | FAIL: 0 | SKIP: 0 | PENDING: 62

---

## Phase 0 — No Devices Connected: Environment & Static Resources

### T-00: Read ui://url Resource and Open Web UI

- [ ] Read the `ui://url` MCP resource
- [ ] Report the URL to the human
- [ ] Use Chrome plugin to load the URL and confirm the page renders

**Expected:** Returns a valid `http://localhost:<port>` URL. Web UI loads without errors.  
**Human:** Confirm the web UI opens in the browser.

**Bug report if:** Resource returns empty/malformed URL, or web UI fails to load.

---

### T-01: waves://library Resource

- [ ] Read `waves://library` resource
- [ ] Verify all 6 built-in presets are listed with descriptions

**Expected:** Lists `breath`, `tide`, `pulse_low`, `pulse_mid`, `pulse_high`, `tap` — one per line with description.  
**Bug report if:** Any preset missing, descriptions wrong, or malformed output.

---

### T-02: waves://guide Resource

- [ ] Read `waves://guide` resource
- [ ] Verify key sections are present

**Expected guide covers:**
- `freq` parameter (10–1000ms, lower = sharper)
- `intensity` parameter (0–100)
- `repeat` parameter (frames, default 1)
- Example patterns and sensation descriptions

**Bug report if:** Content truncated, sections missing, or parameter ranges incorrect.

---

## Phase 1 — No Devices Connected: Status Tools

### T-03: devices://status (No Devices)

- [ ] Read `devices://status` resource
- [ ] Report content

**Expected:** Contains message: "No aliases registered. Ask the user to open the web UI and connect their devices."  
**Bug report if:** Returns malformed output, error, or any device data.

---

### T-04: get_status (No Devices)

- [ ] Call `get_status()`
- [ ] Verify response structure

**Expected:** JSON with `connected_devices: 0`, `aliases: {}`.  
**Bug report if:** Error thrown, malformed JSON, or non-zero counts.

---

## Phase 2 — Web UI: Setup with One Coyote + One Lovense

> These tests establish the baseline connected state for all subsequent phases.

### T-05: Scan for Devices

**Setup:** All devices powered on and in range.

- [ ] Via chrome plugin: navigate to the web UI
- [ ] Click "Scan for Devices"
- [ ] Report discovered devices to human

**Expected:**
- At least Coyote-1 and Lovense-1 appear in scan results
- Each result shows device name, address, and detected type/version

**Bug report if:** Scan returns empty results despite devices being powered on, or devices show incorrect type/version.

---

### T-06: Connect Coyote-1 (Two Channels)

**Precondition:** T-05 passed.

- [ ] From scan results, select Coyote-1
- [ ] Enter alias_a = `left_thigh`, alias_b = `right_thigh`
- [ ] Click Connect
- [ ] Confirm device appears in Connected Devices list

**Expected:**
- Device shows aliases `left_thigh` / `right_thigh`
- Battery percentage shown
- UI shows "connected" within 2 seconds

> **Channel roles for all subsequent tests:**  
> `left_thigh` (Channel A) — **no pain limit** — used for all strength/wave output tests  
> `right_thigh` (Channel B) — pain limit will be set to 50% in T-09 — used only for pain limit enforcement tests

**Bug report if:** Connection fails, wrong aliases shown, battery missing, or UI doesn't update.

---

### T-07: Connect Lovense-1

**Precondition:** T-05 passed.

- [ ] From scan results, select Lovense-1
- [ ] Enter alias_a = `toy_a` (no alias_b for Lovense)
- [ ] Click Connect
- [ ] Confirm device appears in list as Lovense type

**Expected:**
- Device shows alias `toy_a`
- Device type displayed as Lovense

**Bug report if:** Connection fails or device type mislabeled.

---

### T-08: Alias Rename via UI

**Precondition:** T-06 passed (alias `left_thigh` exists).

- [ ] Click the `left_thigh` alias badge in the UI
- [ ] Enter new name `left_leg`
- [ ] Confirm rename
- [ ] Verify badge updates within 2 seconds
- [ ] Rename back to `left_thigh` for use in subsequent tests

**Expected:**
- Badge updates to `left_leg`
- No disconnection or error
- Rename back to `left_thigh` also works

**Human:** Confirm no error message appears during either rename.  
**Bug report if:** Rename fails, old alias persists, or device disconnects.

---

### T-09: Pain Limit Slider via UI

**Precondition:** T-06 passed.

- [ ] Open the Pain Limit panel in the UI
- [ ] Set slider for **`right_thigh`** to **50%** (channel B — pain limit test channel)
- [ ] Leave `left_thigh` at 100% (no limit)
- [ ] Wait for next poll and verify values persist

**Expected:**
- `right_thigh` slider shows 50%, `left_thigh` remains at 100%
- Values persist across UI polls

> **Note:** `right_thigh` (50% limit) is used exclusively for pain limit enforcement tests (T-20, T-47–T-48). All other strength/wave tests use `left_thigh` (no limit) to ensure full 100% output.

**Bug report if:** Values reset, wrong channel updated, or limit doesn't persist.

---

### T-10: Disconnect Device via UI

**Precondition:** T-06 passed.

- [ ] Via chrome plugin: click Disconnect on Coyote-1
- [ ] Verify Coyote-1 disappears from connected list or shows offline

**Human:** Confirm no audible output from Coyote-1 after disconnect.  
**Bug report if:** UI doesn't update, device still listed as connected, or error shown.

---

### T-11: Retry — Reconnect Offline Device

**Precondition:** T-10 passed. Coyote-1 still powered on.

- [ ] Find Coyote-1 in offline/retry section
- [ ] Click Retry
- [ ] Confirm device reconnects with aliases `left_thigh` / `right_thigh`
- [ ] Verify `right_thigh` pain limit is still 50%

**Expected:**
- Device reconnects within a few seconds
- Aliases preserved
- Pain limit 50% on `right_thigh` re-applied

**Bug report if:** Retry fails, aliases lost, or pain limit reset to 100%.

---

### T-12: LLM Toggle — Expose set_pain_limit

- [ ] Find the "Expose set_pain_limit to LLM" toggle in the UI
- [ ] Toggle it ON
- [ ] Confirm a restart-required warning appears in the UI
- [ ] Ask human to restart the kink-mcp server
- [ ] After restart: verify `set_pain_limit` appears in the agent's available tool list

**Expected:**
- Toggle turns ON visually
- Clear warning message prompts restart
- Tool available post-restart

**Human:** Restart kink-mcp. Confirm agent reports `set_pain_limit` in available tools.  
**Bug report if:** Toggle has no visual state, warning missing, or tool absent post-restart.

---

## Phase 3 — MCP Resources with Active Devices

### T-13: devices://status (With Active Devices)

**Setup:** Coyote-1 (`left_thigh`, `right_thigh`) and Lovense-1 (`toy_a`) connected. No commands issued since last connect.

- [ ] Read `devices://status` resource
- [ ] Verify all required fields present

**Expected snapshot includes:**
- Device types: coyote, lovense
- Aliases: `left_thigh`, `right_thigh`, `toy_a` with connection state
- Strength, limit, wave status per channel
- Battery percentages
- Applicable tools per alias
- session.running_since = "not started"
- `right_thigh` shows limit = 50%

**Bug report if:** Missing fields, wrong device type, incorrect battery, wrong limit, or broken formatting.

---

## Phase 4 — get_status with Active Devices

### T-14: get_status with Active Devices

**Setup:** Coyote-1 and Lovense-1 connected, no commands since connect.

- [ ] Call `get_status()`
- [ ] Verify all fields present

**Expected JSON includes:**
- `connected_devices` ≥ 2
- Alias `left_thigh`: strength_pct=0, limit_pct=100, wave_active=false, battery, connected=true
- Alias `right_thigh`: limit_pct=50
- Alias `toy_a`: connected=true
- session.running_since = "not started"

**Bug report if:** Missing aliases, wrong limit values, or session timer in wrong state.

---

## Phase 5 — Coyote: set_strength

> All Coyote strength output tests use **`left_thigh`** (no pain limit). `right_thigh` (50% limit) is only used in T-20.  
> A wave must be active on V2 for output — `play_wave` is called in setup steps where needed.

### T-15: set_strength — Basic Command (100%)

**Setup:** `play_wave("left_thigh", "pulse_high")` first.

- [ ] Call `set_strength("left_thigh", 100)`
- [ ] Human confirms audible output from Coyote-1 channel A

**Expected:** Success message. Coyote-1 channel A emits audible buzz.  
**Bug report if:** No audible output, error returned, or wrong channel fires.

---

### T-16: set_strength — Strength 0 (Off)

**Precondition:** T-15 passed (wave active, strength=100%).

- [ ] Call `set_strength("left_thigh", 0)`
- [ ] Human confirms device goes silent

**Expected:** Device becomes silent immediately.  
**Bug report if:** Device continues output.

---

### T-17: set_strength — Invalid Value (>100)

- [ ] Call `set_strength("left_thigh", 101)`
- [ ] Verify error returned

**Expected:** Error message returned. No device output change.  
**Bug report if:** No error, or device fires.

---

### T-18: set_strength — Invalid Value (<0)

- [ ] Call `set_strength("left_thigh", -1)`
- [ ] Verify error returned

**Expected:** Error message returned.  
**Bug report if:** No error returned.

---

### T-19: set_strength — Unknown Alias

- [ ] Call `set_strength("nonexistent_alias", 100)`
- [ ] Verify error returned

**Expected:** Error: alias not found.  
**Bug report if:** Silent failure or crash.

---

### T-20: set_strength — Pain Limit Enforcement

**Setup:** `play_wave("right_thigh", "pulse_high")` on the **50%-limited** channel.

- [ ] Call `set_strength("right_thigh", 100)`
- [ ] Verify response mentions capped effective strength (50%)
- [ ] Human compares output to T-15 (should be noticeably quieter)

**Expected:** Response states effective strength = 50%. Output clearly lower than full 100% on `left_thigh`.  
**Human:** Confirm audible output is clearly lower than T-15.  
**Bug report if:** Device outputs at full 100% (limit not enforced), or no cap mentioned.

---

### T-21: set_strength — No Waveform Warning

**Setup:** `stop_wave("left_thigh")` to ensure no wave active.

- [ ] Call `set_strength("left_thigh", 100)`
- [ ] Verify response includes a warning about no active waveform
- [ ] Human confirms device is silent

**Expected:** Success with warning. V2 produces no output without a wave.  
**Bug report if:** No warning in response, or device fires unexpectedly.

---

## Phase 6 — Coyote: adjust_strength

> All tests use `left_thigh` (no pain limit).

### T-22: adjust_strength — Positive Delta

**Setup:** `set_strength("left_thigh", 0)`, then `play_wave("left_thigh", "pulse_high")`.

- [ ] Call `adjust_strength("left_thigh", 100)`
- [ ] Human confirms audible output starts

**Expected:** Strength moves to 100%. Device emits audible output.  
**Bug report if:** No output, or strength doesn't increase.

---

### T-23: adjust_strength — Negative Delta

**Precondition:** T-22 passed (strength at 100%).

- [ ] Call `adjust_strength("left_thigh", -100)`
- [ ] Human confirms device goes silent

**Expected:** Strength moves to 0%. Device goes silent.  
**Bug report if:** Strength doesn't decrease.

---

### T-24: adjust_strength — Clamping at 0

**Setup:** `set_strength("left_thigh", 0)`.

- [ ] Call `adjust_strength("left_thigh", -50)`
- [ ] Verify no error, strength remains 0 in `get_status()`

**Expected:** Strength stays at 0 (clamped). No error.  
**Bug report if:** Error thrown or negative value stored.

---

### T-25: adjust_strength — Clamping at 100

**Setup:** `set_strength("left_thigh", 100)` + wave active.

- [ ] Call `adjust_strength("left_thigh", 50)`
- [ ] Verify no error, strength stays at 100 in `get_status()`
- [ ] Human confirms same audible volume

**Expected:** Strength stays at 100% (clamped). No error.  
**Bug report if:** Error thrown or strength exceeds 100%.

---

## Phase 7 — Coyote: play_wave

> All tests use `left_thigh` (no pain limit). Set `set_strength("left_thigh", 100)` before each where needed.

### T-26: play_wave — All 6 Built-in Presets

- [ ] `play_wave("left_thigh", "pulse_high")` + strength 100% — human feedback
- [ ] `play_wave("left_thigh", "breath")` — human feedback
- [ ] `play_wave("left_thigh", "tide")` — human feedback
- [ ] `play_wave("left_thigh", "pulse_low")` — human feedback
- [ ] `play_wave("left_thigh", "pulse_mid")` — human feedback
- [ ] `play_wave("left_thigh", "tap")` — human feedback

Wait ~3 seconds between each and ask human to describe the pattern.

**Expected:** Each wave plays with a distinct audible pattern. All 6 return success.  
**Human:** Confirm each produces distinct output. Note what you hear/feel for each.  
**Bug report if:** Any preset silent, returns error, or two presets sound identical.

---

### T-27: play_wave — loop=1 (Single Cycle)

**Setup:** `set_strength("left_thigh", 100)`.

- [ ] Call `play_wave("left_thigh", "tap", loop=1)`
- [ ] Wait 5 seconds
- [ ] Call `get_status()` — check `wave_active` for `left_thigh`

**Expected:** "tap" plays once (~600ms) then stops. `wave_active: false`.  
**Human:** Confirm tap pattern plays once then goes silent.  
**Bug report if:** Wave loops continuously, never stops, or wrong cycle count.

---

### T-28: play_wave — loop=3 (Fixed Cycles)

**Setup:** `set_strength("left_thigh", 100)`.

- [ ] Call `play_wave("left_thigh", "tap", loop=3)`
- [ ] Human counts audible cycles
- [ ] After ~5 seconds: `get_status()` — verify `wave_active: false`

**Expected:** "tap" plays exactly 3 times then stops automatically.  
**Human:** Count tap cycles — confirm exactly 3.  
**Bug report if:** Wrong number of cycles or wave doesn't stop.

---

### T-29: play_wave — loop=0 (Infinite)

**Setup:** `set_strength("left_thigh", 100)`.

- [ ] Call `play_wave("left_thigh", "pulse_mid", loop=0)`
- [ ] Wait 5 seconds — call `get_status()`, verify `wave_active: true`
- [ ] Call `stop_wave("left_thigh")`
- [ ] Verify device goes silent, `wave_active: false`

**Expected:** Wave runs until explicitly stopped.  
**Human:** Confirm continuous buzz until stop_wave issued.  
**Bug report if:** Wave stops on its own, or stop_wave doesn't silence it.

---

### T-30: play_wave — With Strength Parameter

**Setup:** `set_strength("left_thigh", 0)` to silence channel.

- [ ] Call `play_wave("left_thigh", "pulse_high", strength=100)`
- [ ] Human confirms device starts audibly immediately

**Expected:** Wave starts AND strength set to 100% in one call — no separate set_strength needed.  
**Bug report if:** Wave plays silently (strength parameter not applied).

---

### T-31: play_wave — Unknown Preset

- [ ] Call `play_wave("left_thigh", "nonexistent_wave")`
- [ ] Verify error returned, no device output

**Expected:** Error: preset not found.  
**Bug report if:** No error, or device fires.

---

## Phase 8 — Coyote: stop_wave

### T-32: stop_wave — Specific Alias

**Setup:** `play_wave("left_thigh", "pulse_high")` + `set_strength("left_thigh", 100)`.

- [ ] Call `stop_wave("left_thigh")`
- [ ] Human confirms device goes silent
- [ ] `get_status()` — verify `wave_active: false` for `left_thigh`

**Expected:** Output stops immediately. `right_thigh` unaffected (if active).  
**Bug report if:** Device continues output after stop_wave.

---

### T-33: stop_wave — All Channels (No Alias)

**Setup:**
1. `play_wave("left_thigh", "pulse_low")` + `set_strength("left_thigh", 100)`
2. `play_wave("right_thigh", "pulse_mid")` + `set_strength("right_thigh", 100)`

- [ ] Call `stop_wave()` with no alias
- [ ] `get_status()` — verify both `left_thigh` and `right_thigh` show `wave_active: false`
- [ ] Human confirms both channels go silent simultaneously

**Expected:** Both channels stop at once.  
**Bug report if:** Only one channel stops, or error thrown without an alias argument.

> After this test: `right_thigh` no longer has an active wave. Its 50% pain limit remains.

---

## Phase 9 — Coyote: design_wave

> `design_wave(alias, steps, loop=0, strength=None)` — plays immediately on the alias, does **not** save to library.  
> All tests use `left_thigh` (no pain limit).

### T-34: design_wave — Basic Custom Wave

- [ ] Read `waves://guide` for parameter reference
- [ ] Call:
  ```
  design_wave(
    "left_thigh",
    steps=[
      {"freq": 10, "intensity": 0},
      {"freq": 10, "intensity": 100, "repeat": 3},
      {"freq": 10, "intensity": 0, "repeat": 2}
    ],
    loop=0,
    strength=100
  )
  ```
- [ ] Human confirms wave plays with ramp-up pattern

**Expected:** Success. Device plays: silence (100ms) → burst × 3 frames → silence × 2 frames, looping.  
**Bug report if:** Error, no output, or pattern doesn't match steps.

---

### T-35: design_wave — Freq Clamping

- [ ] Call:
  ```
  design_wave(
    "left_thigh",
    steps=[{"freq": 5, "intensity": 100}, {"freq": 2000, "intensity": 100}],
    strength=100
  )
  ```
- [ ] Verify no error returned
- [ ] Human confirms device fires

**Expected:** No error (freq=5 clamped to 10, freq=2000 clamped to 1000 internally). Device plays.  
**Bug report if:** Error thrown for out-of-range freq values.

---

### T-36: design_wave — Empty Steps (Error Case)

- [ ] Call `design_wave("left_thigh", steps=[])`
- [ ] Verify error returned, no device output

**Expected:** Error: steps list cannot be empty.  
**Bug report if:** No error, or device fires.

---

## Phase 10 — Lovense: vibrate

### T-37: vibrate — Basic On

**Setup:** Lovense-1 connected as `toy_a`.

- [ ] Call `vibrate("toy_a", 50)`
- [ ] Human confirms toy vibrates

**Expected:** Lovense vibrates at medium intensity.  
**Bug report if:** No vibration, error returned, or wrong device fires.

---

### T-38: vibrate — Full Range Test

- [ ] `vibrate("toy_a", 100)` — human feedback (full intensity)
- [ ] `vibrate("toy_a", 50)` — human feedback (medium)
- [ ] `vibrate("toy_a", 10)` — human feedback (low)
- [ ] `vibrate("toy_a", 0)` — human confirms stop

**Expected:** Distinct perceptible steps. Clean stop at 0.  
**Human:** Confirm each step feels different and 0 stops vibration completely.  
**Bug report if:** Steps feel identical, or 0 doesn't stop.

---

### T-39: vibrate — Invalid Values

- [ ] Call `vibrate("toy_a", 101)` — verify error
- [ ] Call `vibrate("toy_a", -1)` — verify error

**Expected:** Both return error. No vibration change.  
**Bug report if:** No error returned for either.

---

### T-40: vibrate — Unknown Alias

- [ ] Call `vibrate("nonexistent", 50)`
- [ ] Verify error returned

**Expected:** Error: alias not found.  
**Bug report if:** Silent failure.

---

### T-41: vibrate — Wrong Device Type (Coyote Alias)

- [ ] Call `vibrate("left_thigh", 50)` (`left_thigh` is a Coyote channel)
- [ ] Verify error returned

**Expected:** Error: no Lovense device on that alias.  
**Bug report if:** Coyote fires, or success returned silently.

---

## Phase 11 — Session Timer

### T-42: Session Timer — First Activity

**Setup:** Freshly reconnected devices, no commands issued since connect.

- [ ] `get_status()` — verify session.running_since = "not started"
- [ ] `vibrate("toy_a", 50)`
- [ ] `get_status()` — verify session.running_since now shows a relative time (e.g., "5 seconds ago")

**Expected:** Timer starts on first command. Not before.  
**Bug report if:** Timer doesn't start, already started before command, or shows wrong time.

---

### T-43: Per-Alias Activity Timestamp

- [ ] `play_wave("left_thigh", "pulse_mid")` + `set_strength("left_thigh", 100)`
- [ ] Wait ~5 seconds
- [ ] `vibrate("toy_a", 50)`
- [ ] `get_status()` — compare last_activity for `left_thigh` vs `toy_a`

**Expected:** `left_thigh` shows ~5 seconds ago, `toy_a` shows ~0 seconds ago — different per alias.  
**Bug report if:** Both show same time, or timestamps not tracked.

---

## Phase 12 — Edge Cases & Error Handling

### T-44: Commands on Disconnected Device

- [ ] Via chrome plugin: disconnect Coyote-1
- [ ] Call `set_strength("left_thigh", 100)`
- [ ] Verify error returned

**Expected:** Error: alias has no connected devices.  
**Bug report if:** Silent failure or crash.

> Reconnect Coyote-1 via UI before proceeding.

---

### T-45: Rapid Sequential Commands

**Setup:** Coyote-1 reconnected.

- [ ] `play_wave("left_thigh", "pulse_high")`
- [ ] `set_strength("left_thigh", 100)`
- [ ] `adjust_strength("left_thigh", -50)`
- [ ] `stop_wave("left_thigh")`
- [ ] `play_wave("left_thigh", "breath")`
- [ ] `set_strength("left_thigh", 100)`
- [ ] `get_status()` — verify: breath wave active, strength=100%, on `left_thigh`

**Expected:** All commands succeed. Final state: breath wave playing at 100%.  
**Bug report if:** Any command fails, state corrupted, or unexpected output.

---

### T-46: Replace Wave While Another Is Active

**Setup:** `play_wave("left_thigh", "pulse_low")` + `set_strength("left_thigh", 100)`.

- [ ] Immediately call `play_wave("left_thigh", "tap")`
- [ ] Human confirms pattern transitions audibly

**Expected:** "tap" replaces "pulse_low" without error or lockup.  
**Human:** Confirm pattern changes from steady pulse to tap.  
**Bug report if:** Old wave continues, error thrown, or device locks up.

---

## Phase 13 — set_pain_limit (MCP Tool), Persistence & Restart

> **Precondition for T-47–T-49:** LLM toggle ON and server restarted (T-12 passed). If T-12 was skipped, skip this sub-section and mark T-47–T-49 as SKIP.

### T-47: set_pain_limit via MCP Tool

**Setup:** `right_thigh` already has a 50% limit from T-09. Play wave + set strength 100% on `right_thigh` to verify current capped output.

- [ ] Call `set_pain_limit("right_thigh", 30)` (lower the limit further)
- [ ] `set_strength("right_thigh", 100)`
- [ ] `get_status()` — verify limit_pct = 30 for `right_thigh`
- [ ] Human compares output to T-20 (should be lower still)

**Expected:** limit_pct = 30. Output clearly lower than T-20 (50% cap).  
**Bug report if:** Limit not applied, status shows wrong value, or error returned.

---

### T-48: set_pain_limit — Boundary Values (0 and 100)

**Setup:** Wave active on `right_thigh`.

- [ ] `set_pain_limit("right_thigh", 0)` → `set_strength("right_thigh", 100)` → human confirms silence
- [ ] `set_pain_limit("right_thigh", 100)` → `set_strength("right_thigh", 100)` → human confirms full output

**Expected:** limit=0 silences the channel entirely. limit=100 removes all restriction.  
**Human:** Confirm silence at 0, full audible output at 100.  
**Bug report if:** Device fires at limit=0, or limit=100 still restricts output.

> After this test: `right_thigh` has limit=100 (restored).

---

### T-49: set_pain_limit — Invalid Values

- [ ] Call `set_pain_limit("right_thigh", -1)` — verify error
- [ ] Call `set_pain_limit("right_thigh", 101)` — verify error

**Expected:** Both return error. Limit unchanged.  
**Bug report if:** Invalid values accepted.

---

### T-50: Config Persistence After Restart

**Setup before restart:**
- Coyote-1: aliases `left_thigh` (limit=100%) / `right_thigh` (limit=100% after T-48)
- Lovense-1: alias `toy_a`
- Set a distinct limit: `set_pain_limit("right_thigh", 40)` via MCP tool (or UI)

**Human:** Restart the kink-mcp server.

- [ ] After restart: read `devices://status`
- [ ] `get_status()`
- [ ] Verify aliases `left_thigh`, `right_thigh`, `toy_a` preserved
- [ ] Verify `right_thigh` limit_pct = 40
- [ ] Verify devices auto-reconnected (or shown as offline if out of range)

**Expected:** All aliases, limits, and addresses survive restart.  
**Bug report if:** Aliases lost, wrong limits, or devices not attempted.

---

### T-51: Offline Device on Restart (Device Powered Off)

**Setup:** Power OFF Coyote-1 before restarting the server.  
**Human:** Restart the server.

- [ ] Via chrome plugin: open UI after restart
- [ ] Verify Coyote-1 appears as "offline" with "Retry" button
- [ ] Verify other devices (Lovense-1) auto-reconnected normally

**Expected:** Offline device shows with Retry. Other devices unaffected.  
**Bug report if:** Server crashes, no Retry button, or other devices fail to reconnect.

---

### T-52: Manual Retry After Powering Device Back On

**Precondition:** T-51 passed. Power Coyote-1 back ON.

- [ ] Via chrome plugin: click Retry on Coyote-1
- [ ] Confirm device connects
- [ ] Verify aliases `left_thigh` / `right_thigh` restored
- [ ] Verify `right_thigh` pain limit = 40% (from T-50 setup)
- [ ] Retry button disappears

**Expected:** Device reconnects with full state restored.  
**Bug report if:** Retry fails, limits/aliases wrong, or button persists after success.

---

## Phase 14 — All 4 Devices: Alias Sync

### T-53: Connect Coyote-2 and Lovense-2

**Setup:** Coyote-1 and Lovense-1 already connected. Ensure Coyote-2 and Lovense-2 are powered on.

- [ ] Via chrome plugin: scan for devices
- [ ] Connect Coyote-2 with alias_a = `dev2_a`, alias_b = `dev2_b`
- [ ] Connect Lovense-2 with alias_a = `toy_b`
- [ ] `get_status()` — verify all 4 devices / channels present

**Expected:** All 4 devices connected. `get_status()` shows `left_thigh`, `right_thigh`, `dev2_a`, `dev2_b`, `toy_a`, `toy_b`.  
**Bug report if:** Any device fails to connect, wrong aliases, or status missing channels.

---

### T-54: Same-Device Channel Sync (Coyote-1)

**Setup (human via UI):** Reconnect Coyote-1 with alias_a = `both`, alias_b = `both` (same alias for both channels).

- [ ] `play_wave("both", "pulse_high")`
- [ ] `set_strength("both", 100)`
- [ ] `get_status()` — verify 2 channel entries under alias `both`
- [ ] Human confirms both channels of Coyote-1 fire simultaneously

**Expected:** Both A and B channels of Coyote-1 fire at the same time.  
**Bug report if:** Only one channel fires, or status shows only one entry under `both`.

---

### T-55: Cross-Device Sync (Coyote-1 + Coyote-2)

**Setup (human via UI):**
1. Reconnect Coyote-1 with alias_a = `sync_test`, alias_b = `coyote1_b`
2. Reconnect Coyote-2 with alias_a = `sync_test`, alias_b = `coyote2_b`

Both Coyotes' channel A share alias `sync_test`.

- [ ] `play_wave("sync_test", "pulse_high")`
- [ ] `set_strength("sync_test", 100)`
- [ ] `get_status()` — verify 2 channel entries under `sync_test`
- [ ] Human confirms both Coyote-1 channel A and Coyote-2 channel A fire simultaneously

**Expected:** Both devices' A channels produce audible output at the same time.  
**Bug report if:** Only one device fires, or cross-device sync not working.

---

### T-56: Independent Channels on Same Device

**Setup:** Coyote-1 with alias_a = `ch_a`, alias_b = `ch_b` (distinct aliases).

- [ ] `play_wave("ch_a", "pulse_high")` + `set_strength("ch_a", 100)`
- [ ] `get_status()` — verify `ch_b` wave_active=false, strength unchanged
- [ ] Human confirms only channel A fires
- [ ] `play_wave("ch_b", "pulse_low")` + `set_strength("ch_b", 100)`
- [ ] Human confirms both channels fire independently with different wave patterns

**Expected:** Each channel controlled independently without bleeding.  
**Bug report if:** Commands bleed between channels, or both channels respond to single-channel command.

---

### T-57: Alias Rename During Active Session

**Setup:** Coyote-1 `ch_a` with active `play_wave` + strength 100%.

- [ ] Via chrome plugin: rename `ch_a` to `ch_a_renamed`
- [ ] Call `set_strength("ch_a_renamed", 100)` — verify success
- [ ] Call `set_strength("ch_a", 100)` — verify error (old alias gone)

**Expected:** New alias works; old alias returns error. Activity timestamps transferred.  
**Bug report if:** Old alias still works, rename fails under load, or device state lost.

---

## Phase 15 — Two Lovense Simultaneously

### T-58: Two Lovense Devices — Independent Control

**Setup:** Both Lovense-1 (`toy_a`) and Lovense-2 (`toy_b`) connected.

- [ ] `vibrate("toy_a", 100)`
- [ ] `vibrate("toy_b", 30)`
- [ ] `get_status()` — verify toy_a=100%, toy_b=30%
- [ ] Human confirms each toy vibrates at a noticeably different intensity

**Expected:** Independent intensity control per device.  
**Bug report if:** Both vibrate at same level, or one doesn't respond.

---

### T-59: Two Lovense — Shared Alias Sync

**Setup (human via UI):** Reconnect both Lovense devices with alias `both_toys`.

- [ ] `vibrate("both_toys", 100)` — human confirms both vibrate
- [ ] `vibrate("both_toys", 0)` — human confirms both stop

**Expected:** Both toys respond together to the same command.  
**Bug report if:** Only one toy responds, or stop doesn't silence both.

---

## Phase 16 — Mixed Session: All 4 Devices

### T-60: Simultaneous Coyote + Lovense (All 4)

**Setup:** All 4 devices connected (Coyote-1, Coyote-2, Lovense-1, Lovense-2) with distinct aliases.

- [ ] `play_wave("sync_test", "pulse_mid")` + `set_strength("sync_test", 100)` — both Coyotes via synced alias
- [ ] `vibrate("toy_a", 100)`
- [ ] `vibrate("toy_b", 50)`
- [ ] `get_status()` — verify all active simultaneously
- [ ] `stop_wave()` — verify all Coyote channels stop, Lovenses continue
- [ ] `vibrate("toy_a", 0)` + `vibrate("toy_b", 0)` — verify all silent

**Expected:** All 4 devices run simultaneously. `stop_wave()` affects only Coyote channels.  
**Human:** Confirm all devices active at the same time; Lovenses keep vibrating after stop_wave.  
**Bug report if:** `stop_wave()` affects Lovense, or any device doesn't respond.

---

## Phase 17 — UX Report & Recommendations

### T-61: UX Report (Agent Self-Assessment)

After completing all tests, write a comprehensive UX report directly in the **UX Report** section at the bottom of this document. Cover:

**1. Test Results Summary**
- Total tests run, PASS / FAIL / SKIP counts
- Full list of all filed bug reports

**2. MCP Tool UX Observations**
- Which tool interactions felt natural vs. awkward?
- Were parameter names, types, and return messages clear?
- Were error messages informative or cryptic?
- Did the wave workflow (library → guide → design → play) feel coherent?
- Was resource naming (`ui://url`, `devices://status`, etc.) intuitive?

**3. Web UI Observations**
- Was the scan → connect → configure flow smooth?
- Were any UI elements missing, confusing, or inconsistently positioned?
- Was the 1-second polling refresh appropriate?
- Was the pain limit slider intuitive?
- Was the LLM toggle + restart requirement clearly communicated?

**4. Device Behavior Observations**
- Did device responses match documented behavior based on human feedback?
- Were wave transitions smooth?
- Were intensity steps meaningful and perceptible?

**5. Improvement Suggestions**
- Missing features (e.g., `design_wave` does not save to library — README says it should; `stop_wave` doesn't apply to Lovense)
- UX improvements (toast notifications, better error display, etc.)
- Documentation gaps
- Safety feature suggestions
- Any inconsistencies not captured in individual bug reports

---

## Bug Report Log

> Populated during testing. Add entries below as tests fail.

```
(empty — populate as tests fail)
```

---

## UX Report

> Agent fills this section during T-61.

```
(pending — filled after all tests complete)
```
