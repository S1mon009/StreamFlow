import time
from src.decorators.timed import timed

def test_timed_decorator_prints_seconds(monkeypatch, capsys):
    def fake_time():
        yield 100.0
        yield 105.423

    generator = fake_time()

    def fake_time_func():
        return next(generator)

    @timed
    def sample(x):
        return x * 2

    monkeypatch.setattr(time, 'time', fake_time_func)

    result = sample(3)

    assert result == 6
    captured = capsys.readouterr()
    assert 'Download time: 5.42 seconds.' in captured.out

def test_timed_decorator_prints_minutes(monkeypatch, capsys):
    def fake_time():
        yield 100.0
        yield 4600.0

    generator = fake_time()

    def fake_time_func():
        return next(generator)

    @timed
    def sample(x):
        return x + 1

    monkeypatch.setattr(time, 'time', fake_time_func)

    result = sample(4)

    assert result == 5
    captured = capsys.readouterr()
    assert 'Download time: 75.00 minutes.' in captured.out
