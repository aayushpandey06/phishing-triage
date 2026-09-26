@echo off
rem Windows setup: downloads the emails, runs the script, opens VS Code.
cd /d "%~dp0"
echo Setting up the phishing triage project...
echo.

set PY=
where py >nul 2>nul && set PY=py
if not defined PY where python >nul 2>nul && set PY=python
if not defined PY (
    echo Python not found. Install it from https://www.python.org/downloads/
    echo During install, tick "Add python.exe to PATH". Then run this file again.
    pause
    exit /b 1
)

%PY% get_samples.py
if errorlevel 1 (
    echo Download failed. Check your internet connection and run this file again.
    pause
    exit /b 1
)

%PY% triage.py samples\ > triage_output.txt
echo.
echo Done. The script's full output is in triage_output.txt
echo.

where code >nul 2>nul
if errorlevel 1 (
    echo Now open VS Code and choose File ^> Open Folder, then pick this folder.
) else (
    code .
)
pause
