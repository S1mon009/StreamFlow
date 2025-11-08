"""
This module provides a VideoDownloader class that allows users to download
videos, audio, and playlists using yt-dlp via subprocess. It
supports multiple quality options, output formats, network handling, and
downloading from a .txt file containing multiple links.
"""

import os
import time
import subprocess
import inquirer
from decorators import timed, ffmpeg_required, is_connected, network_required
from config import video_settings, app_config

class VideoDownloader:
    """
    A class to handle video and audio downloading from YouTube.

    Features:
        - Download single videos, audio, playlists, or multiple links from a TXT file.
        - Provides various quality options for video downloads.
        - Supports multiple output formats (Mp4, Mkv, Mp3).
        - Handles network disconnections gracefully.
        - Ensures the download folder exists and is correctly set.

    Attributes:
        QUALITY_MAP (Dict[str, str]): Mapping of human-readable quality labels to yt-dlp format selectors.
        OUTPUT_FORMATS (List[str]): Supported output formats.
        download_folder (str): Path where downloaded files will be saved.
        urls (List[str]): List of video URLs to download.
        quality (str): Selected video quality.
        output_format (str): Selected output format.
        is_playlist (bool): Flag indicating if the URL is a playlist.
        playlist_folder (str): Folder path for playlist downloads.
        mode (str): Download mode, either 'Video' or 'Audio only'.
    """

    def __init__(self):
        """Initialize the downloader and verify the download folder."""
        self.download_folder = app_config.download_folder
        self.verify_download_folder()
        self.urls = []
        self.quality = None
        self.output_format = None
        self.is_playlist = False
        self.playlist_folder = None
        self.mode = None

    def verify_download_folder(self) -> None:
        """Check if the download folder exists, or prompt the user to provide one."""
        question = [
            inquirer.Confirm('use_default',
                             message=f"Is the default download path ({self.download_folder}) correct?",
                             default=True)
        ]
        answer = inquirer.prompt(question)
        if not answer.get('use_default'):
            new_folder = inquirer.prompt([inquirer.Text('folder',
                                                        message="Enter a new download path")])
            self.download_folder = new_folder.get('folder')
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)

    def prompt_user_options(self) -> None:
        """Prompt the user to select URLs, mode, quality, output format, and playlist folder."""
        source_ans = inquirer.prompt([
            inquirer.List('source',
                          message="Choose source of links", choices=['Single URL', 'TXT File'])
        ])
        source = source_ans.get('source')

        if source == 'Single URL':
            url_answer = inquirer.prompt([inquirer.Text('url', message="Enter the video link")])
            self.urls = [url_answer.get('url')]

            if 'list=' in self.urls[0]:
                self.is_playlist = True
                folder_ans = inquirer.prompt([inquirer.Text('playlist_folder', message="Enter playlist folder name")])
                self.playlist_folder = os.path.join(self.download_folder, folder_ans.get('playlist_folder'))
                if not os.path.exists(self.playlist_folder):
                    os.makedirs(self.playlist_folder)

        else:
            file_answer = inquirer.prompt([inquirer.Text('file', message="Enter path to TXT file with links")])
            filepath = file_answer.get('file')
            if not os.path.exists(filepath) or not os.path.isfile(filepath):
                print(f"Error: File {filepath} not found or invalid.")
                self.urls = []
            else:
                with open(filepath, "r", encoding="utf-8") as f:
                    self.urls = [line.strip() for line in f if line.strip()]

        mode_ans = inquirer.prompt([inquirer.List('mode', message="Choose download mode",
                                                  choices=['Video', 'Audio only'])])
        self.mode = mode_ans.get('mode')

        if self.mode == 'Video':
            quality_ans = inquirer.prompt([inquirer.List('quality', message="Choose quality",
                                                        choices=list(video_settings.quality_map.keys()))])
            self.quality = quality_ans.get('quality')

            format_ans = inquirer.prompt([inquirer.List('output_format', message="Choose output format",
                                                        choices=video_settings.output_formats)])
            self.output_format = format_ans.get('output_format')

    def confirm_options(self) -> bool:
        """Display selected options and ask the user for confirmation.

        Returns:
            bool: True if the user confirms, False otherwise.
        """
        summary = (
            f"\nSummary of selected options:\n"
            f"-----------------------------------\n"
            f"Number of links: {len(self.urls)}\n"
            f"Mode: {self.mode}\n"
        )
        if self.mode == "Video":
            summary += f"Quality: {self.quality}\nOutput format: {self.output_format}\n"
        if self.is_playlist:
            summary += f"Playlist folder: {self.playlist_folder}\n"
        summary += f"Download folder: {self.download_folder}\n-----------------------------------\n"
        print(summary)
        confirm = inquirer.prompt([inquirer.Confirm('confirm', message="Are these options correct?", default=True)])
        return confirm.get('confirm')

    def progress_hook(self, d: dict) -> None:
        """Monitor download progress and handle network interruptions.

        Args:
            d (dict): yt-dlp download status dictionary.
        """
        if d.get('status') == 'downloading':
            if not is_connected():
                print("\nNetwork lost. Pausing download...")
                while not is_connected():
                    time.sleep(5)
                print("Connection restored. Resuming download...")

    @ffmpeg_required
    @network_required
    @timed
    def download_video(self) -> None:
        """Download all URLs using yt-dlp and cookies.txt.

        Handles playlists and non-playlist videos, applying the selected quality
        and output format.
        """
        for url in self.urls:
            is_playlist = 'list=' in url
            if is_playlist and self.playlist_folder:
                output_path = os.path.join(self.playlist_folder, '%(title)s.%(ext)s')
            else:
                output_path = os.path.join(self.download_folder, '%(title)s.%(ext)s')

            cmd = ['yt-dlp', '--cookies', 'cookies.txt', '-o', output_path, url]

            if self.mode == "Video":
                cmd.extend(['-f', video_settings.quality_map.get(self.quality, 'bestvideo+bestaudio/best'),
                            '--merge-output-format', self.output_format.lower()])
            else:
                cmd.extend(['-f', 'bestaudio/best', '--extract-audio', '--audio-format', 'mp3', '--audio-quality', '192'])

            if not is_playlist:
                cmd.append('--no-playlist')

            try:
                print(f"Downloading: {url}")
                subprocess.run(cmd, check=True)
                print(f"\nSuccessful download: {url}")
            except subprocess.CalledProcessError as e:
                print(f"\nDownload error for {url}: {e}")
