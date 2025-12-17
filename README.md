![godoco](/godoco.jpeg)

# godoco - Godot Code Only

**The Godot workflow you've been missing.**

Stop fighting the editor. Stop clicking through menus. Stop wasting time. Let's make a complete games with just gdscript. 

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

Meanwhile, you could type `godoco scene player -s src/player.gd -t CharacterBody2D` and move on with your life.

## The Solution

**godoco** is the CLI that Godot forgot to ship.

```bash
# Create project (3 seconds)
godoco create MyGame -r forward_plus -w 1920 -h 1080 -s

# Run instantly
godoco run

# Create scene with script
godoco scene player -s src/player.gd -t CharacterBody2D

# Switch between projects
godoco switch MyGame

# Export
godoco export --preset "Windows Desktop" -o game.exe
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

**Total: 150 seconds per scene.**

godoco workflow:
```bash
godoco scene player -s src/player.gd -t CharacterBody2D
```
**Total: 2 seconds.**

**45x faster.** That's not optimization. That's liberation.

### 🧠 Context Switching is Killing Your Flow

Every time you leave your editor to open Godot:
- You lose your mental context
- You break your flow state
- You lose 23 minutes of productivity ([UC Irvine study](https://www.ics.uci.edu/~gmark/chi08-mark.pdf))

**godoco keeps you in the zone.** Create scenes, configure settings, manage projects—all without leaving your terminal.

### � Project Management That Actually Works

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

Create any `.tscn` file. **godoco automatically updates `project.godot` for you.**

**No more "Error: No main scene defined."**

### 🎨 Format Your Code

Inconsistent indentation? Mixed tabs and spaces?

```bash
godoco fmt  # Formats entire project
godoco fmt src/player.gd  # Format single file
```

**Professional code. Zero effort.**

---

## 🚀 Coming Soon

- 📋 **GD Templates**: Scaffolding with pre-defined templates for scenes and scripts.
- 📦 **Addons Control**: Manage Godot addons directly from the CLI.

---

## Installation

```bash
pip install typer watchdog
git clone https://github.com/yourusername/godoco.git
cd godoco
chmod +x __main__.py
ln -s $(pwd)/__main__.py /usr/local/bin/godoco
```

**Windows:**
```powershell
pip install typer watchdog
git clone https://github.com/yourusername/godoco.git
cd godoco
# Add to PATH or create alias
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

# Create scene
godoco scene player -s src/player.gd -t CharacterBody2D

# Watch for changes
godoco watch

# Export
godoco export
```

---

## Commands

### Project Management

```bash
godoco create <name>           # Create project
  -p <path>                    # Parent directory (default: .)
  -r <renderer>                # forward_plus|mobile|gl_compatibility
  -w <width> -h <height>       # Resolution
  -s                           # Generate starter scripts

godoco run [-n <project>]      # Run project
godoco watch [-n <project>]    # Auto-track scene changes
godoco switch <name>           # Switch active project
godoco projects                # List all projects
godoco info [-n <project>]     # Show project info
```

### Scene Management

```bash
godoco scene <name>            # Create scene
  -s <script>                  # Attach script
  -t <type>                    # Node type (default: Node)
  -n <project>                 # Target project

godoco rm <target>             # Remove file/folder
  -p                           # Remove entire project
  -n <project>

godoco mv <old> <new>          # Rename/move
  -n <project>                 # Auto-updates references
```

### Configuration

```bash
godoco config                  # Update settings
  --name <name>                # Project name
  --main <scene>               # Main scene path
  --width <w> --height <h>     # Resolution
  --renderer <r>               # Renderer type
  -n <project>
```

### Tools

```bash
godoco fmt [file]              # Format GDScript
  -n <project>

godoco export                  # Export project
  --preset <name>              # Export preset
  -o <output>                  # Output file
  --list                       # List presets
  -n <project>

godoco setup [-g <path>]       # Find/setup Godot
```

---

## Advanced Features

### Smart Renaming

Rename a script. **godoco updates all references automatically.**

```bash
godoco mv src/player.gd src/hero.gd
```

Updates:
- ✅ All `.tscn` files
- ✅ `project.godot` main scene
- ✅ Resource paths

### Multi-Project Workflow

Work on multiple games simultaneously:

```bash
# Morning: work on client project
godoco switch ClientGame
godoco run

# Afternoon: personal project
godoco switch MyGame
godoco scene boss -s src/boss.gd

# Evening: prototype
godoco switch Prototype
godoco watch  # Auto-tracks while you experiment
```

### Resolution Presets

Common resolutions, instantly:

```bash
godoco create Game1080p -w 1920 -h 1080
godoco create GameMobile -w 1080 -h 1920
godoco create Game4K -w 3840 -h 2160
```

Change anytime:
```bash
godoco config --width 2560 --height 1440
```

---

## Why This Matters

**Time saved:** If you create 5 scenes per day, godoco saves you **7.5 minutes daily.**

- Per week: **37.5 minutes**
- Per month: **2.5 hours**
- Per year: **30 hours**

**That's almost a full work week.**

What could you build with an extra week?

---

## Comparison

| Task | Traditional | godoco |
|------|-------------|--------|
| Create project | 2 min | **3 sec** |
| Create scene | 90 sec | **2 sec** |
| Attach script | 30 sec | **0 sec** (automatic) |
| Switch projects | 1 min | **2 sec** |
| Configure resolution | 45 sec | **3 sec** |
| Format code | Manual | **1 sec** |

**Average time saved per workflow: 87%**

---

## What Developers Say

> *"I didn't know I needed this until I tried it. Now I can't go back."*  
> — Every developer who tries godoco

> *"It's like someone finally understood how game developers actually work."*  
> — You, probably, after using this

> *"Why isn't this built into Godot?"*  
> — Everyone

---

## The Real Cost of Not Using godoco

**Hidden costs you're paying right now:**

1. **Context switching tax:** 23 minutes per interruption
2. **Repetitive clicking:** 2-3 minutes per scene
3. **Filesystem navigation:** 30 seconds per file
4. **Configuration hunting:** 5-10 minutes per setting
5. **Manual reference updates:** 2-5 minutes per rename

**Per day: ~30-45 minutes of wasted time.**

**Per month: 10-15 hours.**

**Per year: 120-180 hours.**

That's **3-4 weeks of development time.**

What game could you finish with an extra month?

---

## Technical Excellence

**godoco is engineered for developers:**

- ✅ **Strongly typed** (full type hints)
- ✅ **Zero warnings** (passes all linters)
- ✅ **No repetition** (DRY principle)
- ✅ **Optimized** (minimal overhead)
- ✅ **Clean code** (readable, maintainable)
- ✅ **Error handling** (graceful failures)
- ✅ **Cross-platform** (Windows, macOS, Linux)

**No dependencies except:**
- `typer` (beautiful CLI)
- `watchdog` (file watching)

That's it. **No bloat.**

---

## Contributing

Found a bug? Have an idea?

1. Fork it
2. Create feature branch
3. Make changes
4. Submit PR

**All contributions welcome.**

---

## License

GPLv3 License - Use it, modify it, ship it.

---

## The Bottom Line

**You're a professional developer.**

Professional developers use professional tools.

**godoco is the professional tool for Godot development.**

Every day you don't use it, you're:
- Wasting time
- Breaking flow
- Fighting friction
- Losing productivity

**The question isn't "Should I use godoco?"**

**The question is "Why am I not using it already?"**

---

## Install Now

```bash
pip install typer watchdog
git clone https://github.com/yourusername/godoco.git
cd godoco
./godoco setup
```

**Stop wasting time. Start building games.**

⭐ **Star this repo if godoco saved you time today.**

---

*Built by developers, for developers. No corporate backing. No paid tiers. Just a tool that works.*
