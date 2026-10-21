"""Project discovery and management helpers for ZiExpand."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class ExtensionProject:
    root: Path
    name: str = ""
    language: str = "en-us"
    description: str = ""
    starting_mission: str = ""
    starting_actions: str = ""
    nodes: List[Path] = field(default_factory=list)
    missions: List[Path] = field(default_factory=list)
    actions: List[Path] = field(default_factory=list)
    factions: List[Path] = field(default_factory=list)
    themes: List[Path] = field(default_factory=list)
    people: List[Path] = field(default_factory=list)
    hackerscripts: List[Path] = field(default_factory=list)

    @property
    def info_path(self) -> Path:
        return self.root / "ExtensionInfo.xml"

    def reload(self) -> None:
        """Re-scan the project directory and parse ExtensionInfo.xml."""
        self.nodes = sorted((self.root / "Nodes").glob("*.xml")) if (self.root / "Nodes").is_dir() else []
        self.missions = sorted((self.root / "Missions").rglob("*.xml")) if (self.root / "Missions").is_dir() else []
        self.actions = sorted((self.root / "Actions").glob("*.xml")) if (self.root / "Actions").is_dir() else []
        self.factions = sorted((self.root / "Factions").glob("*.xml")) if (self.root / "Factions").is_dir() else []
        self.themes = sorted((self.root / "Themes").glob("*.xml")) if (self.root / "Themes").is_dir() else []
        self.people = sorted((self.root / "People").glob("*.xml")) if (self.root / "People").is_dir() else []
        self.hackerscripts = sorted((self.root / "HackerScripts").glob("*.txt")) if (self.root / "HackerScripts").is_dir() else []

        if self.info_path.is_file():
            try:
                tree = ET.parse(self.info_path)
                root = tree.getroot()
                self.name = root.findtext("Name", default="") or ""
                self.language = root.findtext("Language", default="en-us") or "en-us"
                self.description = (root.findtext("Description") or "").strip()
                self.starting_mission = root.findtext("StartingMission", default="") or ""
                self.starting_actions = root.findtext("StartingActions", default="") or ""
            except ET.ParseError:
                pass


def find_extension_root(start: Optional[Path] = None) -> Optional[Path]:
    """Walk upwards looking for ExtensionInfo.xml."""
    current = (start or Path.cwd()).resolve()
    for path in [current, *current.parents]:
        if (path / "ExtensionInfo.xml").is_file():
            return path
    return None


def load_project(path: Optional[Path] = None) -> Optional[ExtensionProject]:
    """Load an ExtensionProject from a path (or cwd)."""
    root = find_extension_root(path)
    if root is None:
        return None
    proj = ExtensionProject(root=root)
    proj.reload()
    return proj


def ensure_standard_folders(root: Path) -> None:
    """Create the standard Hacknet extension folders if missing."""
    folders = [
        "Actions", "Factions", "HackerScripts", "Missions",
        "Music", "Nodes", "People", "Themes", "Web", "Web/Cache",
    ]
    for folder in folders:
        (root / folder).mkdir(parents=True, exist_ok=True)
