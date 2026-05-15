# P2P Terminal Voice Chat (Rust Version)

A cross-platform, low-latency peer-to-peer voice chat application built with Rust. This version compiles to a standalone binary, making it much easier to run on machines without Python.

## Features
- **Zero Runtime Dependencies**: Once compiled, it's a single file.
- **Low Latency**: Uses UDP and `cpal` for high-performance audio.
- **Cross-Platform**: Works on Windows (WASAPI) and Linux (ALSA).

## Installation

You will need the Rust toolchain installed. If you don't have it, get it at [rustup.rs](https://rustup.rs/).

### Linux Dependencies
You may need the ALSA development headers:
```bash
sudo apt-get update
sudo apt-get install libasound2-dev
```

### Build
```bash
cargo build --release
```
The binary will be located at `target/release/direct-voice-chat`.

## Usage

### 1. Start the Host
```bash
./target/release/direct-voice-chat --mode host
```
Note the **Local IP** displayed.

### 2. Join the Session
```bash
./target/release/direct-voice-chat --mode join --ip <HOST_IP>
```

## Controls
- **Ctrl+C**: Gracefully stop the chat.
