#!/bin/bash

# Exit on error
set -e

echo "--- P2P Voice Chat: Linux Setup & Run ---"

# 1. Check for Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 is not installed."
    exit 1
fi

# 2. Install System Dependencies (PortAudio)
if command -v apt-get &> /dev/null; then
    echo "Detected Debian/Ubuntu-based system. Checking for PortAudio..."
    if ! dpkg -s portaudio19-dev &> /dev/null; then
        echo "Installing portaudio19-dev (requires sudo)..."
        sudo apt-get update && sudo apt-get install -y portaudio19-dev python3-all-dev
    fi
fi

# 3. Virtual Environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

# 4. Install Requirements
echo "Installing/Updating Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# 5. Run Application
echo "Launching application..."
python3 main.py "$@"
