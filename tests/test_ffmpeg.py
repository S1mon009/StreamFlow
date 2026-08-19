from unittest.mock import MagicMock
from src.decorators.ffmpeg import ffmpeg_required

@ffmpeg_required
def sample_action(x, y=0):
    return x + y

def test_ffmpeg_required_runs_when_ffmpeg_installed(monkeypatch):
    def fake_run(cmd, **kwargs):
        assert cmd == ['ffmpeg', '-version']
        return MagicMock(returncode=0)

    monkeypatch.setattr('src.decorators.ffmpeg.subprocess.run', fake_run)

    result = sample_action(2, y=3)

    assert result == 5

def test_ffmpeg_required_returns_none_when_ffmpeg_missing(monkeypatch):
    def fake_run(cmd, **kwargs):
        assert cmd == ['ffmpeg', '-version']
        raise FileNotFoundError()

    monkeypatch.setattr('src.decorators.ffmpeg.subprocess.run', fake_run)

    assert sample_action(2, y=3) is None
