"""Enhanced validation for Hacknet Extensions."""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from .project import ExtensionProject


@dataclass
class ValidationIssue:
    level: str  # "error" | "warning" | "info"
    message: str
    file: str = ""


@dataclass
class ValidationResult:
    issues: List[ValidationIssue] = field(default_factory=list)

    @property
    def errors(self) -> List[ValidationIssue]:
        return [i for i in self.issues if i.level == "error"]

    @property
    def warnings(self) -> List[ValidationIssue]:
        return [i for i in self.issues if i.level == "warning"]

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0


def _rel(root: Path, p: Path) -> str:
    try:
        return str(p.relative_to(root))
    except ValueError:
        return str(p)


def validate_project(proj: ExtensionProject) -> ValidationResult:
    """Run a full validation suite on the project."""
    result = ValidationResult()
    root = proj.root

    # --- ExtensionInfo.xml ---
    info = proj.info_path
    if not info.is_file():
        result.issues.append(ValidationIssue("error", "Missing ExtensionInfo.xml"))
        return result

    try:
        tree = ET.parse(info)
        elem = tree.getroot()
        if elem.tag != "HacknetExtension":
            result.issues.append(
                ValidationIssue("error", "Root tag must be <HacknetExtension>", "ExtensionInfo.xml")
            )
        for required in ("Name", "Language"):
            if elem.find(required) is None:
                result.issues.append(
                    ValidationIssue("warning", f"Missing recommended tag <{required}>", "ExtensionInfo.xml")
                )
        # Check starting mission exists
        sm = elem.findtext("StartingMission")
        if sm and sm.upper() != "NONE":
            sm_path = root / sm
            if not sm_path.is_file():
                result.issues.append(
                    ValidationIssue("error", f"StartingMission points to missing file: {sm}", "ExtensionInfo.xml")
                )
        sa = elem.findtext("StartingActions")
        if sa and sa.upper() != "NONE":
            sa_path = root / sa
            if not sa_path.is_file():
                result.issues.append(
                    ValidationIssue("warning", f"StartingActions points to missing file: {sa}", "ExtensionInfo.xml")
                )
    except ET.ParseError as e:
        result.issues.append(
            ValidationIssue("error", f"ExtensionInfo.xml is not well-formed: {e}", "ExtensionInfo.xml")
        )

    # --- Standard folders ---
    for folder in ("Actions", "Factions", "HackerScripts", "Missions", "Music",
                   "Nodes", "People", "Themes", "Web"):
        if not (root / folder).is_dir():
            result.issues.append(ValidationIssue("warning", f"Missing recommended folder: {folder}/"))

    # --- Collect known node ids ---
    node_ids = set()
    for npath in proj.nodes:
        try:
            ntree = ET.parse(npath)
            nid = ntree.getroot().get("id")
            if nid:
                node_ids.add(nid)
            else:
                result.issues.append(
                    ValidationIssue("warning", "Computer missing id attribute", _rel(root, npath))
                )
        except ET.ParseError as e:
            result.issues.append(
                ValidationIssue("error", f"Not well-formed XML: {e}", _rel(root, npath))
            )

    # --- Validate missions ---
    for mpath in proj.missions:
        try:
            mtree = ET.parse(mpath)
            mroot = mtree.getroot()
            if mroot.tag.lower() != "mission":
                result.issues.append(
                    ValidationIssue("warning", "Root tag should be <mission>", _rel(root, mpath))
                )
            # nextMission reference
            next_m = mroot.findtext("nextMission")
            if next_m and next_m.strip().upper() != "NONE":
                next_path = root / next_m.strip()
                if not next_path.is_file():
                    result.issues.append(
                        ValidationIssue(
                            "warning",
                            f"nextMission points to missing file: {next_m.strip()}",
                            _rel(root, mpath),
                        )
                    )
            # Check goals for target nodes that don't exist
            for goal in mroot.findall(".//goal"):
                target = goal.get("target")
                if target and target not in node_ids and not target.startswith("#"):
                    result.issues.append(
                        ValidationIssue(
                            "info",
                            f"Goal references unknown node id '{target}' (may be intentional)",
                            _rel(root, mpath),
                        )
                    )
        except ET.ParseError as e:
            result.issues.append(
                ValidationIssue("error", f"Not well-formed XML: {e}", _rel(root, mpath))
            )

    # --- Actions & Factions well-formedness ---
    for collection, label in (
        (proj.actions, "Actions"),
        (proj.factions, "Factions"),
        (proj.themes, "Themes"),
        (proj.people, "People"),
    ):
        for fpath in collection:
            try:
                ET.parse(fpath)
            except ET.ParseError as e:
                result.issues.append(
                    ValidationIssue("error", f"Not well-formed XML: {e}", _rel(root, fpath))
                )

    # --- Duplicate node ids ---
    seen = {}
    for npath in proj.nodes:
        try:
            nid = ET.parse(npath).getroot().get("id")
            if nid:
                if nid in seen:
                    result.issues.append(
                        ValidationIssue(
                            "error",
                            f"Duplicate node id '{nid}' (also in {seen[nid]})",
                            _rel(root, npath),
                        )
                    )
                else:
                    seen[nid] = _rel(root, npath)
        except ET.ParseError:
            pass

    if not result.issues:
        result.issues.append(ValidationIssue("info", "No issues found – project looks healthy."))

    return result
