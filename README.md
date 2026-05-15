# P2P Terminal Voice Chat

A cross-platform (Windows & Linux), low-latency peer-to-peer voice chat application built with Python.

## Features
- **P2P Architecture:** Connects directly between two peers.
- **Low Latency:** Uses UDP for real-time audio transmission.
- **Clean CLI:** Modern terminal interface using the `rich` library.
- **Fast Join:** Automatically detects local IPs to simplify connections.

## Prerequisites

### Linux (Ubuntu/Debian)
You need to install the PortAudio development headers before installing the Python packages:
```bash
sudo apt-get update
sudo apt-get install portaudio19-dev python3-pyaudio
```

### Windows
PyAudio usually installs directly via pip, but ensure you have a working Python environment.

## Installation

1. Clone the repository (if you haven't already).
2. Install the Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### 1. Start the Host
On one machine, run:
```bash
python main.py --mode host
```
The app will display the local IP address (e.g., `192.168.1.50`).

### 2. Join the Session
On the second machine (on the same local network), run:
```bash
python main.py --mode join --ip 192.168.1.50
```
*(Replace `192.168.1.50` with the IP displayed on the host machine).*

## Controls
- **Ctrl+C**: Gracefully stop the chat and exit.

## Troubleshooting
- **Firewall:** Ensure that the port (default `50005`) is allowed through your system firewall for UDP traffic.
- **Microphone Permissions:** Ensure your terminal or Python executable has permission to access the microphone.
