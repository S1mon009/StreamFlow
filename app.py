"""
Entry point of the application.

Initializes services and starts the Flet application.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
import flet as ft
from src.main import main
from src.db.db import create_services


if __name__ == "__main__":
    services = create_services()
    ft.app(target=main)
