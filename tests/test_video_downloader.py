import os
import pytest
from unittest.mock import MagicMock
from classes.video_downloader import VideoDownloader


@pytest.fixture
def mock_subprocess(monkeypatch):
    """Mock subprocess.run and network decorator."""
    calls = []
    
    def fake_run(args, **kwargs):
        calls.append(args)
        return MagicMock(returncode=0)
    
    monkeypatch.setattr('decorators.ffmpeg.subprocess.run', fake_run)
    monkeypatch.setattr('decorators.connected.is_connected', lambda *a, **k: True)
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
    return d


def _extract_yt_dlp_command(calls):
    """Extract yt-dlp command from subprocess calls."""
    yt_calls = [c for c in calls if isinstance(c, list) and c and c[0] == 'yt-dlp']
    assert yt_calls, "yt-dlp was not called"
    return yt_calls[0]


def test_custom_filename_video(tmp_path, mock_subprocess):
    d = _get_downloader(tmp_path, custom_filename='my_custom_name')
    d.download_video()

    cmd = _extract_yt_dlp_command(mock_subprocess)
    assert '-o' in cmd
    out_idx = cmd.index('-o') + 1
    assert cmd[out_idx] == os.path.join(str(tmp_path), 'my_custom_name.%(ext)s')


def test_custom_filename_audio(tmp_path, mock_subprocess):
    d = _get_downloader(tmp_path, mode='Audio only', custom_filename='audio_name', output_format=None)
    d.download_video()

    cmd = _extract_yt_dlp_command(mock_subprocess)
    assert '-o' in cmd
    out_idx = cmd.index('-o') + 1
    assert cmd[out_idx] == os.path.join(str(tmp_path), 'audio_name.%(ext)s')
    assert '--extract-audio' in cmd
    assert '--audio-format' in cmd




def test_sanitize_filename():
    d = VideoDownloader()
    bad = 'inva<>:"/\\|?*name '
    clean = d._sanitize_filename(bad)
    for ch in '<>:"/\\|?*':
        assert ch not in clean
    assert clean.strip() == clean
