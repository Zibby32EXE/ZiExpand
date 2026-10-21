#!/usr/bin/env python3
"""Build a standalone ZiExpand executable with PyInstaller."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SPEC = ROOT / "ziexpand.spec"
DIST = ROOT / "dist"


def main() -> int:
    print("[ZiExpand] Ensuring PyInstaller is installed...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pyinstaller"])

    if not SPEC.is_file():
        print(f"ERROR: {SPEC} not found.", file=sys.stderr)
        return 1

    print("[ZiExpand] Building executable (this may take a minute)...")
    subprocess.check_call([
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        str(SPEC),
    ])

    exe_name = "ZiExpand.exe" if sys.platform == "win32" else "ZiExpand"
    out = DIST / exe_name
    if out.is_file():
        size_mb = out.stat().st_size / (1024 * 1024)
        print()
        print("=" * 50)
        print(f"  Build succeeded!")
        print(f"  Output : {out}")
        print(f"  Size   : {size_mb:.1f} MB")
        print("=" * 50)
        print()
        print("Double-click the executable to open the GUI.")
        print("You can also pass CLI args, e.g.:")
        print(f"  {exe_name} new MyExtension")
        print(f"  {exe_name} gui")
        return 0

    print("ERROR: Expected output file was not created.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
