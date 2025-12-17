"""Interactive prompts."""

import questionary
from typing import List, Optional


def select_project(projects: List[str]) -> Optional[str]:
    """Select a project."""
    if not projects:
        return None
    return questionary.select("Select project:", choices=projects).ask()


def select_export_preset(presets: List[str]) -> Optional[str]:
    """Select export preset."""
    if not presets:
        return None
    return questionary.select("Select preset:", choices=presets).ask()


def confirm_action(message: str) -> bool:
    """Confirm action."""
    return questionary.confirm(message).ask()


def prompt_text(message: str, default: str = "") -> str:
    """Ask for text."""
    return questionary.text(message, default=default).ask()


def create_project_wizard() -> dict:
    """Interactive wizard for creating a project."""
    name = questionary.text(
        "Project Name:", validate=lambda text: len(text) > 0
    ).ask()

    renderer = questionary.select(
        "Renderer:",
        choices=[
            questionary.Choice("Forward Plus", value="forward_plus"),
            questionary.Choice("Mobile", value="mobile"),
            questionary.Choice("GL Compatibility", value="gl_compatibility"),
        ],
    ).ask()

    scripts = questionary.confirm(
        "Generate sample scripts?", default=False
    ).ask()

    return {"name": name, "renderer": renderer, "scripts": scripts}
