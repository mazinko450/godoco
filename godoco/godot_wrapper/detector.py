"""Godot executable detection."""

from __future__ import annotations
import shutil
import platform
import subprocess
import re
from pathlib import Path
from typing import Optional
import os


def find_godot_executable() -> Optional[Path]:
    """
    Find Godot executable on the system.

    Returns
    -------
    Optional[Path]
        Path to Godot executable if found.
    """
    system = platform.system()
    godot_exe = "godot.exe" if system == "Windows" else "godot"

    # Check PATH
    if p := shutil.which(godot_exe):
        return Path(p)

    # Check standard locations
    search_paths = (
        [Path.home() / "Desktop/Godot", Path.home() / "Downloads"]
        if system == "Windows"
        else [Path("/usr/local/bin")]
    )

    for d in search_paths:
        if d.exists():
            for f in d.rglob("*godot*"):
                if f.is_file() and os.access(f, os.X_OK):
                    # Basic filter to ensure it's likely the executable
                    if system == "Windows" and not f.name.endswith(".exe"):
                        continue
                    return f
    return None


def detect_godot_version(godot_path: Path) -> str:
    """
    Detect Godot version by running --version.

    Parameters
    ----------
    godot_path : Path
        Path to Godot executable.

    Returns
    -------
    str
        Version string (e.g. "4.3").
    """
    try:
        # Run with timeout
        result = subprocess.run(
            [str(godot_path), "--version"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        output = result.stdout.strip()
        # Parse output: "Godot Engine v4.3.stable.official..."
        # Regex to capture Major.Minor
        if m := re.search(r"v(\d+\.\d+)", output):
            return m.group(1)
        # Fallback if format differs
        if m := re.search(r"(\d+\.\d+)", output):
            return m.group(1)

    except Exception:
        pass

    return "4.3"  # Default fallback
