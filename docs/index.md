# StreamFlow

StreamFlow is a Python-based command-line application for downloading video and audio content using [yt-dlp](https://github.com/yt-dlp/yt-dlp).

The application provides an interactive terminal interface that allows users to configure downloads without manually constructing `yt-dlp` commands.

StreamFlow supports:

* single video downloads;
* playlist downloads;
* multiple URLs loaded from a text file;
* video downloads;
* audio-only downloads;
* configurable video quality;
* MP4 and MKV output;
* custom filenames;
* configurable download directories;
* network connectivity monitoring;
* FFmpeg availability checks;
* download execution-time measurement.

## Features

### Interactive CLI

StreamFlow uses an interactive terminal workflow. Instead of requiring a large number of command-line arguments, the application asks the user for the required configuration step by step.

### Video downloads

Users can select one of several predefined quality levels, from low-quality downloads up to the best available quality.

Supported video containers are currently:

* MP4
* MKV

### Audio-only downloads

StreamFlow can extract audio from a source and save it as MP3.

### Playlist support

URLs containing a `list=` parameter are treated as playlists. StreamFlow creates a dedicated directory for the playlist and downloads its contents there.

### Multiple URLs

A text file can be used as a source containing multiple URLs. Each non-empty line is treated as a separate download URL.

### Network resilience

The application checks network connectivity before starting a download and can wait for connectivity to return when the connection is lost during a download.

### FFmpeg integration

FFmpeg is required for multimedia processing. StreamFlow verifies that FFmpeg is available before starting the download operation.

## Documentation

The documentation is divided into several sections:

* **Getting started** — installation and first steps;
* **User guide** — detailed information about download functionality;
* **Architecture** — internal project structure and execution flow;
* **API** — Python API reference;
* **Development** — information for contributors;
* **Reference** — FAQ and troubleshooting.

## Project repository

The source code is available on GitHub:

[StreamFlow](https://github.com/S1mon009/StreamFlow)

## License

See the repository license for information about the terms under which StreamFlow may be used and distributed.
