import json
import os
from pathlib import Path

_DEFAULT_CONFIG: dict = {
    "pain_limit_exposed_to_llm": False,
    "devices": [],
}


def get_config_path() -> Path:
    if os.name == "nt":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    config_dir = base / "kink-mcp"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "config.json"


def load_config() -> dict:
    path = get_config_path()
    if not path.exists():
        return dict(_DEFAULT_CONFIG)
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        return {**_DEFAULT_CONFIG, **data}
    except Exception:
        return dict(_DEFAULT_CONFIG)


def save_config(data: dict) -> None:
    path = get_config_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
