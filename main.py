"""
Main script for the Video Downloader application.

This script initializes the `VideoDownloader` class, prompts the user for download options,
and handles multiple download requests in a loop. It supports both single video links
and TXT files containing multiple links, as well as video or audio download modes.
"""

import time
import inquirer
from art import text2art
from classes.video_downloader import VideoDownloader
from utils.console import clear_console

def main() -> None:
    """Run the Video Downloader application.

    Continuously prompts the user for download options and executes downloads
    until the user chooses to exit.

    Returns:
        None: This function does not return a value.
    """
    clear_console()
    print(text2art("StreamFlow"))
    while True:
        downloader = VideoDownloader()
        downloader.prompt_user_options()

        if not downloader.urls:
            print("No valid links provided. Returning to configuration...\n")
            time.sleep(1)
            clear_console()
            continue

        if not downloader.confirm_options():
            print("Return to configuration...\n")
            time.sleep(1)
            clear_console()
            continue

        downloader.download_video()

        again = inquirer.prompt([
            inquirer.Confirm('again', message="Do you want to download more?", default=False)
        ])
        if not again.get('again'):
            print("Thank you for using the program.")
            break

        clear_console()

if __name__ == "__main__":
    main()
