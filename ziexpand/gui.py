"""Tkinter-based graphical interface for ZiExpand."""

from __future__ import annotations

import os
import subprocess
import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext, simpledialog, ttk
from typing import Optional

from . import __version__
from .generators import (
    generate_action,
    generate_faction,
    generate_hackerscript,
    generate_mission,
    generate_node,
    generate_person,
    generate_theme,
    generate_web_page,
)
from .project import ExtensionProject, ensure_standard_folders, load_project
from .validator import validate_project


class ZiExpandGUI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(f"ZiExpand {__version__} – Hacknet Extension Builder")
        self.geometry("1100x700")
        self.minsize(900, 550)

        self.project: Optional[ExtensionProject] = None
        self.current_file: Optional[Path] = None

        self._build_menu()
        self._build_ui()
        self._set_status("Ready – open or create a project to begin.")

        # Try auto-load if started inside an extension
        proj = load_project()
        if proj:
            self._load_project(proj)

    # ------------------------------------------------------------------ UI
    def _build_menu(self) -> None:
        menubar = tk.Menu(self)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Extension…", command=self._new_project, accelerator="Ctrl+N")
        file_menu.add_command(label="Open Extension…", command=self._open_project, accelerator="Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label="Save File", command=self._save_current, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.destroy)
        menubar.add_cascade(label="File", menu=file_menu)

        gen_menu = tk.Menu(menubar, tearoff=0)
        gen_menu.add_command(label="Node (Computer)…", command=lambda: self._generate("node"))
        gen_menu.add_command(label="Mission…", command=lambda: self._generate("mission"))
        gen_menu.add_command(label="Action Set…", command=lambda: self._generate("action"))
        gen_menu.add_command(label="Faction…", command=lambda: self._generate("faction"))
        gen_menu.add_command(label="Theme…", command=lambda: self._generate("theme"))
        gen_menu.add_command(label="Person…", command=lambda: self._generate("person"))
        gen_menu.add_command(label="HackerScript…", command=lambda: self._generate("hackerscript"))
        gen_menu.add_command(label="Web Page…", command=lambda: self._generate("web"))
        menubar.add_cascade(label="Generate", menu=gen_menu)

        tools_menu = tk.Menu(menubar, tearoff=0)
        tools_menu.add_command(label="Validate Project", command=self._run_validate)
        tools_menu.add_command(label="Refresh Tree", command=self._refresh_tree)
        tools_menu.add_command(label="Open in File Manager", command=self._open_in_explorer)
        tools_menu.add_command(label="Ensure Standard Folders", command=self._ensure_folders)
        menubar.add_cascade(label="Tools", menu=tools_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self._about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menubar)

        self.bind_all("<Control-n>", lambda e: self._new_project())
        self.bind_all("<Control-o>", lambda e: self._open_project())
        self.bind_all("<Control-s>", lambda e: self._save_current())

    def _build_ui(self) -> None:
        # Main paned window
        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        # Left: project tree
        left = ttk.Frame(paned, width=260)
        paned.add(left, weight=1)

        ttk.Label(left, text="Project", font=("", 10, "bold")).pack(anchor=tk.W, pady=(0, 2))
        self.tree = ttk.Treeview(left, show="tree", selectmode="browse")
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)
        self.tree.bind("<Double-1>", self._on_tree_double)

        # Right: editor + status
        right = ttk.Frame(paned)
        paned.add(right, weight=3)

        self.file_label = ttk.Label(right, text="No file open", font=("", 9))
        self.file_label.pack(anchor=tk.W)

        self.editor = scrolledtext.ScrolledText(
            right, wrap=tk.NONE, font=("Consolas", 10), undo=True
        )
        self.editor.pack(fill=tk.BOTH, expand=True, pady=(2, 0))

        # Bottom toolbar
        toolbar = ttk.Frame(right)
        toolbar.pack(fill=tk.X, pady=4)
        ttk.Button(toolbar, text="Save", command=self._save_current).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Validate", command=self._run_validate).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Refresh", command=self._refresh_tree).pack(side=tk.LEFT, padx=2)

        # Status bar
        self.status = ttk.Label(self, text="", relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(fill=tk.X, side=tk.BOTTOM)

    # ------------------------------------------------------------------ Project loading
    def _load_project(self, proj: ExtensionProject) -> None:
        self.project = proj
        self.current_file = None
        self.editor.delete("1.0", tk.END)
        self.file_label.config(text="No file open")
        self._refresh_tree()
        self.title(f"ZiExpand – {proj.name or proj.root.name}")
        self._set_status(f"Loaded: {proj.root}")

    def _new_project(self) -> None:
        name = simpledialog.askstring("New Extension", "Extension folder name:", parent=self)
        if not name:
            return
        name = name.strip()
        target = Path(name)
        if target.exists():
            messagebox.showerror("Error", f"Directory '{name}' already exists.")
            return

        # Ask where to create it
        parent = filedialog.askdirectory(title="Choose parent folder for the new extension")
        if not parent:
            return
        target = Path(parent) / name
        if target.exists():
            messagebox.showerror("Error", f"'{target}' already exists.")
            return

        from .generators import generate_action, generate_extension_info, generate_intro, generate_mission

        target.mkdir(parents=True)
        ensure_standard_folders(target)
        (target / "ExtensionInfo.xml").write_text(generate_extension_info(name), encoding="utf-8")
        (target / "Intro.txt").write_text(generate_intro(name), encoding="utf-8")
        (target / "Actions" / "StartingActions.xml").write_text(
            generate_action("StartingActions"), encoding="utf-8"
        )
        (target / "Missions" / "StartingMission.xml").write_text(
            generate_mission("StartingMission", title="Getting Started"), encoding="utf-8"
        )
        (target / "Logo.png.placeholder").write_text(
            "Replace with Logo.png and delete this file.\n", encoding="utf-8"
        )

        proj = load_project(target)
        if proj:
            self._load_project(proj)
            messagebox.showinfo("Created", f"New extension created at:\n{target}")

    def _open_project(self) -> None:
        path = filedialog.askdirectory(title="Select Extension folder (contains ExtensionInfo.xml)")
        if not path:
            return
        proj = load_project(Path(path))
        if proj is None:
            messagebox.showerror("Error", "No ExtensionInfo.xml found in that folder.")
            return
        self._load_project(proj)

    # ------------------------------------------------------------------ Tree
    def _refresh_tree(self) -> None:
        self.tree.delete(*self.tree.get_children())
        if not self.project:
            return
        self.project.reload()
        root_id = self.tree.insert("", "end", text=self.project.root.name, open=True, values=[str(self.project.root)])

        categories = [
            ("ExtensionInfo.xml", [self.project.info_path] if self.project.info_path.is_file() else []),
            ("Intro.txt", [self.project.root / "Intro.txt"] if (self.project.root / "Intro.txt").is_file() else []),
            ("Nodes", self.project.nodes),
            ("Missions", self.project.missions),
            ("Actions", self.project.actions),
            ("Factions", self.project.factions),
            ("Themes", self.project.themes),
            ("People", self.project.people),
            ("HackerScripts", self.project.hackerscripts),
        ]
        for label, files in categories:
            if not files and label not in ("ExtensionInfo.xml", "Intro.txt"):
                # still show empty categories so user knows they exist
                cat = self.tree.insert(root_id, "end", text=f"{label} (0)", open=False)
                continue
            cat = self.tree.insert(root_id, "end", text=f"{label} ({len(files)})", open=True)
            for f in files:
                self.tree.insert(cat, "end", text=f.name, values=[str(f)])

    def _on_tree_select(self, _event=None) -> None:
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0], "values")
        if not vals:
            return
        path = Path(vals[0])
        if path.is_file():
            self._open_file(path)

    def _on_tree_double(self, _event=None) -> None:
        self._on_tree_select()

    def _open_file(self, path: Path) -> None:
        try:
            content = path.read_text(encoding="utf-8")
        except Exception as e:
            messagebox.showerror("Error", f"Could not read file:\n{e}")
            return
        self.current_file = path
        self.editor.delete("1.0", tk.END)
        self.editor.insert("1.0", content)
        self.file_label.config(text=str(path.relative_to(self.project.root)) if self.project else str(path))
        self._set_status(f"Opened {path.name}")

    def _save_current(self) -> None:
        if not self.current_file:
            messagebox.showinfo("Save", "No file is currently open.")
            return
        try:
            content = self.editor.get("1.0", tk.END)
            # remove trailing extra newline that ScrolledText adds
            if content.endswith("\n"):
                content = content[:-1]
            self.current_file.write_text(content, encoding="utf-8")
            self._set_status(f"Saved {self.current_file.name}")
            if self.project:
                self.project.reload()
        except Exception as e:
            messagebox.showerror("Error", f"Could not save:\n{e}")

    # ------------------------------------------------------------------ Generators
    def _generate(self, kind: str) -> None:
        if not self.project:
            messagebox.showwarning("No project", "Open or create an extension first.")
            return

        if kind == "node":
            nid = simpledialog.askstring("New Node", "Node id (no spaces):", parent=self)
            if not nid:
                return
            name = simpledialog.askstring("New Node", "Display name:", initialvalue=nid, parent=self) or nid
            content = generate_node(nid, name=name)
            out = self.project.root / "Nodes" / f"{nid}.xml"
        elif kind == "mission":
            name = simpledialog.askstring("New Mission", "Mission file name (without .xml):", parent=self)
            if not name:
                return
            title = simpledialog.askstring("New Mission", "Title:", initialvalue=name, parent=self) or name
            content = generate_mission(name, title=title)
            out = self.project.root / "Missions" / f"{name}.xml"
        elif kind == "action":
            name = simpledialog.askstring("New Action Set", "Name:", parent=self)
            if not name:
                return
            content = generate_action(name)
            out = self.project.root / "Actions" / f"{name}.xml"
        elif kind == "faction":
            name = simpledialog.askstring("New Faction", "Faction id:", parent=self)
            if not name:
                return
            content = generate_faction(name)
            out = self.project.root / "Factions" / f"{name}.xml"
        elif kind == "theme":
            name = simpledialog.askstring("New Theme", "Theme name:", parent=self)
            if not name:
                return
            content = generate_theme(name)
            out = self.project.root / "Themes" / f"{name}.xml"
        elif kind == "person":
            name = simpledialog.askstring("New Person", "Person id:", parent=self)
            if not name:
                return
            content = generate_person(name)
            out = self.project.root / "People" / f"{name}.xml"
        elif kind == "hackerscript":
            name = simpledialog.askstring("New HackerScript", "Script name (without .txt):", parent=self)
            if not name:
                return
            content = generate_hackerscript(name)
            out = self.project.root / "HackerScripts" / f"{name}.txt"
        elif kind == "web":
            name = simpledialog.askstring("New Web Page", "Page name (without .html):", parent=self) or "index"
            content = generate_web_page(name)
            out = self.project.root / "Web" / f"{name}.html"
        else:
            return

        if out.exists():
            if not messagebox.askyesno("Overwrite?", f"{out.name} already exists. Overwrite?"):
                return
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")
        self._refresh_tree()
        self._open_file(out)
        self._set_status(f"Generated {out.relative_to(self.project.root)}")

    # ------------------------------------------------------------------ Tools
    def _run_validate(self) -> None:
        if not self.project:
            messagebox.showwarning("No project", "Open a project first.")
            return
        self.project.reload()
        result = validate_project(self.project)

        win = tk.Toplevel(self)
        win.title("Validation Results")
        win.geometry("650x400")
        txt = scrolledtext.ScrolledText(win, wrap=tk.WORD, font=("Consolas", 10))
        txt.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        for issue in result.issues:
            prefix = {"error": "[ERROR]  ", "warning": "[WARN]   ", "info": "[INFO]   "}.get(issue.level, "")
            line = f"{prefix}{issue.message}"
            if issue.file:
                line += f"  ({issue.file})"
            txt.insert(tk.END, line + "\n")
        txt.configure(state=tk.DISABLED)

        if result.ok:
            self._set_status("Validation passed.")
        else:
            self._set_status(f"Validation finished – {len(result.errors)} error(s).")

    def _ensure_folders(self) -> None:
        if not self.project:
            return
        ensure_standard_folders(self.project.root)
        self._refresh_tree()
        self._set_status("Standard folders ensured.")

    def _open_in_explorer(self) -> None:
        if not self.project:
            return
        path = self.project.root
        try:
            if sys.platform == "win32":
                os.startfile(path)
            elif sys.platform == "darwin":
                subprocess.run(["open", path], check=False)
            else:
                subprocess.run(["xdg-open", path], check=False)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _about(self) -> None:
        messagebox.showinfo(
            "About ZiExpand",
            f"ZiExpand {__version__}\n\n"
            "A friendly builder for Hacknet Extensions.\n"
            "Scaffold, generate, edit and validate – while keeping full creative control.\n\n"
            "https://github.com/Zibby32EXE/ZiExpand",
        )

    def _set_status(self, text: str) -> None:
        self.status.config(text=f"  {text}")


def run_gui() -> None:
    app = ZiExpandGUI()
    app.mainloop()
