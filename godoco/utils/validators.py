"""Input validation utilities."""

from __future__ import annotations
from pathlib import Path
import re
from .errors import ProjectNotFoundError, GodotNotFoundError


def validate_project_path(path: Path) -> bool:
    """
    Check if directory contains project.godot.

    Parameters
    ----------
    path : Path
        Directory to check.

    Returns
    -------
    bool
        True if project.godot exists.
    """
    return (path / "project.godot").exists()


def validate_godot_executable(path: Path) -> bool:
    """
    Check if godot executable exists and is executable.

    Parameters
    ----------
    path : Path
        Path to executable.

    Returns
    -------
    bool
        True if valid.
    """
    import os

    return path.exists() and path.is_file() and os.access(path, os.X_OK)


def validate_scene_path(path: Path) -> bool:
    """
    Check if path has .tscn extension.

    Parameters
    ----------
    path : Path
        File path.

    Returns
    -------
    bool
        True if valid extension.
    """
    return path.suffix == ".tscn"


def validate_version_string(version: str) -> bool:
    """
    Validate version string format (X.Y or X.Y.Z).

    Parameters
    ----------
    version : str
        Version string.

    Returns
    -------
    bool
        True if matches pattern.
    """
    return bool(re.match(r"^\d+\.\d+(\.\d+)?$", version))
