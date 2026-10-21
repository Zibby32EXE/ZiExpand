@echo off
REM ============================================================
REM  ZiExpand – Build standalone Windows executable
REM ============================================================
REM  Requirements: Python 3.8+ and pip
REM  Usage:  double-click this file  OR  run  build.bat  in cmd
REM ============================================================

setlocal
cd /d "%~dp0"

echo.
echo  [ZiExpand] Installing / upgrading PyInstaller...
pip install --upgrade pyinstaller
if errorlevel 1 (
    echo  ERROR: pip install failed. Is Python on your PATH?
    pause
    exit /b 1
)

echo.
echo  [ZiExpand] Building ZiExpand.exe ...
pyinstaller --noconfirm ziexpand.spec
if errorlevel 1 (
    echo  ERROR: PyInstaller build failed.
    pause
    exit /b 1
)

echo.
echo  ============================================================
echo   Build succeeded!
echo   Executable:  dist\ZiExpand.exe
echo  ============================================================
echo.
echo  You can copy dist\ZiExpand.exe anywhere and run it.
echo  Double-clicking it opens the GUI. You can also pass CLI
echo  arguments, e.g.:  ZiExpand.exe new MyExtension
echo.
pause
