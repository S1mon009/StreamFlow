"""
This module provides a decorator for verifying the presence of FFmpeg.

Functions:
    ffmpeg_required: Ensures FFmpeg is installed before executing the decorated function.
"""

import subprocess

def ffmpeg_required(func:callable) -> callable:
    """Decorator that checks if FFmpeg is installed before running a function.

    If FFmpeg is not found, prints an error message and prevents the function from executing.

    Args:
        func (Callable): Function to decorate.

    Returns:
        Callable: Wrapped function that verifies FFmpeg installation.
    """
    def wrapper(*args:tuple, **kwargs:dict[str, dict]) -> callable:
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, check=True)
        except FileNotFoundError:
            print("Error: FFmpeg is not installed. Please install FFmpeg and try again.")
            return None
        return func(*args, **kwargs)
    return wrapper
