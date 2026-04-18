import json
import pytest
from pathlib import Path


def test_load_config_returns_defaults_when_no_file(tmp_path, monkeypatch):
    monkeypatch.setenv("APPDATA", str(tmp_path))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    import importlib
    import kink_mcp.config as cfg_mod
    importlib.reload(cfg_mod)
    cfg = cfg_mod.load_config()
    assert cfg["pain_limit_exposed_to_llm"] is False
    assert cfg["devices"] == []


def test_save_and_load_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setenv("APPDATA", str(tmp_path))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    import importlib
    import kink_mcp.config as cfg_mod
    importlib.reload(cfg_mod)
    data = {
        "pain_limit_exposed_to_llm": True,
        "devices": [
            {
                "address": "AA:BB:CC:DD:EE:FF",
                "name": "Coyote V3",
                "device_type": "coyote",
                "version": "v3",
                "alias_a": "left_thigh",
                "alias_b": "right_thigh",
                "limit_a_pct": 50,
                "limit_b_pct": 40,
            }
        ],
    }
    cfg_mod.save_config(data)
    loaded = cfg_mod.load_config()
    assert loaded["pain_limit_exposed_to_llm"] is True
    assert loaded["devices"][0]["alias_a"] == "left_thigh"
    assert loaded["devices"][0]["limit_a_pct"] == 50


def test_load_config_handles_corrupt_file(tmp_path, monkeypatch):
    monkeypatch.setenv("APPDATA", str(tmp_path))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    import importlib
    import kink_mcp.config as cfg_mod
    importlib.reload(cfg_mod)
    path = cfg_mod.get_config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("not valid json")
    cfg = cfg_mod.load_config()
    assert cfg["devices"] == []


def test_load_config_merges_missing_keys(tmp_path, monkeypatch):
    monkeypatch.setenv("APPDATA", str(tmp_path))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    import importlib
    import kink_mcp.config as cfg_mod
    importlib.reload(cfg_mod)
    path = cfg_mod.get_config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"devices": []}))
    cfg = cfg_mod.load_config()
    assert "pain_limit_exposed_to_llm" in cfg
