"""Rich console integration."""

from rich.console import Console
from rich.theme import Theme
from rich.panel import Panel
from typing import Optional

# Custom theme
theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "success": "bold green",
})

console = Console(theme=theme)


def print_success(msg: str):
    """Print success message."""
    console.print(f"[success]✓[/success] {msg}")


def print_error(msg: str, exception: Optional[Exception] = None):
    """Print error message."""
    console.print(f"[error]✗ {msg}[/error]")
    if exception:
        console.print_exception()


def print_warning(msg: str):
    """Print warning."""
    console.print(f"[warning]! {msg}[/warning]")


def print_info(msg: str):
    """Print info."""
    console.print(f"[info]i {msg}[/info]")


def print_panel(msg: str, title: str):
    """Print panel."""
    console.print(Panel(msg, title=title, border_style="cyan"))
