"""CLI Commands."""

import typer
import click
from pathlib import Path
from typing import Optional, Literal
import subprocess
import re

from ..config.manager import ConfigManager
from ..config.models import AppConfig
from ..godot_wrapper.detector import find_godot_executable, detect_godot_version
from ..godot_wrapper.wrapper import GodotWrapper
from ..godot_wrapper.project import ProjectGodotFile
from ..ui.console import (
    print_success,
    print_error,
    print_info,
    print_panel,
    console,
)
from ..ui.tables import create_projects_table, create_info_table
from ..ui.prompts import (
    create_project_wizard,
)
from ..utils.paths import resolve_project_path
from ..utils.errors import GodocoError


app = typer.Typer()
cfg_mgr = ConfigManager()

ICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128"><rect width="124" height="124" x="2" y="2" fill="#363d52" stroke="#212532" stroke-width="4" rx="14"/><g fill="#fff" transform="translate(12.322 12.322)scale(.101)"><path d="M105 673v33q407 354 814 0v-33z"/><path fill="#478cbf" d="m105 673 152 14q12 1 15 14l4 67 132 10 8-61q2-11 15-15h162q13 4 15 15l8 61 132-10 4-67q3-13 15-14l152-14V427q30-39 56-81-35-59-83-108-43 20-82 47-40-37-88-64 7-51 8-102-59-28-123-42-26 43-46 89-49-7-98 0-20-46-46-89-64 14-123 42 1 51 8 102-48 27-88 64-39-27-82-47-48 49-83 108 26 42 56 81zm0 33v39c0 276 813 276 814 0v-39l-134 12-5 69q-2 10-14 13l-162 11q-12 0-16-11l-10-65H446l-10 65q-4 11-16 11l-162-11q-12-3-14-13l-5-69z"/><path d="M483 600c0 34 58 34 58 0v-86c0-34-58-34-58 0z"/><circle cx="725" cy="526" r="90"/><circle cx="299" cy="526" r="90"/></g><g fill="#414042" transform="translate(12.322 12.322)scale(.101)"><circle cx="307" cy="532" r="60"/><circle cx="717" cy="532" r="60"/></g></svg>"""

ICON_IMPORT = '[remap]\nimporter="texture"\ntype="CompressedTexture2D"\npath="res://.godot/imported/icon.svg"\n[params]\ncompress/mode=0\n'


def get_godot_wrapper() -> GodotWrapper:
    """Get configured Godot wrapper."""
    cfg: AppConfig = cfg_mgr.load()
    if cfg.godot.executable_path and cfg.godot.executable_path.exists():
        return GodotWrapper(cfg.godot.executable_path)

    # Try auto-detect
    if godot := find_godot_executable():
        return GodotWrapper(godot)

    print_error("Godot not found. Run 'godoco setup' first.")
    raise typer.Exit(1)


def get_proj_path(name: Optional[str] = None) -> Path:
    """Helper to resolve project path."""
    cfg: AppConfig = cfg_mgr.load()
    return resolve_project_path(name, cfg.current_project, cfg.projects)


def ensure_main_scene(proj: Path) -> None:
    """Auto-detect and set main scene if missing."""
    pf = ProjectGodotFile(proj)
    if not pf.exists():
        return

    content = pf.read()
    if 'run/main_scene=""' in content:
        if scenes := list(proj.rglob("*.tscn")):
            try:
                rel = scenes[0].relative_to(proj).as_posix()
                pf.update_main_scene(f"res://{rel}")
                print_info(f"Auto-set main scene: {rel}")
            except ValueError:
                pass


@app.command()
def setup(
    path: Optional[str] = typer.Option(
        None, "--path", help="Path to Godot executable"
    ),
) -> None:
    """Setup Godot executable."""
    if path:
        exe = Path(path)
    else:
        exe = find_godot_executable()

    if not exe or not exe.exists():
        print_error(
            "Godot executable not found. Please specify --path or install Godot."
        )
        raise typer.Exit(1)

    version = detect_godot_version(exe)

    cfg: AppConfig = cfg_mgr.load()
    cfg.godot.executable_path = exe
    cfg.godot.version = version
    cfg_mgr.save(cfg)

    print_panel(
        f"Executable: {exe}\nVersion: {version}", "Godot Setup Complete"
    )


def ensure_script_attachment(proj: Path) -> None:
    """Ensure src/main.gd is attached to main.tscn if it exists."""
    main_scene = proj / "main.tscn"
    script = proj / "src" / "main.gd"

    if not main_scene.exists() or not script.exists():
        return

    content = main_scene.read_text()

    # Check if script is already attached (simple string check)
    if 'path="res://src/main.gd"' in content:
        return

    # Check if we can safely inject
    # Look for [gd_scene ...] header
    if "[gd_scene" not in content:
        return

    print_info("Attaching src/main.gd to main.tscn...")

    # update load_steps if possible, or just add resource
    # For simplicity in this tool, we will try to inject the resource definition
    # before the first node or resource.

    # 1. Add ExtResource definition
    # We assign id="1_script" to avoid conflict with standard "1_script" if possible
    # but "1_script" is standard for single script.
    resource_def = '\n[ext_resource type="Script" path="res://src/main.gd" id="1_script"]\n'

    # Insert after format line
    content = re.sub(
        r"(\[gd_scene.*?\])", r"\1" + resource_def, content, count=1
    )

    # 2. Attach to root node
    # Find [node name="Main" ...] and append script = ExtResource("1_script")
    # We use regex to match the node header
    content = re.sub(
        r'(\[node name=".*?" type=".*?"]\n)',
        r'\1script = ExtResource("1_script")\n',
        content,
        count=1,
    )

    main_scene.write_text(content)
    print_success("Script attached successfully.")


@app.command()
def create(
    name: Optional[str] = typer.Argument(None, help="Project name"),
    path: str = typer.Option(".", "--path", "-p", help="Project path"),
    renderer: Optional[str] = typer.Option(
        None,
        "--renderer",
        "-r",
        help="Renderer (forward_plus, mobile, gl_compatibility)",
    ),
    scripts: Optional[bool] = typer.Option(
        None, "--scripts", "-s", help="Generate sample scripts"
    ),
    # Interactive flag removed
) -> None:
    """Create a new Godot project."""

    # Interactive Wizard Trigger
    if name is None:
        data = create_project_wizard()
        if not data:
            raise typer.Exit()
        name = data["name"]
        renderer = data["renderer"]
        scripts = data["scripts"]
    else:
        # Defaults or Interactive for missing args?
        # User requested "interactive by default".
        # If args are missing, prompt.
        if renderer is None:
            renderer = typer.prompt(
                "Renderer",
                default="forward_plus",
                type=click.Choice(
                    ["forward_plus", "mobile", "gl_compatibility"],
                    case_sensitive=False,
                ),
            )

        if scripts is None:
            scripts = typer.confirm("Generate sample scripts?", default=False)

    # Ensure valid renderer choice even if passed via flag
    if renderer not in ["forward_plus", "mobile", "gl_compatibility"]:
        print_error(f"Invalid renderer: {renderer}")
        raise typer.Exit(1)

    proj_path = Path(path) / name
    if proj_path.exists():
        print_error(f"Directory {proj_path} already exists.")
        raise typer.Exit(1)

    proj_path.mkdir(parents=True)
    for d in ["src", "assets", "addons", ".godot"]:
        (proj_path / d).mkdir()

    (proj_path / ".gitignore").write_text(
        ".godot/\n.import/\nexport_presets.cfg\n"
    )
    (proj_path / ".gitattributes").write_text(
        "*.wav filter=lfs diff=lfs merge=lfs -text\n"
    )
    (proj_path / ".gdignore").write_text("")
    (proj_path / "addons/.gdignore").write_text("")
    (proj_path / "icon.svg").write_text(ICON_SVG)
    (proj_path / "icon.svg.import").write_text(ICON_IMPORT)

    cfg: AppConfig = cfg_mgr.load()
    version = cfg.godot.version or "4.3"

    # Map renderer to friendly name
    feat_map = {
        "forward_plus": "Forward Plus",
        "mobile": "Mobile",
        "gl_compatibility": "GL Compatibility",
    }
    feat_name = feat_map.get(renderer, "Forward Plus")

    pf = ProjectGodotFile(proj_path)
    pf.write(f'''config_version=5

[application]
config/name="{name}"
run/main_scene=""
config/features=PackedStringArray("{version}", "{feat_name}")
config/icon="res://icon.svg"

[display]
window/size/viewport_width=1280
window/size/viewport_height=720
window/size/resizable=true
window/stretch/mode="canvas_items"

[rendering]
renderer/rendering_method="{renderer}"
''')

    if scripts:
        (proj_path / "main.tscn").write_text(
            '[gd_scene load_steps=2 format=3 uid="uid://b4y5z1x2w3v4"]\n\n[ext_resource type="Script" path="res://src/main.gd" id="1_script"]\n\n[node name="Main" type="Node"]\nscript = ExtResource("1_script")\n'
        )
        (proj_path / "src/main.gd").write_text(
            'extends Node\n\nfunc _ready() -> void:\n\tprint("Ready")\n'
        )
    else:
        (proj_path / "main.tscn").write_text(
            '[gd_scene format=3 uid="uid://b4y5z1x2w3v4"]\n\n[node name="Main" type="Node"]\n'
        )

    cfg_mgr.track_project(name, proj_path)
    print_success(f"Project '{name}' created at {proj_path}")


@app.command()
def run(
    proj: Optional[str] = typer.Option(None, "--project", "-p"),
    scene: Optional[str] = typer.Option(None, "--scene", "-s"),
    editor: bool = False,
    debug: bool = False,
    fullscreen: bool = False,
    maximized: bool = False,
) -> None:
    """Run project."""
    path: Path = get_proj_path(proj)
    wrapper: GodotWrapper = get_godot_wrapper()

    # Auto-update main scene before running
    ensure_main_scene(path)
    ensure_script_attachment(path)

    print_info(f"Running {path.name}...")
    wrapper.run_editor(
        path,
        scene=scene,
        editor=editor,
        debug=debug,
        fullscreen=fullscreen,
        maximized=maximized,
    )


@app.command()
def projects() -> None:
    """List projects."""
    cfg: AppConfig = cfg_mgr.load()
    table = create_projects_table(cfg.projects, cfg.current_project)
    console.print(table)


@app.command()
def switch(name: str) -> None:
    """Switch current project."""
    cfg: AppConfig = cfg_mgr.load()
    if name not in cfg.projects:
        print_error(f"Project '{name}' not found.")
        raise typer.Exit(1)

    cfg.current_project = name
    cfg_mgr.save(cfg)
    print_success(f"Switched to {name}")


@app.command()
def info(proj: Optional[str] = typer.Option(None, "--project", "-p")) -> None:
    """Show project info."""
    path: Path = get_proj_path(proj)
    pf = ProjectGodotFile(path)
    if not pf.exists():
        print_error("No project.godot found.")
        return

    data: dict[str, Optional[Path | str]] = {
        "Name": pf.get_value("application", "config/name"),
        "Main Scene": pf.get_value("application", "run/main_scene"),
        "Renderer": pf.get_value("rendering", "renderer/rendering_method"),
        "Path": path,
    }
    console.print(create_info_table(data))


@app.command()
def export(
    preset: str,
    output: Optional[str] = None,
    proj: Optional[str] = None,
    debug: bool = False,
) -> None:
    """Export project."""
    path: Path = get_proj_path(proj)
    if not output:
        # Infer output path/name
        # Simple default to ./build/
        out_dir = path / "build"
        out_dir.mkdir(exist_ok=True)
        ext = (
            ".exe"
            if "Windows" in preset
            else ".x86_64"
            if "Linux" in preset
            else ".zip"
        )
        output = str(out_dir / f"{path.name}{ext}")

    wrapper: GodotWrapper = get_godot_wrapper()
    print_info(f"Exporting to {output}...")
    try:
        wrapper.export_project(path, preset, Path(output), debug=debug)
        print_success("Export successful.")
    except subprocess.CalledProcessError:
        print_error("Export failed.")
        raise typer.Exit(1)
