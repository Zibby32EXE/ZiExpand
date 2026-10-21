# ZiExpand

**ZiExpand** is a developer-friendly tool that makes creating [Hacknet](https://store.steampowered.com/app/365450/Hacknet/) Extensions significantly easier — without limiting what you can build.

It provides both a **command-line interface** and a full **graphical UI**, scaffolds complete projects, generates correct XML/HTML/templates for every major content type, validates structure & references, and keeps the full power of the official extension format in your hands.

> Spend less time fighting boilerplate and more time designing stories, systems and challenges.

## Features (v0.2)

### Core
- **One-command scaffolding** – Full extension folder structure + starter files
- **Rich generators** for:
  - Nodes (Computers)
  - Missions
  - Conditional Actions
  - Factions
  - Themes
  - People database entries
  - HackerScripts
  - Web pages (XHTML suitable for Hacknet)
- **Enhanced validation** – XML well-formedness, missing files, duplicate node IDs, broken `nextMission` / `StartingMission` references, unknown goal targets, etc.
- **Zero lock-in** – Everything is plain editable XML/TXT/HTML

### Graphical UI (`ziexpand gui`)
- Project browser with live tree of Nodes / Missions / Actions / …
- Built-in code editor (with save)
- One-click generation of any content type
- One-click validation with detailed report window
- Open project folder in system file manager
- New / Open project dialogs
- Keyboard shortcuts (Ctrl+N / Ctrl+O / Ctrl+S)

### CLI
- Full feature parity for scripting and automation
- Works great in CI or from the terminal

### Standalone Windows `.exe`
- Build a single-file executable that runs without installing Python
- Double-click opens the GUI; CLI arguments still work

## Installation

### Option A – Python package (any OS)

```bash
pip install git+https://github.com/Zibby32EXE/ZiExpand.git
```

Or clone and install in editable mode:

```bash
git clone https://github.com/Zibby32EXE/ZiExpand.git
cd ZiExpand
pip install -e .
```

Requires **Python 3.8+**. The GUI needs Tkinter (included with most Python installations).

### Option B – Windows executable (no Python needed)

1. Download `ZiExpand.exe` from the [Releases](https://github.com/Zibby32EXE/ZiExpand/releases) page (when available), **or**
2. Build it yourself (see below).

Double-click `ZiExpand.exe` to open the GUI. You can also run it from a terminal with CLI arguments:

```text
ZiExpand.exe new MyExtension
ZiExpand.exe gui
ZiExpand.exe validate
```

## Building the Windows `.exe`

### Easiest (Windows)

1. Clone the repo and open a command prompt in the project folder.
2. Double-click **`build.bat`** (or run it from cmd).
3. When it finishes, the executable is at:

```text
dist\ZiExpand.exe
```

### Cross-platform / scripted

```bash
python build.py
```

This installs PyInstaller if needed and produces `dist/ZiExpand.exe` (Windows) or `dist/ZiExpand` (Linux/macOS).

### Manual PyInstaller

```bash
pip install pyinstaller
pyinstaller --noconfirm ziexpand.spec
```

### Automatic builds (GitHub Actions)

The workflow `.github/workflows/build-exe.yml` builds the Windows executable on every version tag (`v*`) and on manual dispatch. The `.exe` is uploaded as an artifact and attached to the GitHub Release.

## Quick Start

### GUI (recommended for most users)

```bash
ziexpand gui
# or just double-click ZiExpand.exe
```

Then use **File → New Extension…** or **Open Extension…** and start generating content from the **Generate** menu.

### CLI

```bash
# Create a new extension
ziexpand new MyAwesomeExtension
cd MyAwesomeExtension

# Generate content
ziexpand gen node gateway --name "Gateway Server" --security 4 --ports "22,21,25,80,443"
ziexpand gen mission intro --title "First Contact"
ziexpand gen action SetupActions
ziexpand gen faction CorpX --display "Corporation X"
ziexpand gen theme darknet
ziexpand gen person alice --display "Alice Johnson"
ziexpand gen hackerscript recon
ziexpand gen web index

# Check everything
ziexpand validate
ziexpand info
```

Copy the finished folder into your Hacknet `Extensions` directory and launch the game with `-enabledebug` for fast iteration.

## Commands Overview

| Command | Description |
|---------|-------------|
| `ziexpand new <name>` | Scaffold a full new extension |
| `ziexpand gui` | Launch the graphical interface |
| `ziexpand gen node <id>` | Generate a Computer/Node |
| `ziexpand gen mission <name>` | Generate a Mission |
| `ziexpand gen action <name>` | Generate ConditionalActions |
| `ziexpand gen faction <name>` | Generate a Faction |
| `ziexpand gen theme <name>` | Generate a Theme |
| `ziexpand gen person <name>` | Generate a People entry |
| `ziexpand gen hackerscript <name>` | Generate a HackerScript |
| `ziexpand gen web [name]` | Generate a Web page |
| `ziexpand validate` | Deep project validation |
| `ziexpand info` | Show project summary |

Run `ziexpand <command> --help` for options.

## Project Structure

```
MyAwesomeExtension/
├── ExtensionInfo.xml
├── Intro.txt
├── Logo.png.placeholder
├── Actions/
├── Factions/
├── HackerScripts/
├── Missions/
├── Music/
├── Nodes/
├── People/
├── Themes/
└── Web/
    └── Cache/          ← put CSS & images here
```

## Philosophy

ZiExpand is a **builder’s assistant**, not a black-box generator. It removes the tedious setup and gives you correct, commented templates so you can focus on design. Every advanced feature of the official Hacknet extension system remains fully available.

## Requirements

- **Python mode:** Python 3.8+ and Tkinter (standard with most Python builds)
- **.exe mode:** Windows 10/11 – no Python required
- No third-party packages required at runtime

## License

MIT

## Credits

- Official [Hacknet Extensions Guide](https://steamcommunity.com/sharedfiles/filedetails/?id=914587661)
- XML schemas: [rquinio/hacknet-xsd](https://github.com/rquinio/hacknet-xsd)
- Community knowledge from the Hacknet Discord & wiki

---

Made with ♥ for the Hacknet extension community.
