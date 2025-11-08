"""
This package provides commonly used decorators for the application.

Modules:
    connected: Provides `network_required` decorator to ensure network connectivity.
    ffmpeg: Provides `ffmpeg_required` decorator to ensure FFmpeg is installed.
    timed: Provides `timed` decorator to measure function execution time.

Attributes:
    network_required: Imported from `connected`, ensures a network connection before function execution.
    is_connected: Imported from `connected`, checks if the system is connected to the internet.
    ffmpeg_required: Imported from `ffmpeg`, ensures FFmpeg is installed before function execution.
    timed: Imported from `timed`, measures and displays the execution time of a function.
"""
from .connected import network_required, is_connected
from .ffmpeg import ffmpeg_required
from .timed import timed

__all__ = ['network_required', 'is_connected', 'ffmpeg_required', 'timed']
