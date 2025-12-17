"""Path utilities for Godoco."""

from __future__ import annotations
from pathlib import Path
from typing import Optional


def resolve_project_path(
    name_or_path: Optional[str] = None,
    current_project: Optional[str] = None,
    projects_map: dict[str, str] = None,
) -> Path:
    """
    Resolve project path from name, path string, or current working directory.

    Parameters
    ----------
    name_or_path : Optional[str]
        Project name (from config) or file system path.
    current_project : Optional[str]
        Path of the currently active project from config.
    projects_map : dict[str, str]
        Map of project names to paths from config.

    Returns
    -------
    Path
        Resolved absolute path to project directory.

    Raises
    ------
    FileNotFoundError
        If path does not exist.
    """
    if not name_or_path:
        # Try current project from config
        if current_project:
            p = Path(current_project)
            if p.exists():
                return p

        # Try context (cwd)
        cwd = Path.cwd()
        if (cwd / "project.godot").exists():
            return cwd

        return cwd

    # Check if key in projects map
    if projects_map and name_or_path in projects_map:
        return Path(projects_map[name_or_path])

    # Check if valid path
    p = Path(name_or_path)
    if p.exists():
        return p if p.is_dir() else p.parent

    return p


def make_godot_path_relative(project_root: Path, file_path: Path) -> str:
    """
    Convert absolute path to Godot res:// path.

    Parameters
    ----------
    project_root : Path
        Root directory of the Godot project.
    file_path : Path
        Absolute path to the file.

    Returns
    -------
    str
        Path string starting with res://
    """
    try:
        rel = file_path.relative_to(project_root)
        return f"res://{rel.as_posix()}"
    except ValueError:
        return file_path.as_posix()
