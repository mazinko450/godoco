import typer
from .commands import app as commands_app
from ..ui.banners import print_welcome_banner
from .. import __version__
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
import subprocess
import re
from ..godot_wrapper.detector import find_godot_executable
from typer import rich_utils
from rich import box, print
import click
from typer.core import TyperGroup


class PassthroughGroup(TyperGroup):
    """Custom Group allowing unknown commands/args to fall back to the main callback."""

    # resolve_command removed

    def parse_args(self, ctx: click.Context, args: list[str]) -> list[str]:
        # Run standard parsing
        # Group.parse_args manually handles formatting protected_args
        # We let it do its job, then check the result.
        remaining_args = super().parse_args(ctx, args)

        # TyperGroup/Click Group logic puts the first non-option arg into ctx.protected_args
        # if chain is False.
        # Note: protected_args is a property, need to use internal _protected_args
        if ctx.protected_args:
            cmd_name = ctx.protected_args[0]
            # Check if it is a real command
            if not self.get_command(ctx, cmd_name):
                # Not a command, so treat it as an argument for the callback
                # Prepend it back to ctx.args
                ctx.args.insert(0, cmd_name)
                # Clear protected args so invoke() triggers invoke_without_command logic
                ctx._protected_args = []

        return ctx.args


def get_godot_help_options() -> list[tuple[str, str]]:
    """Extract options from Godot help output."""
    exe = find_godot_executable()
    if not exe:
        return []

    try:
        # Run Godot --help and capture output
        # Ensure we don't get colored output from Godot if possible,
        # though --help usually ignores it.
        result = subprocess.run(
            [str(exe), "--help"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        output = result.stdout

        # Strip ANSI codes
        ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
        output = ansi_escape.sub("", output)

        # Godot help format usually:
        # "  --option <arg>    Description..."
        # But sometimes description is close or wrapped.

        options = []
        for line in output.splitlines():
            line = line.strip()
            if not line.startswith("-"):
                continue

            # Skip header lines if they accidentally start with -
            if line.startswith("---"):
                continue

            # Attempt 1: Split by 2+ spaces or tab
            parts = re.split(r"(\s{2,}|\t)", line, maxsplit=1)

            opt = ""
            desc = ""

            if len(parts) >= 3:
                opt = parts[0].strip()
                desc = parts[2].strip()
            else:
                # Attempt 2: Regex for -flag [args] <space> Description
                # Match: ^ (-short|--long) (optional args) (space) (Description)
                match = re.search(r"^(--?[\w-]+(?: [^ ]+)?)\s+(.*)$", line)
                if match:
                    opt = match.group(1).strip()
                    desc = match.group(2).strip()
                else:
                    # Fallback: Treat whole line as option if no split found
                    opt = line

            if opt:
                options.append((opt, desc))

        return options

    except Exception:
        return []


def print_combined_help(ctx: typer.Context):
    """Print Godoco + Godot help."""
    console = Console()

    # 1. Print Banner
    print_welcome_banner(__version__)

    # 2. Print Godoco Help (Commands & Options)
    # We can use ctx.get_help() but it returns a string.
    # We want to use Rich to verify it looks good.
    # Actually, proper integration into the Options table is hard because it's managed by Click.

    # Let's print the Godoco help first.
    print(ctx.get_help())

    # 3. Print Godot Options
    godot_opts = get_godot_help_options()
    if godot_opts:
        # Create a table matching Rich help style
        table = Table(
            box=rich_utils.BOX_STYLE,
            show_header=False,
            show_edge=True,
            pad_edge=False,
            collapse_padding=True,
        )
        table.add_column("Option", style="bold cyan", no_wrap=True)
        table.add_column("Description")

        for opt, desc in godot_opts:
            table.add_row(opt, desc)

        panel = Panel(
            table,
            title="[bold]Godot Engine Options[/bold]",
            title_align="left",
            border_style="dim",
            box=rich_utils.BOX_STYLE,
        )
        console.print(panel)


def custom_rich_format_help(obj, ctx, markup_mode):
    """
    Custom help format:
    1. Welcome Banner (Root only)
    2. Usage
    3. Commands Panel (with Headers)
    4. Option Legend (Boxed) - ABOVE Options
    5. Options Panel (Godoco) (with Headers)
    6. Godot Options Panel (Separate) (with Headers)
    """
    console = Console()

    # 1. Welcome Banner (Only for Root command)
    if ctx.parent is None:
        print_welcome_banner(__version__)

    # 2. Print Usage
    # Clean up Usage string "Usage: Usage: ..."
    usage_str = (
        ctx.command.get_usage(ctx)
        if ctx.command
        else "godoco [OPTIONS] COMMAND [ARGS]..."
    )
    if usage_str.startswith("Usage: "):
        usage_str = usage_str[len("Usage: ") :]
    print(f"\n [bold]Usage:[/bold] {usage_str}\n")

    # 3. Print Description
    help_text = getattr(obj, "help", None) or getattr(ctx.command, "help", "")
    if help_text:
        help_text = str(help_text)  # Ensure string
        console.print(
            Text.from_markup(help_text) if markup_mode == "rich" else help_text
        )
        print()

    # 4. Print Commands
    if hasattr(obj, "list_commands"):
        commands = []
        for cmd_name in obj.list_commands(ctx):
            cmd = obj.get_command(ctx, cmd_name)
            if cmd and not cmd.hidden:
                # Use short_help, fallback to first line of help (docstring)
                help_str = cmd.short_help or cmd.help or ""
                # If help is multiline, take first line
                if help_str:
                    help_str = help_str.split("\n")[0]
                commands.append((cmd_name, help_str))

        if commands:
            cmd_table = Table(highlight=True, box=None, show_header=True)
            cmd_table.add_column("Command", style="bold cyan", no_wrap=True)
            cmd_table.add_column("Description")
            for name, help in commands:
                cmd_table.add_row(name, help)

            console.print(
                Panel(
                    cmd_table,
                    title="Commands",
                    border_style="dim",
                    title_align="left",
                    box=box.ROUNDED,
                )
            )

    # 5. Option Legend (Godot Style) - Boxed and Above
    if ctx.parent is None:
        legend = Text()
        legend.append("  R", style="bold green")
        legend.append(
            "  Available in editor builds, debug export templates and release export templates.\n"
        )
        legend.append("  D", style="bold blue")
        legend.append(
            "  Available in editor builds and debug export templates only.\n"
        )
        legend.append("  E", style="bold red")
        legend.append("  Only available in editor builds.")

        console.print(
            Panel(
                legend,
                title="Option Legend (this build = editor)",
                border_style="dim",
                title_align="left",
                box=box.ROUNDED,
            )
        )

    # 6. Print Options (Godoco)
    options_table = Table(highlight=True, box=None, show_header=True)
    options_table.add_column("Option", style="bold cyan")
    options_table.add_column("Description", ratio=1)

    # Typer Options
    if hasattr(obj, "get_params"):
        for param in obj.get_params(ctx):
            if param.hidden:
                continue

            primary_opts = param.opts
            secondary_opts = param.secondary_opts

            def fmt_opt(o):
                if o.startswith("-"):
                    return o
                return f"--{o}" if len(o) > 1 else f"-{o}"

            p_str = ", ".join([fmt_opt(o) for o in reversed(primary_opts)])
            if secondary_opts:
                p_str += " / " + ", ".join([
                    fmt_opt(o) for o in reversed(secondary_opts)
                ])

            desc = param.help or ""
            options_table.add_row(p_str, desc)

    if options_table.row_count > 0:
        console.print(
            Panel(
                options_table,
                title="Options",
                border_style="dim",
                title_align="left",
                box=box.ROUNDED,
            )
        )

    # 7. Print Godot Options (Separate Panel)
    if ctx.parent is None:
        godot_opts = get_godot_help_options()
        if godot_opts:
            godot_table = Table(highlight=True, box=None, show_header=True)
            godot_table.add_column(
                "Option", style="bold cyan", no_wrap=False
            )  # Allow wrap
            godot_table.add_column("Description", ratio=1)  # Force width

            for opt, desc in godot_opts:
                # Colorize R, D, E at start of description
                desc_colored = desc
                if (
                    desc_colored.startswith("R ")
                    or desc_colored.startswith("R\t")
                    or desc_colored == "R"
                ):
                    desc_colored = desc_colored.replace(
                        "R", "[bold green]R[/bold green]", 1
                    )
                elif (
                    desc_colored.startswith("D ")
                    or desc_colored.startswith("D\t")
                    or desc_colored == "D"
                ):
                    desc_colored = desc_colored.replace(
                        "D", "[bold blue]D[/bold blue]", 1
                    )
                elif (
                    desc_colored.startswith("E ")
                    or desc_colored.startswith("E\t")
                    or desc_colored == "E"
                ):
                    desc_colored = desc_colored.replace(
                        "E", "[bold red]E[/bold red]", 1
                    )

                godot_table.add_row(opt, desc_colored)

            console.print(
                Panel(
                    godot_table,
                    title="Godot Options",
                    border_style="dim",
                    title_align="left",
                    box=box.ROUNDED,
                )
            )


# Monkeypatch Typer's help formatter
rich_utils.rich_format_help = custom_rich_format_help


def version_callback(value: bool):
    if value:
        print_welcome_banner(__version__)
        raise typer.Exit()


# Initialize main app
app = typer.Typer(
    name="godoco",
    cls=PassthroughGroup,  # Custom command resolution
    help="🎮 Godot Code-Only Development Tool",
    rich_markup_mode="rich",
    pretty_exceptions_enable=True,
    add_completion=False,
    context_settings={
        "allow_extra_args": True,
        "ignore_unknown_options": True,
        # help_option_names removed to re-enable default help
    },
)

# Merge commands
app.add_typer(commands_app)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(
        None,
        "--version",
        "-V",  # Changed from -v to -V to avoid conflict
        callback=version_callback,
        is_eager=True,
        help="Show version",
    ),
    help: bool = typer.Option(
        False, "--help", "-h", help="Show this message and exit."
    ),
):
    """
    Godoco - Godot Code-Only Development Tool.
    """
    if version:
        print_welcome_banner(__version__)
        raise typer.Exit()

    # Check for passthrough arguments (ctx.args contains unparsed/extra args)
    if ctx.args:
        # Run Godot with these arguments
        from ..godot_wrapper.detector import find_godot_executable
        import subprocess
        import sys

        exe = find_godot_executable()
        if exe:
            # We must pass the args exactly as received.
            try:
                # Use sys.exit to return Godot's exit code
                sys.exit(subprocess.run([str(exe)] + ctx.args).returncode)
            except Exception as e:
                typer.echo(f"Error running Godot: {e}", err=True)
                raise typer.Exit(1)
        else:
            typer.echo(
                "Godot executable not configured. Run 'godoco setup'.", err=True
            )
            raise typer.Exit(1)

    if help or ctx.invoked_subcommand is None:
        # If no subcommand, just show help (which will use our custom formatter)
        # Note: --help is handled by Typer before this, but if user runs `godoco` (no args),
        # we want to show help.
        # We can trigger help manually.
        rich_utils.rich_format_help(ctx.command, ctx, "rich")
        raise typer.Exit()
