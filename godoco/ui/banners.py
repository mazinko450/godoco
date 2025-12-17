"""UI Banners."""

from .console import console

LOGO = r"""
   ______          __                 
  / ____/___  ____/ /___  _________   
 / / __/ __ \/ __  / __ \/ ___/ __ \  
/ /_/ / /_/ / /_/ / /_/ / /__/ /_/ /  
\____/\____/\__,_/\____/\___/\____/   
"""


def print_welcome_banner(version: str):
    """Print app banner."""
    console.print(f"[bold cyan]{LOGO}[/bold cyan]")
    console.print(f"[dim]Godot Code-Only Development Tool v{version}[/dim]")
    console.print()


def print_command_header(command: str):
    """Print header for command."""
    console.rule(f"[bold]{command}[/bold]")
