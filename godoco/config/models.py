"""Configuration models."""

from __future__ import annotations
from typing import Optional, Dict
from pathlib import Path
from pydantic import BaseModel, Field, validator
from datetime import datetime


class ProjectConfig(BaseModel):
    """Configuration for a single project."""

    name: str
    path: Path
    last_accessed: datetime = Field(default_factory=datetime.now)


class GodotConfig(BaseModel):
    """Configuration for Godot engine."""

    executable_path: Optional[Path] = None
    version: Optional[str] = "4.3"  # Default fallback
    auto_detect: bool = True


class AppConfig(BaseModel):
    """Global application configuration."""

    current_project: Optional[str] = None
    projects: Dict[str, str] = Field(
        default_factory=dict
    )  # Name -> Path string
    godot: GodotConfig = Field(default_factory=GodotConfig)

    @validator("projects")
    def validate_projects(cls, v):
        """Ensure paths are valid."""
        return v
