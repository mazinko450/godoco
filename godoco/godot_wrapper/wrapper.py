"""Godot Engine Wrapper."""

from __future__ import annotations
import subprocess
from pathlib import Path
from typing import Optional, List, Any


class GodotWrapper:
    """Wraps Godot executable interactions."""

    def __init__(self, godot_path: Path):
        self.godot_path = godot_path

    def _build_cmd(self, project_path: Path, args: List[str]) -> List[str]:
        return [str(self.godot_path), "--path", str(project_path)] + args

    def run_editor(
        self, project_path: Path, **kwargs
    ) -> subprocess.CompletedProcess:
        """
        Run Godot editor or game.

        Kwargs can be:
        - editor: bool (open editor)
        - scene: str (run specific scene)
        - fullscreen: bool
        - debug: bool
        """
        args = []
        if kwargs.get("editor"):
            args.append("--editor")

        if kwargs.get("fullscreen"):
            args.append("--fullscreen")

        if kwargs.get("maximized"):
            args.append("--maximized")

        if scene := kwargs.get("scene"):
            args.append(scene)

        cmd = self._build_cmd(project_path, args)
        return subprocess.run(cmd)

    def run_headless(
        self, project_path: Path, script: Optional[Path] = None, **kwargs
    ) -> subprocess.CompletedProcess:
        """Run headless (for scripts/formatting)."""
        args = ["--headless"]
        if script:
            args.extend(["--script", str(script)])

        cmd = self._build_cmd(project_path, args)
        return subprocess.run(cmd)

    def export_project(
        self, project_path: Path, preset: str, output: Path, debug: bool = False
    ) -> subprocess.CompletedProcess:
        """Export project."""
        args = [
            "--headless",
            "--export-debug" if debug else "--export-release",
            preset,
            str(output),
        ]

        cmd = self._build_cmd(project_path, args)
        return subprocess.run(cmd, check=True)

    def get_cli_args(self, **kwargs) -> List[str]:
        """Convert kwargs to CLI args (helper)."""
        args = []
        for k, v in kwargs.items():
            if v is True:
                args.append(f"--{k.replace('_', '-')}")
            elif isinstance(v, str):
                args.append(f"--{k.replace('_', '-')}")
                args.append(v)
        return args
