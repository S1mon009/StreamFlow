"""
This module provides a VideoDownloader class that allows users to download
videos, audio, and playlists using yt-dlp via subprocess. It
supports multiple quality options, output formats, network handling, and
downloading from TXT URL lists and YAML configuration files.
"""
import os
import string
import time
import subprocess
import inquirer
import yaml
from src.config import video_settings, app_config
from src.decorators import ffmpeg_required, is_connected, network_required, timed
from src.utils import send_notification


class VideoDownloader:
    """
    A class to handle video and audio downloading from YouTube.

    Features:
        - Download single URLs, TXT URL lists, and grouped YAML configurations.
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
        self.custom_filename = None
        self.download_profiles = []

    def verify_download_folder(self) -> None:
        """Ensure the configured download folder exists, prompting user if needed.

        If the configured folder does not exist, the user can provide a different
        path. The function will create the folder if it does not exist.

        Returns:
            None: This function updates the instance's ``download_folder`` attribute.
        """
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

    def _sanitize_filename(self, name: str) -> str:
        """Sanitize filename by removing or replacing characters invalid in file names.
        
        Args:
            name (str): The original filename to sanitize.
            
        Returns:
            str: The sanitized filename with invalid characters replaced by underscores.
        """
        invalid_chars = '<>:"/\\|?*'
        for ch in invalid_chars:
            name = name.replace(ch, '_')
        return name.strip()

    def prompt_user_options(self) -> None:
        """Prompt the user for download source, mode and format options.

        After this call the instance attributes ``urls``, ``mode``, ``quality`` and
        ``output_format`` will be set based on user choices.

        Returns:
            None
        """
        source_ans = inquirer.prompt([
            inquirer.List('source',
                          message="Choose source of links",
                          choices=['Single URL', 'TXT File', 'YAML File'])
        ])
        if not source_ans:
            return
        source = source_ans.get('source')

        if source == 'Single URL':
            url_answer = inquirer.prompt([inquirer.Text('url', message="Enter the video link")])
            if not url_answer or not url_answer.get('url'):
                self.urls = []
                return
            self.urls = [url_answer.get('url')]

            if 'list=' in self.urls[0]:
                self.is_playlist = True
                folder_ans = inquirer.prompt([inquirer.Text('playlist_folder', message="Enter playlist folder name")])
                if not folder_ans or not folder_ans.get('playlist_folder'):
                    self.urls = []
                    return
                self.playlist_folder = os.path.join(self.download_folder, folder_ans.get('playlist_folder'))
                if not os.path.exists(self.playlist_folder):
                    os.makedirs(self.playlist_folder)
            else:
                filename_ans = inquirer.prompt([inquirer.Text('filename',
                                                              message="Enter a new filename (default original title)")])
                filename = (filename_ans.get('filename') or '').strip()
                if filename:
                    filename = os.path.splitext(filename)[0]
                    filename = self._sanitize_filename(filename)
                    self.custom_filename = filename

        elif source == 'TXT File':
            file_answer = inquirer.prompt([inquirer.Text('file', message="Enter path to TXT file with links")])
            filepath = (file_answer or {}).get('file', '').strip()
            self.urls = self._read_urls_file(filepath)
            if self.urls:
                try:
                    self.download_profiles = [self._prompt_txt_profile()]
                except ValueError as error:
                    print(f"Invalid TXT download options: {error}")
                    self.urls = []
                    return
            else:
                return
        elif source == 'YAML File':
            file_answer = inquirer.prompt([inquirer.Text('file', message="Enter path to YAML download configuration")])
            filepath = (file_answer or {}).get('file', '').strip()
            try:
                self.download_profiles = self._load_yaml_profiles(filepath)
                self.urls = [
                    url for profile in self.download_profiles for url in profile['urls']
                ]
            except (OSError, UnicodeError, yaml.YAMLError, ValueError) as error:
                print(f"Error loading YAML download configuration: {error}")
                self.download_profiles = []
                self.urls = []
                return

        if self.download_profiles:
            first_profile = self.download_profiles[0]
            self.mode = first_profile['mode']
            self.quality = first_profile['quality']
            self.output_format = first_profile['output_format']
            self.download_folder = first_profile['folder']
            return

        mode_ans = inquirer.prompt([inquirer.List('mode', message="Choose download mode",
                                                  choices=['Video', 'Audio only'])])
        if not mode_ans:
            self.urls = []
            return
        self.mode = mode_ans.get('mode')

        if self.mode == 'Video':
            quality_ans = inquirer.prompt([inquirer.List('quality', message="Choose quality",
                                                        choices=list(video_settings.quality_map.keys()))])
            if not quality_ans:
                self.urls = []
                return
            self.quality = quality_ans.get('quality')

            format_ans = inquirer.prompt([inquirer.List('output_format', message="Choose output format",
                                                        choices=video_settings.output_formats)])
            if not format_ans:
                self.urls = []
                return
            self.output_format = format_ans.get('output_format')

    def _read_urls_file(self, filepath: str) -> list[str]:
        """Read non-empty URL lines from a TXT file."""
        if not filepath or not os.path.isfile(filepath):
            print(f"Error: File {filepath or '(no path provided)'} not found or invalid.")
            return []
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                urls = [line.strip() for line in file if line.strip()]
        except (OSError, UnicodeError) as error:
            print(f"Error reading URL file {filepath}: {error}")
            return []
        if not urls:
            print(f"Error: No URLs found in {filepath}.")
        return urls

    def _prompt_txt_profile(self) -> dict:
        """Ask for output and media settings for URLs read from a TXT file."""
        name = inquirer.prompt([
            inquirer.Text('name', message="Name for this download group", default="TXT downloads")
        ]) or {}
        output = inquirer.prompt([
            inquirer.Text('folder', message="Output folder", default=self.download_folder),
            inquirer.Text('prefix', message="Filename prefix", default=""),
            inquirer.Text('suffix', message="Filename suffix", default=""),
        ]) or {}
        naming = inquirer.prompt([
            inquirer.Text('template', message="Filename template", default="{title}"),
            inquirer.Confirm('indexing', message="Add an index to filenames?", default=False),
        ]) or {}
        indexing = {'enabled': bool(naming.get('indexing')), 'start': 1, 'padding': 2}
        if indexing['enabled']:
            index_options = inquirer.prompt([
                inquirer.Text('start', message="First index", default="1"),
                inquirer.Text('padding', message="Index padding", default="2"),
            ]) or {}
            try:
                indexing['start'] = int(index_options.get('start', '1'))
                indexing['padding'] = int(index_options.get('padding', '2'))
            except (TypeError, ValueError) as error:
                raise ValueError("Index start and padding must be whole numbers.") from error
            if indexing['start'] < 0 or indexing['padding'] < 1:
                raise ValueError("Index start must be non-negative and padding must be positive.")

        media_type_answer = inquirer.prompt([
            inquirer.List('type', message="Choose media type", choices=['video', 'audio'])
        ]) or {}
        media_type = media_type_answer.get('type')
        if media_type == 'video':
            format_choices = ['mkv', 'mp4']
            quality_choices = list(video_settings.quality_map.keys())
        else:
            format_choices = ['mp3', 'm4a', 'wav', 'flac']
            quality_choices = ['best', '320k', '192k', '128k']
        media_options = inquirer.prompt([
            inquirer.List('format', message="Choose output format", choices=format_choices),
            inquirer.List('quality', message="Choose quality", choices=quality_choices),
        ]) or {}

        folder = (output.get('folder') or '').strip()
        template = naming.get('template') or ''
        if not folder or not template or media_type not in ('video', 'audio'):
            raise ValueError("Output folder, filename template, and a media type are required.")
        if not media_options.get('format') or not media_options.get('quality'):
            raise ValueError("A media format and quality must be selected.")
        self._validate_naming_template(template, indexing['enabled'])
        return {
            'name': (name.get('name') or "TXT downloads").strip(),
            'urls': self.urls.copy(),
            'folder': os.path.expandvars(os.path.expanduser(folder)),
            'prefix': output.get('prefix', ''),
            'suffix': output.get('suffix', ''),
            'template': template,
            'indexing': indexing,
            'mode': 'Video' if media_type == 'video' else 'Audio only',
            'quality': media_options.get('quality'),
            'output_format': media_options.get('format'),
            'audio_quality': media_options.get('quality', 'best'),
        }

    def _load_yaml_profiles(self, filepath: str) -> list[dict]:
        """Load and validate version 1 YAML download profiles."""
        if not filepath or not os.path.isfile(filepath):
            raise ValueError(f"File {filepath or '(no path provided)'} not found or invalid.")
        with open(filepath, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)

        version = config.get('version') if isinstance(config, dict) else None
        if (
            not isinstance(config, dict)
            or not isinstance(version, int)
            or isinstance(version, bool)
            or version != 1
        ):
            raise ValueError("The YAML root must be a mapping with version: 1.")
        downloads = config.get('downloads')
        if not isinstance(downloads, list) or not downloads:
            raise ValueError("'downloads' must be a non-empty list.")

        profiles = []
        for position, entry in enumerate(downloads, start=1):
            if not isinstance(entry, dict):
                raise ValueError(f"Download entry {position} must be a mapping.")
            urls = entry.get('urls')
            output = entry.get('output')
            naming = entry.get('naming', {})
            media = entry.get('media')
            if not isinstance(urls, list) or not urls or not all(
                isinstance(url, str) and url.strip() for url in urls
            ):
                raise ValueError(f"Download entry {position} must contain a non-empty 'urls' list.")
            if not isinstance(output, dict) or not isinstance(output.get('folder'), str):
                raise ValueError(f"Download entry {position} must define output.folder.")
            if not isinstance(naming, dict) or not isinstance(media, dict):
                raise ValueError(f"Download entry {position} must define naming and media mappings.")
            indexing = naming.get('indexing', {})
            if not isinstance(indexing, dict):
                raise ValueError(f"Download entry {position}: naming.indexing must be a mapping.")
            enabled = indexing.get('enabled', False)
            start = indexing.get('start', 1)
            padding = indexing.get('padding', 2)
            if not isinstance(enabled, bool):
                raise ValueError(f"Download entry {position}: indexing.enabled must be true or false.")
            if (not isinstance(start, int) or isinstance(start, bool) or start < 0
                    or not isinstance(padding, int) or isinstance(padding, bool) or padding < 1):
                raise ValueError(f"Download entry {position}: indexing start/padding must be valid integers.")

            template = naming.get('template', '{title}')
            if not isinstance(template, str) or not template:
                raise ValueError(f"Download entry {position}: naming.template must be a non-empty string.")
            try:
                self._validate_naming_template(template, enabled)
            except ValueError as error:
                raise ValueError(f"Download entry {position}: {error}") from error
            media_type = media.get('type')
            media_format = media.get('format')
            quality = media.get('quality', 'best')
            if media_type not in ('video', 'audio'):
                raise ValueError(f"Download entry {position}: media.type must be 'video' or 'audio'.")
            if not isinstance(media_format, str) or not media_format.strip():
                raise ValueError(f"Download entry {position}: media.format must be a non-empty string.")
            if not isinstance(quality, str) or not quality.strip():
                raise ValueError(f"Download entry {position}: media.quality must be a non-empty string.")
            if media_type == 'video':
                self._quality_selector(quality)

            folder = os.path.expandvars(os.path.expanduser(output['folder'].strip()))
            if not folder:
                raise ValueError(f"Download entry {position}: output.folder cannot be empty.")
            prefix = output.get('prefix', '')
            suffix = output.get('suffix', '')
            name = entry.get('name', f"Download group {position}")
            if not isinstance(prefix, str) or not isinstance(suffix, str):
                raise ValueError(f"Download entry {position}: output prefix and suffix must be strings.")
            if not isinstance(name, str) or not name.strip():
                raise ValueError(f"Download entry {position}: name must be a non-empty string.")
            profiles.append({
                'name': name,
                'urls': [url.strip() for url in urls],
                'folder': folder,
                'prefix': prefix,
                'suffix': suffix,
                'template': template,
                'indexing': {'enabled': enabled, 'start': start, 'padding': padding},
                'mode': 'Video' if media_type == 'video' else 'Audio only',
                'quality': quality,
                'output_format': media_format.strip().lower(),
                'audio_quality': quality,
            })
        return profiles

    @staticmethod
    def _validate_naming_template(
        template: str, indexing_enabled: bool | None = None
    ) -> None:
        """Ensure naming templates use only supported fields."""
        try:
            parsed = list(string.Formatter().parse(template))
        except ValueError as error:
            raise ValueError(f"Invalid naming template: {error}") from error
        fields = [field for _, field, _, _ in parsed if field]
        unknown = set(fields) - {'title', 'prefix', 'suffix', 'index'}
        if unknown:
            raise ValueError(f"Unsupported naming template fields: {', '.join(sorted(unknown))}.")
        if indexing_enabled is False and 'index' in fields:
            raise ValueError("The naming template uses {index} while indexing is disabled.")
        for _, field, format_spec, conversion in parsed:
            if not field:
                continue
            if conversion:
                raise ValueError("Naming template conversions are not supported.")
            if format_spec and field != 'index':
                raise ValueError(f"Formatting is not supported for {{{field}}}.")
            if format_spec and (
                not format_spec.endswith('d')
                or not format_spec.startswith('0')
                or not format_spec[1:-1].isdigit()
            ):
                raise ValueError("Index format must use an integer format such as {index:02d}.")

    @staticmethod
    def _quality_selector(quality: str) -> str:
        """Resolve YAML shorthand or a configured quality label to yt-dlp syntax."""
        aliases = {
            'best': 'The best',
            '1440p': 'Medium (1440p)',
            '1080p': 'Above High (1080p)',
            '720p': 'High (720p)',
            '480p': 'Low (<=480p)',
        }
        label = aliases.get(quality.lower(), quality)
        if label not in video_settings.quality_map:
            raise ValueError(f"Unsupported video quality: {quality}.")
        return video_settings.quality_map[label]

    def _render_naming_template(
        self, template: str, profile: dict, index: int, is_playlist: bool
    ) -> str:
        """Translate the user-facing filename format into a yt-dlp output template."""
        indexing = profile['indexing']
        parts = []
        for literal, field, format_spec, conversion in string.Formatter().parse(template):
            parts.append(literal.replace('%', '%%'))
            if field is None:
                continue
            if conversion:
                raise ValueError("Naming template conversions are not supported.")
            if field == 'title':
                parts.append('%(title)s')
            elif field in ('prefix', 'suffix'):
                parts.append(str(profile[field]).replace('%', '%%'))
            elif field == 'index':
                if not indexing['enabled']:
                    raise ValueError("The naming template uses {index} while indexing is disabled.")
                width = indexing['padding']
                if format_spec:
                    if not format_spec.endswith('d') or not format_spec[:-1].startswith('0'):
                        raise ValueError("Index format must use an integer format such as {index:02d}.")
                    try:
                        width = int(format_spec[1:-1])
                    except ValueError as error:
                        raise ValueError(f"Invalid index format: {format_spec}.") from error
                    if width < 1:
                        raise ValueError("Index padding must be positive.")
                if is_playlist:
                    parts.append(f"%(autonumber)0{width}d")
                else:
                    parts.append(f"{index:0{width}d}")
            else:
                raise ValueError(f"Unsupported naming template field: {field}.")
        return ''.join(parts)

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
        for profile in self.download_profiles:
            indexing = profile['indexing']
            summary += (
                f"Group: {profile['name']}\n"
                f"Output folder: {profile['folder']}\n"
                f"Filename template: {profile['template']}\n"
                f"Indexing: {'on' if indexing['enabled'] else 'off'}\n"
                f"Media: {profile['mode']} ({profile['output_format']}, "
                f"quality: {profile['quality']})\n"
            )
        if not self.download_profiles and self.mode == "Video":
            summary += f"Quality: {self.quality}\nOutput format: {self.output_format}\n"
        if self.is_playlist:
            summary += f"Playlist folder: {self.playlist_folder}\n"
        if getattr(self, 'custom_filename', None) and len(self.urls) == 1 and not self.is_playlist:
            summary += f"Custom filename: {self.custom_filename}\n"
        summary += f"Download folder: {self.download_folder}\n-----------------------------------\n"
        print(summary)
        confirm = inquirer.prompt([inquirer.Confirm('confirm', message="Are these options correct?", default=True)])
        return confirm.get('confirm')

    def progress_hook(self, d: dict) -> None:
        """Monitor download progress and handle network interruptions.

        Args:
            d (dict): yt-dlp download status dictionary.
            
        Returns:
            None
        """
        if d.get('status') == 'downloading':
            if not is_connected():
                print("\nNetwork lost. Pausing download...")
                while not is_connected():
                    time.sleep(5)
                print("Connection restored. Resuming download...")

    def _retry_with_cookies(self, command: list[str], url: str) -> bool:
        """Ask for a cookies file after a failed download and retry once.
        
        Args:
            command (list[str]): The original command used for downloading.
            url (str): The URL that failed to download.
            
        Returns:
            bool: True if the retry was successful, False otherwise.
        """
        answer = inquirer.prompt([
            inquirer.Confirm(
                'use_cookies',
                message="Do you want to retry with a cookies file?",
                default=False,
            )
        ])
        if not answer or not answer.get('use_cookies'):
            return False

        cookies_answer = inquirer.prompt([
            inquirer.Text('cookies_path', message="Enter the path to the cookies file")
        ])
        cookies_path = (cookies_answer or {}).get('cookies_path', '').strip()
        if not cookies_path:
            print("No cookies path provided. Download cancelled.")
            return False
        if not os.path.isfile(cookies_path):
            print(f"Cookies file not found: {cookies_path}")
            return False

        retry_command = command.copy()
        cookies_index = retry_command.index('--cookies') + 1
        retry_command[cookies_index] = cookies_path
        try:
            print(f"Retrying download with cookies: {cookies_path}")
            subprocess.run(retry_command, check=True)
            return True
        except subprocess.CalledProcessError as error:
            print(f"\nRetry failed for {url}: {error}")
            return False

    @ffmpeg_required
    @network_required
    @timed
    def download_video(self) -> None:
        """Download configured URLs using ``yt-dlp`` and the project's cookies.

        Applies the selected quality and output format. Handles playlists by
        placing downloads in a playlist folder when configured. Errors from
        ``subprocess`` calls are caught and reported per-URL.

        Returns:
            None
        """
        profiles = self.download_profiles or [{
            'name': 'Downloads',
            'urls': self.urls,
            'folder': self.download_folder,
            'prefix': '',
            'suffix': '',
            'template': None,
            'indexing': {'enabled': False, 'start': 1, 'padding': 2},
            'mode': self.mode,
            'quality': self.quality,
            'output_format': self.output_format,
            'audio_quality': '192',
        }]
        for profile in profiles:
            folder = profile['folder']
            os.makedirs(folder, exist_ok=True)
            for position, url in enumerate(profile['urls']):
                is_playlist = 'list=' in url
                mode = profile['mode']
                quality = profile['quality']
                output_format = profile['output_format']
                output_format = output_format or 'mp3'
                if profile['template']:
                    filename_template = self._render_naming_template(
                        profile['template'],
                        profile,
                        profile['indexing']['start'] + position,
                        is_playlist,
                    )
                    output_folder = folder
                elif is_playlist and self.playlist_folder:
                    output_folder = self.playlist_folder
                    filename_template = '%(title)s'
                elif len(profile['urls']) == 1 and self.custom_filename and not is_playlist:
                    output_folder = folder
                    filename_template = self.custom_filename
                else:
                    output_folder = folder
                    filename_template = '%(title)s'
                output_path = os.path.join(output_folder, f"{filename_template}.%(ext)s")
                notification_path = output_path
                has_custom_filename = (
                    not profile['template']
                    and len(profile['urls']) == 1
                    and self.custom_filename
                    and not is_playlist
                )
                if has_custom_filename:
                    extension = output_format.lower() if mode == 'Video' else 'mp3'
                    print(f"Saving as: {self.custom_filename}.{extension}")
                    notification_path = os.path.join(
                        folder, f"{self.custom_filename}.{extension}"
                    )

                cmd = ['yt-dlp', '-o', output_path, url]
                if mode == "Video":
                    cmd.extend([
                        '-f', self._quality_selector(quality),
                        '--merge-output-format', output_format.lower(),
                    ])
                else:
                    audio_quality = str(profile['audio_quality'])
                    if audio_quality.lower() == 'best':
                        audio_quality = '0'
                    cmd.extend([
                        '-f', 'bestaudio/best',
                        '--extract-audio',
                        '--audio-format', output_format.lower(),
                        '--audio-quality', audio_quality,
                    ])
                if profile['template'] and is_playlist and profile['indexing']['enabled']:
                    cmd.extend(['--autonumber-start', str(profile['indexing']['start'])])
                if not is_playlist:
                    cmd.append('--no-playlist')

                try:
                    print(f"Downloading: {url}")
                    subprocess.run(cmd, check=True)
                    send_notification(
                        "Successful download",
                        f"Saved as: {notification_path.replace('\\', '/')}",
                    )
                    print(f"\nSuccessful download: {url}")
                except subprocess.CalledProcessError as error:
                    print(f"\nDownload error for {url}: {error}")
                    if self._retry_with_cookies(cmd, url):
                        send_notification(
                            "Successful download",
                            f"Saved to: {notification_path.replace('\\', '/')}",
                        )
                        print(f"\nSuccessful download: {url}")
