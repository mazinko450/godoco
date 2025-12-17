"""Table generation."""

from rich.table import Table
from typing import Dict, Any, Optional


def create_projects_table(
    projects: Dict[str, str], current: Optional[str]
) -> Table:
    """Create project list table."""
    table = Table(
        title="Projects", show_header=True, header_style="bold magenta"
    )
    table.add_column("Status", width=4)
    table.add_column("Name", style="cyan")
    table.add_column("Path", style="dim")

    for name, path in projects.items():
        status = "→" if name == current else ""
        table.add_row(status, name, path)

    return table


def create_info_table(data: Dict[str, Any]) -> Table:
    """Create info table."""
    table = Table(show_header=False)
    table.add_column("Key", style="bold")
    table.add_column("Value")

    for k, v in data.items():
        table.add_row(k, str(v))

    return table
