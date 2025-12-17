"""Configuration manager."""

from __future__ import annotations
from pathlib import Path
import json
from typing import Optional
from .models import AppConfig
from ..utils.errors import InvalidConfigError

CONFIG_PATH = Path.home() / ".godoco.json"


class ConfigManager:
    """Manages loading and saving of application configuration."""

    def __init__(self, path: Path = CONFIG_PATH):
        self.path = path
        self._config: Optional[AppConfig] = None

    def load(self) -> AppConfig:
        """
        Load configuration from disk.
        """
        if self._config:
            self.validate_projects()
            return self._config

        if not self.path.exists():
            self._config = AppConfig()
            return self._config

        try:
            data = json.loads(self.path.read_text())
            self._config = AppConfig(**data)
            self.validate_projects()
            return self._config
        except Exception:
            # Return fresh config on error
            self._config = AppConfig()
            return self._config

    def validate_projects(self) -> None:
        """Remove projects that no longer exist."""
        if not self._config:
            return

        cleaned = {}
        modified = False
        for name, path_str in self._config.projects.items():
            if Path(path_str).exists():
                cleaned[name] = path_str
            else:
                modified = True

        if modified:
            self._config.projects = cleaned
            if self._config.current_project not in cleaned:
                self._config.current_project = None
            self.save()

    def save(self, config: Optional[AppConfig] = None) -> None:
        """
        Save configuration to disk.

        Parameters
        ----------
        config : Optional[AppConfig]
            Config to save. If None, saves currently loaded config.
        """
        if config:
            self._config = config

        if not self._config:
            return

        # Atomic write pattern could be implemented here,
        # but simple write is fine for now.
        content = self._config.model_dump_json(indent=4)
        self.path.write_text(content)

    def get_current_project(self) -> Optional[Path]:
        """Get path of current project."""
        cfg = self.load()
        if cfg.current_project and cfg.current_project in cfg.projects:
            return Path(cfg.projects[cfg.current_project])
        return None

    def track_project(self, name: str, path: Path) -> None:
        """
        Add project to config and set as current.

        Parameters
        ----------
        name : str
            Project name.
        path : Path
            Project path.
        """
        cfg = self.load()
        cfg.projects[name] = str(path)
        cfg.current_project = name
        self.save()

    def get_godot_path(self) -> Optional[Path]:
        """Get configured Godot executable path."""
        cfg = self.load()
        return cfg.godot.executable_path
