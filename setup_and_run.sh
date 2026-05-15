#!/bin/bash

# Exit on error
set -e

echo "--- P2P Voice Chat: Linux Setup & Run ---"

# 1. Check for Python & Pip
if ! command -v python3 &> /dev/null; then
    echo "Python3 not found. Attempting to install..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get update && sudo apt-get install -y python3 python3-pip python3-venv
    else
        echo "Error: Python3 is not installed and I don't know how to install it on this distro."
        echo "Please install python3, pip, and venv manually."
        exit 1
    fi
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
