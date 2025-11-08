"""
This module provides the main class for downloading videos and audio from YouTube.

Modules:
- `VideoDownloader`: A class to handle downloading videos, audio, playlists, and multiple links
  with support for different quality options, output formats, and network handling.
"""

from .video_downloader import VideoDownloader

__all__ = ['VideoDownloader']
