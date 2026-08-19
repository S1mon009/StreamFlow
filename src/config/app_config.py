"""
This module defines the application's configuration settings using Pydantic.
It loads variables and provides a centralized
way to access configuration values throughout the project.
"""
from pydantic import Field
from pydantic import BaseModel


class AppConfig(BaseModel):
    """Application configuration settings.

    This class loads and manages application-wide configuration variables.

    Attributes:
        download_folder (str): The default folder where downloaded videos will be saved.

    Example:
        ```python
        app_config = AppConfig()
        print(app_config.download_folder)
        ```
    """

    download_folder: str = Field(default="~/Downloads")


app_config = AppConfig()
"""app_config: Global configuration instance for app."""
