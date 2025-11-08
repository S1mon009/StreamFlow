"""
This module defines the application's configuration settings using Pydantic.
It loads environment variables from a `.env` file and provides a centralized
way to access configuration values throughout the project.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class AppConfig(BaseSettings):
    """Application configuration settings.

    This class loads and manages application-wide configuration variables.
    It uses environment variables defined in a `.env` file to override defaults.

    Attributes:
        download_folder (str): The default folder where downloaded videos will be saved.
            This value can be set via the environment variable `DOWNLOAD_FOLDER`.

    Example:
        ```python
        app_config = AppConfig()
        print(app_config.download_folder)
        ```
    """

    download_folder: str = Field(default="~/Downloads", alias="DOWNLOAD_FOLDER")

    model_config = SettingsConfigDict(env_file=".env")


app_config = AppConfig()
"""app_config: Global configuration instance loaded from the environment file."""
