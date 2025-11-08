"""
This module provides utility functions for console operations.

Functions:
    clear_console: Clears the terminal screen on both Windows and Unix-based systems.
"""

import os

def clear_console() -> None:
    """Clear the console screen.

    This function works for both Windows ('cls') and Unix-based ('clear') operating systems.

    Returns:
        None
    """
    os.system('cls' if os.name == 'nt' else 'clear')
