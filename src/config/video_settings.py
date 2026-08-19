"""
This module provides default settings for video downloading or processing.
It defines a Pydantic model for video quality mapping and supported output formats.
"""

from typing import Dict, List
from pydantic import BaseModel

class VideoSettings(BaseModel):
    """
    Defines default configurations for video downloads.

    Attributes:
        quality_map (Dict[str, str]): Mapping of human-readable quality labels
            to video format selectors. Keys include:
                - 'The best'
                - 'Medium (1440p)'
                - 'Above High (1080p)'
                - 'High (720p)'
                - 'Low (<=480p)'
        output_formats (List[str]): List of supported output file formats, e.g., 'Mp4' and 'Mkv'.
        
    Example:
        ```python
        from config.video_settings import video_settings
        print(video_settings.quality_map)
        print(video_settings.output_formats)
        ```
    """

    quality_map: Dict[str, str] = {
        'The best': 'bestvideo+bestaudio/best',
        'Medium (1440p)': 'bestvideo[height<=1440]+bestaudio/best[height<=1440]',
        'Above High (1080p)': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        'High (720p)': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
        'Low (<=480p)': 'bestvideo[height<=480]+bestaudio/best[height<=480]'
    }

    output_formats: List[str] = ['Mp4', 'Mkv']

video_settings = VideoSettings()
"""video_settings: Global video settings instance."""
