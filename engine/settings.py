"""
Settings persistence for Nexora
"""
import os
import yaml
from typing import Dict, Any, Optional
from .utils import DATA_DIR, log

SETTINGS_PATH = os.path.join(DATA_DIR, "settings.yml")


def save_settings(settings: Dict[str, Any]) -> None:
    """Save settings to YAML file"""
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            yaml.dump(settings, f, default_flow_style=False)
        log.info("Settings saved")
    except Exception as e:
        log.error(f"Failed to save settings: {e}")


def load_settings() -> Optional[Dict[str, Any]]:
    """Load settings from YAML file"""
    if not os.path.exists(SETTINGS_PATH):
        return None
    
    try:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            settings = yaml.safe_load(f)
        log.info("Settings loaded")
        return settings
    except Exception as e:
        log.error(f"Failed to load settings: {e}")
        return None


def get_setting(key: str, default: Any = None) -> Any:
    """Get a specific setting"""
    settings = load_settings()
    if settings:
        return settings.get(key, default)
    return default


def update_setting(key: str, value: Any) -> None:
    """Update a specific setting"""
    settings = load_settings() or {}
    settings[key] = value
    save_settings(settings)

