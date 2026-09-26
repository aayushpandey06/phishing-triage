#!/bin/sh
# Mac / Linux setup: downloads the emails, runs the script, opens VS Code.
# Run it with:  sh setup.sh
cd "$(dirname "$0")" || exit 1
echo "Setting up the phishing triage project..."

PY=$(command -v python3 || command -v python)
if [ -z "$PY" ]; then
    echo "Python not found. Install it from https://www.python.org/downloads/ and run this again."
    exit 1
fi

if ! "$PY" get_samples.py; then
    echo "Download failed. On a Mac this is usually missing certificates:"
    echo "open your Python folder in Applications, run 'Install Certificates.command', then try again."
    exit 1
fi

"$PY" triage.py samples/ > triage_output.txt
echo "Done. The script's full output is in triage_output.txt"

if command -v code >/dev/null 2>&1; then
    code .
else
    echo "Now open VS Code and choose File > Open Folder, then pick this folder."
fi
