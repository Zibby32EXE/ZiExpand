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

## Installation

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

## Quick Start

### GUI (recommended for most users)

```bash
ziexpand gui
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

- Python 3.8+
- Tkinter (for the GUI – standard with most Python builds)
- No third-party packages required

## License

MIT

## Credits

- Official [Hacknet Extensions Guide](https://steamcommunity.com/sharedfiles/filedetails/?id=914587661)
- XML schemas: [rquinio/hacknet-xsd](https://github.com/rquinio/hacknet-xsd)
- Community knowledge from the Hacknet Discord & wiki

---

Made with ♥ for the Hacknet extension community.
