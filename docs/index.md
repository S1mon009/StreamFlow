# StreamFlow CLI — Professional Getting Started

Welcome to the official documentation for **StreamFlow CLI** — a complete command-line application for downloading videos and audio. This project is designed as a flexible CLI tool that integrates `yt-dlp`, `FFmpeg`, environment-based configuration, and intelligent decorators for stability and reliable execution.

---

## About the Project

StreamFlow CLI is a command-line utility for users who need an efficient and dependable tool for downloading videos and audios.

Key capabilities:

- Download single videos, playlists, or multiple links from a `.txt` file
- Video mode and audio-only mode
- Video quality selection and output format conversion
- Download folder and file name management
- Network connectivity monitoring and automatic resume handling
- Automatic FFmpeg dependency verification
- Support for `cookies.txt` to access restricted or age-gated content

---

## Core Features

- **Interactive guided prompts**: The CLI asks for source type, download mode, quality, and format.
- **Playlist support and batch downloads**: Automatically detect playlists and read multiple URLs from a text file.
- **Quality selection**:
    - The best
    - Medium (1440p)
    - Above High (1080p)
    - High (720p)
    - Low (<=480p)
- **Supported output formats**: `Mp4`, `Mkv`; audio downloads are saved as `mp3`.
- **Configuration management**: Default download folder can be customized via `.env`.
- **Download validation**: Checks for `FFmpeg` and network availability before starting.

---

## Installation

1.Clone the repository:

```bash
git clone https://github.com/S1mon009/StreamFlow/CLI
cd CLI
```

2.Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

3.Install dependencies:

```bash
pip install -r requirements.txt
```

4.Ensure `yt-dlp` and `ffmpeg` are available on your PATH.

---

## Configuration

The application configuration in `config/app_config.py` reads the `DOWNLOAD_FOLDER` value from a `.env` file.

Example `.env`:

```ini
DOWNLOAD_FOLDER=C:\Users\YourUser\Downloads\StreamFlow
```

If the folder does not exist, the app prompts for a new path and creates the directory automatically.

---

## Usage

Run the program:

```bash
python main.py
```

Then:

1. choose the source type (single URL or `.txt` file),
2. choose download mode (`Video` or `Audio only`),
3. choose quality and format,
4. confirm settings and start the download.

---

## How It Works

1. `main.py` creates a `VideoDownloader` instance and calls `prompt_user_options()`.
2. `VideoDownloader` prompts for:
   - source type,
   - URL or link file path,
   - download mode,
   - video quality and format.
3. The user confirms selections in `confirm_options()`.
4. `download_video()` builds the `yt-dlp` command and executes it with `subprocess.run()`.
5. If network connectivity is lost, `progress_hook()` waits until the connection is restored.
6. If `FFmpeg` is required for merging or format conversion, the `ffmpeg_required` decorator ensures it is installed.

---

## `cookies.txt` Support

The `cookies.txt` file is used by `yt-dlp` to download content that requires authentication or cookies. Place the file in the project root to improve support for age-restricted or protected videos.

