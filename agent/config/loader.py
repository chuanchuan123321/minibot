"""Configuration loader."""

import json
import os
from pathlib import Path

from agent.config.schema import Config


def get_config_path() -> Path:
    """Get the configuration file path."""
    config_dir = Path.home() / ".minibot"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "config.json"


def load_config(config_path: str | None = None) -> Config:
    """
    Load configuration from file.

    Args:
        config_path: Path to config file. If None, uses default location.

    Returns:
        Config object.
    """
    if config_path is None:
        config_path = str(get_config_path())

    config_file = Path(config_path)

    if not config_file.exists():
        # Return default config
        return Config()

    try:
        with open(config_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return Config(**data)
    except Exception as e:
        print(f"⚠️  Error loading config from {config_path}: {e}")
        print("Using default configuration")
        return Config()


def save_config(config: Config, config_path: str | None = None) -> bool:
    """
    Save configuration to file.

    Args:
        config: Config object to save.
        config_path: Path to config file. If None, uses default location.

    Returns:
        True if successful, False otherwise.
    """
    if config_path is None:
        config_path = str(get_config_path())

    config_file = Path(config_path)
    config_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config.model_dump(), f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"❌ Error saving config to {config_path}: {e}")
        return False


def create_default_config() -> None:
    """Create a default configuration file."""
    config_path = get_config_path()

    if config_path.exists():
        print(f"Config file already exists at {config_path}")
        return

    config = Config()
    if save_config(config, str(config_path)):
        print(f"✅ Created default config at {config_path}")
        print(f"Please edit {config_path} to add your API keys and channel credentials")
    else:
        print(f"❌ Failed to create config file")
