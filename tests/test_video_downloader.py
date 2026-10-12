import os
import subprocess
import pytest
from unittest.mock import MagicMock
from src.classes.video_downloader import VideoDownloader

@pytest.fixture
def downloader_environment(monkeypatch):
    """Prepare the VideoDownloader environment without real prompts or subprocess calls."""
    calls = []

    def fake_run(args, **kwargs):
        calls.append(args)
        return MagicMock(returncode=0)

    monkeypatch.setattr('src.classes.video_downloader.subprocess.run', fake_run)
    monkeypatch.setattr('src.decorators.ffmpeg.subprocess.run', fake_run)
    monkeypatch.setattr('src.decorators.connected.is_connected', lambda *a, **k: True)
    monkeypatch.setattr('src.classes.video_downloader.is_connected', lambda *a, **k: True)
    monkeypatch.setattr('src.classes.video_downloader.send_notification', lambda *a, **k: None)
    monkeypatch.setattr('src.classes.video_downloader.VideoDownloader.verify_download_folder', lambda self: None)
    return calls

def _get_downloader(tmp_path, mode='Video', custom_filename='test', urls=None, output_format='Mp4'):
    """Factory for creating configured VideoDownloader instances."""
    d = VideoDownloader()
    d.download_folder = str(tmp_path)
    d.urls = urls or ['http://example.com/video']
    d.custom_filename = custom_filename
    d.mode = mode
    d.quality = 'The best'
    d.output_format = output_format
    d.is_playlist = False
    d.playlist_folder = None
    return d

def _extract_yt_dlp_command(calls):
    """Extract yt-dlp command from subprocess calls."""
    yt_calls = [c for c in calls if isinstance(c, list) and c and c[0] == 'yt-dlp']
    assert yt_calls, "yt-dlp was not called"
    return yt_calls[0]

def test_custom_filename_video(tmp_path, downloader_environment):
    d = _get_downloader(tmp_path, custom_filename='my_custom_name')
    d.download_video()

    cmd = _extract_yt_dlp_command(downloader_environment)
    assert '-o' in cmd
    out_idx = cmd.index('-o') + 1
    assert cmd[out_idx] == os.path.join(str(tmp_path), 'my_custom_name.%(ext)s')
    assert '--merge-output-format' in cmd
    assert '--no-playlist' in cmd

def test_custom_filename_audio(tmp_path, downloader_environment):
    d = _get_downloader(tmp_path, mode='Audio only', custom_filename='audio_name', output_format=None)
    d.download_video()

    cmd = _extract_yt_dlp_command(downloader_environment)
    assert '-o' in cmd
    out_idx = cmd.index('-o') + 1
    assert cmd[out_idx] == os.path.join(str(tmp_path), 'audio_name.%(ext)s')
    assert '--extract-audio' in cmd
    assert '--audio-format' in cmd
    assert '--audio-quality' in cmd
    assert '--no-playlist' in cmd

def test_download_notification_uses_output_path_without_custom_filename(
    tmp_path, downloader_environment, monkeypatch
):
    notifications = []
    monkeypatch.setattr(
        'src.classes.video_downloader.send_notification',
        lambda title, message: notifications.append((title, message)),
    )
    d = _get_downloader(tmp_path, custom_filename=None)

    d.download_video()

    assert notifications == [
        (
            'Successful download',
            f"Saved as: {os.path.join(str(tmp_path), '%(title)s.%(ext)s').replace('\\', '/')}",
        )
    ]

def test_custom_filename_notification_includes_resolved_extension(
    tmp_path, downloader_environment, monkeypatch
):
    notifications = []
    monkeypatch.setattr(
        'src.classes.video_downloader.send_notification',
        lambda title, message: notifications.append((title, message)),
    )
    d = _get_downloader(tmp_path, custom_filename='my_video')

    d.download_video()

    assert notifications == [
        (
            'Successful download',
            f"Saved as: {os.path.join(str(tmp_path), 'my_video.mp4').replace('\\', '/')}",
        )
    ]

def test_download_retries_with_optional_cookies_path(
    tmp_path, downloader_environment, monkeypatch
):
    cookies_path = tmp_path / 'browser-cookies.txt'
    cookies_path.write_text('cookies', encoding='utf-8')
    attempts = []

    def fail_once_then_succeed(args, **kwargs):
        if args[0] == 'ffmpeg':
            return MagicMock(returncode=0)
        attempts.append(args)
        return MagicMock(returncode=0)

    monkeypatch.setattr('src.classes.video_downloader.subprocess.run', fail_once_then_succeed)
    prompts = iter([
        {'use_cookies': True},
        {'cookies_path': str(cookies_path)},
    ])
    monkeypatch.setattr(
        'src.classes.video_downloader.inquirer.prompt',
        lambda *args, **kwargs: next(prompts),
    )

    d = _get_downloader(tmp_path)
    command = ['yt-dlp', '--cookies', '', 'http://example.com/video']
    assert d._retry_with_cookies(command, 'http://example.com/video') is True

    assert len(attempts) == 1
    cookies_index = attempts[0].index('--cookies') + 1
    assert attempts[0][cookies_index] == str(cookies_path)

def test_download_does_not_retry_when_cookies_prompt_is_declined(
    tmp_path, downloader_environment, monkeypatch
):
    attempts = []

    def fail_download(args, **kwargs):
        if args[0] == 'ffmpeg':
            return MagicMock(returncode=0)
        attempts.append(args)
        raise subprocess.CalledProcessError(1, args)

    monkeypatch.setattr('src.classes.video_downloader.subprocess.run', fail_download)
    monkeypatch.setattr(
        'src.classes.video_downloader.inquirer.prompt',
        lambda *args, **kwargs: {'use_cookies': False},
    )

    d = _get_downloader(tmp_path)
    d.download_video()

    assert len(attempts) == 1

def test_playlist_download_uses_playlist_folder(tmp_path, downloader_environment):
    playlist_url = 'http://example.com/watch?v=1&list=PL123'
    playlist_folder = tmp_path / 'playlist'

    d = _get_downloader(tmp_path, urls=[playlist_url], custom_filename=None)
    d.mode = 'Video'
    d.quality = 'The best'
    d.output_format = 'Mp4'
    d.is_playlist = True
    d.playlist_folder = str(playlist_folder)

    d.download_video()

    cmd = _extract_yt_dlp_command(downloader_environment)
    assert cmd[cmd.index('-o') + 1] == os.path.join(str(playlist_folder), '%(title)s.%(ext)s')
    assert '--no-playlist' not in cmd

def test_confirm_options_returns_true(monkeypatch):
    monkeypatch.setattr('src.classes.video_downloader.VideoDownloader.verify_download_folder', lambda self: None)
    d = _get_downloader(os.getcwd())
    d.urls = ['http://example.com/video']
    d.mode = 'Video'
    d.quality = 'The best'
    d.output_format = 'Mp4'
    d.download_folder = os.getcwd()
    d.custom_filename = 'custom_name'

    monkeypatch.setattr('src.classes.video_downloader.inquirer.prompt', lambda *args, **kwargs: {'confirm': True})
    assert d.confirm_options() is True

def test_verify_download_folder_creates_missing_folder(monkeypatch, tmp_path):
    download_path = tmp_path / 'new_download_folder'
    monkeypatch.setattr('src.classes.video_downloader.app_config.download_folder', str(download_path), raising=False)
    monkeypatch.setattr('src.classes.video_downloader.inquirer.prompt', lambda *args, **kwargs: {'use_default': True})

    d = VideoDownloader()
    assert d.download_folder == str(download_path)
    assert download_path.exists()

def test_sanitize_filename(monkeypatch):
    monkeypatch.setattr('src.classes.video_downloader.VideoDownloader.verify_download_folder', lambda self: None)
    d = VideoDownloader()
    bad = 'inva<>:"/\\|?*name '
    clean = d._sanitize_filename(bad)
    for ch in '<>:"/\\|?*':
        assert ch not in clean
    assert clean == 'inva_________name'

def test_load_yaml_profiles(tmp_path, monkeypatch):
    monkeypatch.setattr('src.classes.video_downloader.VideoDownloader.verify_download_folder', lambda self: None)
    config_path = tmp_path / 'downloads.yaml'
    config_path.write_text(
        '''
version: 1
downloads:
  - name: YouTube videos
    urls:
      - https://www.youtube.com/watch?v=VIDEO_ID
    output:
      folder: ./videos
      prefix: "[YT] "
      suffix: ""
    naming:
      template: "{prefix}{index:02d} - {title}{suffix}"
      indexing:
        enabled: true
        start: 3
        padding: 2
    media:
      type: video
      format: mkv
      quality: 1080p
''',
        encoding='utf-8',
    )

    profile = VideoDownloader()._load_yaml_profiles(str(config_path))[0]

    assert profile['name'] == 'YouTube videos'
    assert profile['urls'] == ['https://www.youtube.com/watch?v=VIDEO_ID']
    assert os.path.normpath(profile['folder']) == os.path.normpath('./videos')
    assert profile['mode'] == 'Video'
    assert profile['quality'] == '1080p'
    assert profile['output_format'] == 'mkv'

def test_txt_source_prompts_for_output_naming_and_media_options(
    tmp_path, monkeypatch
):
    monkeypatch.setattr(
        'src.classes.video_downloader.VideoDownloader.verify_download_folder',
        lambda self: None,
    )
    urls_path = tmp_path / 'urls.txt'
    urls_path.write_text('https://example.com/video\n', encoding='utf-8')
    answers = iter([
        {'source': 'TXT File'},
        {'file': str(urls_path)},
        {'name': 'TXT group'},
        {'folder': str(tmp_path / 'output'), 'prefix': '[YT] ', 'suffix': ''},
        {'template': '{prefix}{index:02d} - {title}{suffix}', 'indexing': True},
        {'start': '4', 'padding': '2'},
        {'type': 'audio'},
        {'format': 'mp3', 'quality': 'best'},
    ])
    monkeypatch.setattr(
        'src.classes.video_downloader.inquirer.prompt',
        lambda *args, **kwargs: next(answers),
    )

    downloader = VideoDownloader()
    downloader.prompt_user_options()

    profile = downloader.download_profiles[0]
    assert profile['name'] == 'TXT group'
    assert profile['folder'] == str(tmp_path / 'output')
    assert profile['prefix'] == '[YT] '
    assert profile['template'] == '{prefix}{index:02d} - {title}{suffix}'
    assert profile['indexing'] == {'enabled': True, 'start': 4, 'padding': 2}
    assert profile['mode'] == 'Audio only'
    assert profile['output_format'] == 'mp3'
    assert profile['quality'] == 'best'

def test_yaml_profile_generates_numbered_yt_dlp_template(
    tmp_path, downloader_environment
):
    d = _get_downloader(tmp_path, urls=['https://www.youtube.com/playlist?list=PL123'])
    d.download_profiles = [{
        'name': 'Anime',
        'urls': ['https://www.youtube.com/playlist?list=PL123'],
        'folder': str(tmp_path),
        'prefix': '',
        'suffix': '',
        'template': '{prefix}S01E{index:02d} - {title}{suffix}',
        'indexing': {'enabled': True, 'start': 1, 'padding': 2},
        'mode': 'Video',
        'quality': '1080p',
        'output_format': 'mkv',
        'audio_quality': 'best',
    }]

    d.download_video()

    cmd = _extract_yt_dlp_command(downloader_environment)
    assert cmd[cmd.index('-o') + 1] == os.path.join(
        str(tmp_path), 'S01E%(autonumber)02d - %(title)s.%(ext)s'
    )
    assert cmd[cmd.index('--autonumber-start') + 1] == '1'
    assert cmd[cmd.index('--merge-output-format') + 1] == 'mkv'
    assert '--no-playlist' not in cmd

def test_yaml_audio_profile_uses_selected_format_and_best_quality(
    tmp_path, downloader_environment
):
    d = _get_downloader(tmp_path, mode='Audio only', output_format=None)
    d.download_profiles = [{
        'name': 'Music',
        'urls': ['https://www.youtube.com/watch?v=MUSIC_ID'],
        'folder': str(tmp_path),
        'prefix': '',
        'suffix': '',
        'template': '{title}',
        'indexing': {'enabled': False, 'start': 1, 'padding': 2},
        'mode': 'Audio only',
        'quality': 'best',
        'output_format': 'mp3',
        'audio_quality': 'best',
    }]

    d.download_video()

    cmd = _extract_yt_dlp_command(downloader_environment)
    assert cmd[cmd.index('--audio-format') + 1] == 'mp3'
    assert cmd[cmd.index('--audio-quality') + 1] == '0'
    assert cmd[cmd.index('-o') + 1] == os.path.join(
        str(tmp_path), '%(title)s.%(ext)s'
    )
