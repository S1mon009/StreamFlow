# Installation

This page describes how to install StreamFlow and prepare the environment required to run it.

## Requirements

Before installing StreamFlow, make sure the following software is available:

* Python 3.x;
* pip;
* Git;
* FFmpeg;
* an active internet connection.

FFmpeg is an external system dependency and must be installed separately from the Python packages.

## Clone the repository

Clone the repository using Git:

```bash
git clone https://github.com/S1mon009/StreamFlow.git
```

Navigate to the project directory:

```bash
cd StreamFlow
```

## Create a virtual environment

Using a virtual environment is recommended because it keeps StreamFlow's dependencies isolated from other Python projects.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Windows Command Prompt

```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

After activation, the terminal should indicate that the virtual environment is active.

## Install Python dependencies

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Then install the project's dependencies:

```bash
pip install -r requirements.txt
```

## Install FFmpeg

StreamFlow relies on FFmpeg for multimedia processing and verifies its availability before downloading.

### Windows

Install FFmpeg and add its executable directory to the system `PATH`.

Verify the installation:

```powershell
ffmpeg -version
```

### Ubuntu / Debian

```bash
sudo apt update
sudo apt install ffmpeg
```

Verify:

```bash
ffmpeg -version
```

### macOS

If Homebrew is installed:

```bash
brew install ffmpeg
```

Then:

```bash
ffmpeg -version
```

## Verify the installation

Run StreamFlow from the project root:

```bash
python main.py
```

If the environment has been configured correctly, the application starts and displays its interactive terminal interface.

## Common installation problems

### Python is not recognized

Verify that Python is installed and available in `PATH`:

```bash
python --version
```

On some Linux systems:

```bash
python3 --version
```

### FFmpeg is not recognized

Run:

```bash
ffmpeg -version
```

If the command is unavailable, install FFmpeg and make sure its executable directory is present in `PATH`.

### Dependencies cannot be imported

Make sure the virtual environment is activated before running:

```bash
pip install -r requirements.txt
```
