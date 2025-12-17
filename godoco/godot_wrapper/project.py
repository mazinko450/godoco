"""Godot project file management."""

from __future__ import annotations
from pathlib import Path
import re
from typing import Optional


class ProjectGodotFile:
    """Parses and updates project.godot files."""

    def __init__(self, path: Path):
        self.path = path / "project.godot"

    def exists(self) -> bool:
        """Check if project.godot exists."""
        return self.path.exists()

    def read(self) -> str:
        """Read content."""
        return self.path.read_text(encoding="utf-8") if self.exists() else ""

    def write(self, content: str) -> None:
        """Write content."""
        self.path.write_text(content, encoding="utf-8")

    def get_value(self, section: str, key: str) -> Optional[str]:
        """
        Get value from config.
        Crucial simplified parser: mostly looks for key=value
        """
        content = self.read()
        # Regex (simplified): key="value" or key=123
        # Use simple search for parsing, not full ini parser as Godot has unique syntax
        pattern = re.compile(rf"{key}=(.+)")
        if m := pattern.search(content):
            return m.group(1).strip()
        return None

    def update_setting(self, key_pattern: str, new_value: str) -> bool:
        """
        Update a setting using regex pattern.
        """
        if not self.exists():
            return False
        content = self.read()
        if re.search(key_pattern, content):
            content = re.sub(key_pattern, new_value, content)
            self.write(content)
            return True
        return False

    def update_icon(self, icon_path: str) -> None:
        """Update application/config/icon."""
        # This regex tries to find config/icon="old"
        self.update_setting(
            r'config/icon="[^"]*"', f'config/icon="{icon_path}"'
        )

    def update_main_scene(self, scene_path: str) -> None:
        """Update run/main_scene."""
        self.update_setting(
            r'run/main_scene="[^"]*"', f'run/main_scene="{scene_path}"'
        )

    def set_renderer(self, renderer: str, version: str) -> None:
        """Set rendering method."""
        feat = {
            "forward_plus": "Forward Plus",
            "mobile": "Mobile",
            "gl_compatibility": "GL Compatibility",
        }.get(renderer, "Forward Plus")
        self.update_setting(
            r'rendering_method="[^"]*"', f'rendering_method="{renderer}"'
        )
        self.update_setting(
            r"config/features=PackedStringArray\([^)]*\)",
            f'config/features=PackedStringArray("{version}", "{feat}")',
        )
