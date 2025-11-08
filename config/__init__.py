"""
This package provides access to application-wide configuration objects.

Modules:
    app_config: Application configuration settings.
    video_settings: Default video download settings.

Attributes:
    app_config: Imported from `app_config`, contains main application settings.
    video_settings: Imported from `video_settings`, contains video quality and format settings.
"""

from .app_config import app_config
from .video_settings import video_settings

__all__:str = ['app_config', 'video_settings']
