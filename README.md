# ZiExpand

**ZiExpand** is a powerful, developer-friendly CLI tool that makes creating [Hacknet](https://store.steampowered.com/app/365450/Hacknet/) Extensions significantly easier — without limiting what you can build.

It scaffolds projects, generates correct XML templates for Nodes, Missions, Actions, Factions and more, validates structure, and keeps the full power of the official extension format in your hands.

> Built for creators who want to spend less time fighting XML boilerplate and more time designing stories, systems and challenges.

## Features

- **One-command project scaffolding** – Creates a complete, ready-to-run extension folder structure with `ExtensionInfo.xml`, `Intro.txt`, and all standard directories.
- **Smart generators** – Quickly generate Nodes, Missions, Conditional Actions, Factions, Themes and HackerScripts with correct structure and helpful comments.
- **Structure validation** – Checks that required files and folders exist and that key XML files are well-formed.
- **Templates based on official docs** – Uses patterns from the official Hacknet Extensions Guide and community best practices.
- **Zero lock-in** – Everything is plain XML. You can edit freely, ignore the tool later, or mix generated and hand-written files.
- **Cross-platform** – Works on Windows, Linux and macOS (Python 3.8+).

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

## Quick Start

```bash
# Create a new extension project
ziexpand new MyAwesomeExtension

cd MyAwesomeExtension

# Generate a computer/node
ziexpand gen node myFirstPC --name "My First Computer" --ip 192.168.1.10 --security 3

# Generate a mission
ziexpand gen mission intro_mission --title "Welcome to the Network"

# Generate starting actions
ziexpand gen action StartingActions

# Validate the project
ziexpand validate
```

Then copy the folder into your Hacknet `Extensions` directory, rename if needed, and launch with the `-enabledebug` flag for faster iteration.

## Commands

| Command | Description |
|---------|-------------|
| `ziexpand new <name>` | Scaffold a full new extension project |
| `ziexpand gen node <id>` | Generate a Node (Computer) XML file |
| `ziexpand gen mission <name>` | Generate a Mission XML file |
| `ziexpand gen action <name>` | Generate a ConditionalActions file |
| `ziexpand gen faction <name>` | Generate a Faction file |
| `ziexpand validate` | Check project structure and basic XML validity |
| `ziexpand info` | Show current project info (if inside an extension) |

Run `ziexpand --help` or `ziexpand <command> --help` for detailed options.

## Project Structure Created by `new`

```
MyAwesomeExtension/
├── ExtensionInfo.xml
├── Intro.txt
├── Logo.png          (placeholder note)
├── Actions/
├── Factions/
├── HackerScripts/
├── Missions/
├── Music/
├── Nodes/
├── People/
├── Themes/
└── Web/
    └── Cache/
```

## Philosophy

ZiExpand accelerates the *boring* parts (folder setup, correct tags, boilerplate) while leaving every advanced feature of the Hacknet extension system completely open. You still write (or edit) the XML yourself for complex logic, custom daemons, sequencers, web content, etc.

It is a **builder’s assistant**, not a black-box generator.

## Requirements

- Python 3.8+
- No external dependencies for core functionality (uses only stdlib)

## Contributing

Pull requests, issue reports and template improvements are welcome!

## License

MIT

## Credits

- Inspired by the official [Hacknet Extensions Guide](https://steamcommunity.com/sharedfiles/filedetails/?id=914587661)
- XML schemas reference: [rquinio/hacknet-xsd](https://github.com/rquinio/hacknet-xsd)
- Community knowledge from the Hacknet Discord and wiki

---

Made with ♥ for the Hacknet extension community.
