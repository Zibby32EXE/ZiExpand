# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for ZiExpand
# Build with: pyinstaller ziexpand.spec

block_cipher = None

a = Analysis(
    ['ziexpand/__main__.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'ziexpand',
        'ziexpand.cli',
        'ziexpand.gui',
        'ziexpand.generators',
        'ziexpand.project',
        'ziexpand.validator',
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.simpledialog',
        'tkinter.scrolledtext',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ZiExpand',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,          # GUI mode (no console window)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,              # Optional: add icon='assets/icon.ico'
)
