![godoco](/godoco.jpeg)

# godoco - Godot Code Only

**The Godot workflow you've been missing.**

Stop fighting the editor. Stop clicking through menus. Stop wasting time. Let's make complete games with just gdscript. 

[Installation](#installation) • [Quick Start](#quick-start) • [Commands](#commands) • [Why](#why-godoco)

---

## The Problem

You're a developer. You live in the terminal. You automate everything.

**Except your game development.**

Every time you need to create a scene, you:
- Open the Godot editor
- Wait for it to load
- Click through the filesystem
- Right-click, select "New Scene"
- Configure node types
- Attach scripts manually
- Save, close, repeat

**Five minutes. Gone.** Twenty times a day. That's **100 minutes of pure friction.**

## The Solution

**godoco** is the CLI that Godot forgot to ship.

```bash
# Create project (3 seconds)
godoco create MyGame -r forward_plus -s

# Run instantly
godoco run

# Open in editor
godoco run --editor

# Switch between projects
godoco switch MyGame

# Export
godoco export "Windows Desktop" -o build/game.exe
```

**No editor. No clicks. Just gdscript code.**

---

## Why godoco?

### ⚡ Speed

Traditional workflow:
1. Open editor: **15s**
2. Wait for loading: **10s-60s**
2. Navigate filesystem: **10s**
3. Create scene: **20s**
4. Attach script: **15s**
5. Configure properties: **30s**

**Total: 150 seconds per project setup.**

godoco workflow:
```bash
godoco create MyGame -s
```
**Total: 2 seconds.**

**45x faster.** That's not optimization. That's liberation.

### 🧠 Context Switching is Killing Your Flow

Every time you leave your editor to open Godot:
- You lose your mental context
- You break your flow state
- You lose 23 minutes of productivity ([UC Irvine study](https://www.ics.uci.edu/~gmark/chi08-mark.pdf))

**godoco keeps you in the zone.** Configure settings, manage projects—all without leaving your terminal.

### 🔄 Project Management That Actually Works

Remember that other project you started last week? Where is it?

```bash
# godoco remembers everything
godoco projects
→ MyGame: /home/user/games/MyGame
  Prototype: /home/user/prototypes/Prototype
  ClientWork: /home/user/work/ClientWork

# Switch instantly
godoco switch Prototype
godoco run  # Runs Prototype immediately
```

**No more hunting through directories.** Your projects are always one command away.

### 🎯 Zero Configuration

Other tools make you:
- Edit YAML files
- Configure build scripts
- Set up directory structures
- Manually track dependencies

**godoco does all of this automatically.**

```bash
godoco create MyGame
```

You get:
- ✅ Proper folder structure (`src/`, `assets/`, `addons/`)
- ✅ Git configuration (`.gitignore`, `.gitattributes`)
- ✅ Project settings with **inline documentation**
- ✅ Icon and imports
- ✅ Automatic project tracking

**Everything. Just. Works.**

### 📝 Self-Documenting

Every setting in `project.godot` is documented:

```ini
[display]
window/size/viewport_width=1280  # Window width in pixels
window/size/viewport_height=720  # Window height in pixels
window/stretch/mode="canvas_items"  # Scale mode: disabled|canvas_items|viewport

[rendering]
renderer/rendering_method="forward_plus"  # forward_plus|mobile|gl_compatibility
```

**No more Googling "what does physics_jitter_fix do?"** It's right there.

---

## 🚀 Coming Soon

- 📋 **GD Templates**: Scaffolding with pre-defined templates for scenes and scripts.
- 📦 **Addons Control**: Manage Godot addons directly from the CLI.
- 🎬 **Scene Creation**: `godoco scene <name>` to create scenes with scripts attached.
- 🔍 **Auto-Tracking**: `godoco watch` to automatically update `project.godot` when files change.
- 🎨 **Code Formatting**: `godoco fmt` for consistent GDScript indentation.

---

## Installation

```bash
pip install .
```

---

## Quick Start

```bash
# Setup (one time)
godoco setup

# Create project
godoco create MyGame -s

# Run
cd MyGame
godoco run
```

---

## Commands

### Project Management

```bash
godoco create [name]           # Create project (Interactive if name omitted)
  -p <path>                    # Parent directory (default: .)
  -r <renderer>                # forward_plus|mobile|gl_compatibility
  -s                           # Generate starter scripts

godoco run                     # Run active project
  --editor                     # Open in Godot editor
  --scene <path>               # Run specific scene
  --debug                      # Run with debug flags
  --fullscreen                 # Run in fullscreen
  --maximized                  # Run maximized

godoco projects                # List all tracked projects
godoco switch <name>           # Switch active project
godoco info                    # Show project info (Renderer, Main Scene, etc.)
```

### Export

```bash
godoco export <preset>         # Export project
  -o <output>                  # Output file
  --debug                      # Export with debug flags
```

### Configuration

```bash
godoco setup                   # Find/setup Godot (Auto-detects)
  --path <path>                # Manually specify Godot executable
```

---

## Multi-Project Workflow

Work on multiple games simultaneously:

```bash
# Morning: work on client project
godoco switch ClientGame
godoco run

# Afternoon: personal project
godoco switch MyGame
godoco run --editor
```

---

## why This Matters

**godoco saves you precious development time by automating boilerplate tasks and keeping you in your favorite editor.**

---

## Technical Excellence

**godoco is engineered for developers:**

- ✅ **Strongly typed** (full type hints)
- ✅ **Zero dependencies** (minimal overhead, use `uv` or `pip`)
- ✅ **Clean code** (readable, maintainable)
- ✅ **Cross-platform** (Windows, macOS, Linux)

---

## License

GPLv3 License - Use it, modify it, ship it.

---

⭐ **Star this repo if godoco saved you time today.**

---

*Built by developers, for developers. Just a tool that works.*
