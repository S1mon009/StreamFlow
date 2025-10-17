"""
This module defines the settings view for the application.
It uses SettingsComponent to render the UI and SettingsService for data handling.
"""

import flet as ft
from src.db.db import create_services
from src.controls import Settings

def settings_view(page: ft.Page) -> ft.Row:
    """
    Renders the settings view of the app with editable configuration fields.
    Loads SettingsService automatically from create_services().
    """
    services = create_services()
    service = services["settings_service"]
    settings = service.get_settings()

    component = Settings(page, settings, service)
    return component.render()
