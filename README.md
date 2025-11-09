# StreamFlow - Multi-Interface Media Fetcher
StreamFlow is a modular Python project that provides three different interfaces for fetching and streaming multimedia content:
- **API** - FastAPI-based REST API for remote access
- **CLI** - Command-line interface for local usage
- **GUI** - Desktop application with a simple graphical interface

Each interface is stored on a separate branch:
- `API` - FastAPI version
- `CLI` - Command-line version
- `GUI` - Graphical desktop version

> StreamFlow is designed for educational and personal use.
> It should only be used with **authorized or publicly available sources** (e.g. open media, personal content or internal servers).

---

## Features
- Stream and process media in real time
- Unified architecture across API, CLI and GUI
- Modular core logic shared between interfaces
- Docker-ready deplayment (for API version)

---

## Branch overview
| Branch | Description | Interface |
|--------|-------------|-----------|
| `API` | REST API built with FastAPI | Web |
| `CLI` | Command-line version | Terminal |
| `GUI` | Graphical version | Desktop |

---

## Installation
1. Clone the repository
```bash
git clone https://github.com/S1mon009/StreamFlow.git
cd streamflow
```

2. Switch to the desired branch
For example, to use the API version:
```bash
git checkout API
```

Or for the CLI version:
```bash
git checkout CLI
```

3. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

4. Install dependencies
```bash
pip install -r requirements.txt
```

6. Install FFmpeg (required)

StreamFlow relies on FFmpeg for handling and processing multimedia content.
Make sure it is installed and accessible from your system’s PATH.

Linux (Debian/Ubuntu)
```bash
sudo apt update
sudo apt install ffmpeg
```

macOS (Homebrew)
```bash
brew install ffmpeg
```

Windows
Download and install FFmpeg from:
https://ffmpeg.org/download.html

You can verify the installation by running:
```bash
ffmpeg -version
```

---

## Example use cases
- Educational demo for Python interface design
- Internal media management system
- Self-hosted streaming tool for authorized content
- Showcase of backend + CLI + GUI architecture

---

## License
MIT License - for educational and non-commercial use.
Always respect third-party content rights.

