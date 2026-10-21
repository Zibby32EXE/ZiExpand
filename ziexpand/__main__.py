"""Entry point so the package can be run as `python -m ziexpand` or frozen as an .exe."""

from __future__ import annotations

import sys


def main() -> int:
    # If no arguments are given when running the frozen .exe, launch the GUI.
    # This makes double-clicking ZiExpand.exe open the interface directly.
    if getattr(sys, "frozen", False) and len(sys.argv) == 1:
        from ziexpand.gui import run_gui
        run_gui()
        return 0

    from ziexpand.cli import main as cli_main
    return cli_main()


if __name__ == "__main__":
    sys.exit(main())
