"""
This module defines the SettingsComponent class for building the UI
components of the settings view using Flet.
"""

import flet as ft
from src.config import THEME, OUTPUT_OPTIONS

class Settings:
    """
    A reusable component encapsulating all UI controls for the settings view.
    """

    def __init__(self, page: ft.Page, settings, service):
        self.page = page
        self.settings = settings
        self.service = service
        self._build_ui()

    def _build_ui(self):
        # Theme change handler
        def on_theme_change(e: ft.ControlEvent):
            new_theme = e.control.value
            self.page.theme_mode = ft.ThemeMode.DARK if new_theme == "dark" else ft.ThemeMode.LIGHT
            self.page.update()
            self.service.update_settings(theme=new_theme)

        # Generic field change handler
        def on_change(e: ft.ControlEvent):
            key = e.control.data
            value = e.control.value
            self.service.update_settings(**{key: value})

        # Download path change
        def on_path_change(e: ft.ControlEvent):
            self.service.update_settings(default_download_path=e.control.value)

        # Reset button click
        def on_reset_click(e: ft.ControlEvent):
            self.service.update_settings(
                theme="light",
                default_quality="The best",
                default_video_format="mp4",
                default_audio_format="mp3",
                default_download_path="C:/Downloads",
            )
            self.page.snack_bar = ft.SnackBar(ft.Text("Settings reset to defaults"))
            self.page.snack_bar.open = True
            self.page.theme_mode = ft.ThemeMode.LIGHT

            self.theme_radio.value = "light"
            self.quality_dropdown.value = "The best"
            self.video_format_dropdown.value = "mp4"
            self.audio_format_dropdown.value = "mp3"
            self.path_field.value = "C:/Downloads"
            self.page.update()

        # Theme radio group
        self.theme_radio = ft.RadioGroup(
            content=ft.Column([ft.Radio(label=t, value=t.lower()) for t in THEME], spacing=5),
            value=self.settings.theme,
            on_change=on_theme_change,
        )

        self.personalization_section = ft.Column(
            [
                ft.Text("Personalization", style="headlineMedium"),
                self.theme_radio,
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        )

        # Dropdowns and fields
        self.quality_dropdown = ft.Dropdown(
            label="Default download quality",
            options=[ft.dropdown.Option(o) for o in OUTPUT_OPTIONS["video"]["qualities"]],
            value=self.settings.default_quality,
            width=400,
            on_change=on_change,
            data="default_quality",
            border_color=ft.Colors.SECONDARY_CONTAINER,
            focused_border_color=ft.Colors.PRIMARY,
        )

        self.video_format_dropdown = ft.Dropdown(
            label="Default video format",
            options=[ft.dropdown.Option(o) for o in OUTPUT_OPTIONS["video"]["formats"]],
            value=self.settings.default_video_format,
            width=400,
            on_change=on_change,
            data="default_video_format",
            border_color=ft.Colors.SECONDARY_CONTAINER,
            focused_border_color=ft.Colors.PRIMARY,
        )

        self.audio_format_dropdown = ft.Dropdown(
            label="Default audio format",
            options=[ft.dropdown.Option("mp3"), ft.dropdown.Option("FLAC")],
            value=self.settings.default_audio_format,
            width=400,
            on_change=on_change,
            data="default_audio_format",
            focused_border_color=ft.Colors.PRIMARY,
            border_color=ft.Colors.SECONDARY_CONTAINER,
        )

        self.path_field = ft.TextField(
            label="Default download folder",
            value=self.settings.default_download_path,
            width=400,
            on_change=on_path_change,
            border_color=ft.Colors.SECONDARY_CONTAINER,
            focused_border_color=ft.Colors.PRIMARY,
        )

        self.reset_button = ft.OutlinedButton(
            "Reset to defaults",
            icon=ft.icons.RESTART_ALT,
            on_click=on_reset_click,
        )

        self.general_section = ft.Column(
            [
                ft.Text("General", style="headlineMedium"),
                self.quality_dropdown,
                self.video_format_dropdown,
                self.audio_format_dropdown,
                self.path_field,
                ft.Row([self.reset_button]),
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        )

    def render(self) -> ft.Row:
        """
        Returns the complete UI component for the settings view.
        """
        return ft.Row(
            spacing=0,
            controls=[
                ft.Container(
                    content=ft.Column(
                        [
                            self.general_section,
                            ft.Divider(),
                            self.personalization_section,
                        ],
                        spacing=30,
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                    ),
                    margin=ft.margin.only(left=-40, top=60, right=40, bottom=40),
                    expand=True,
                )
            ],
            vertical_alignment=ft.CrossAxisAlignment.START,
            expand=True,
        )
