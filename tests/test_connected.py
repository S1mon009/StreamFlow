import socket
import pytest
from src.decorators.connected import is_connected, network_required

"""
Fake socket implementation for testing network connectivity.
"""
class FakeSocket:
    def __init__(self, *args, **kwargs):
        self.connected = False

    def connect(self, addr):
        if addr == ('8.8.8.8', 53):
            self.connected = True
            return None
        raise socket.timeout()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

"""
Fake socket implementation that simulates a failed connection.
"""
class FakeSocketFail(FakeSocket):
    def connect(self, addr):
        raise socket.error("network unreachable")

def test_is_connected_success(monkeypatch):
    monkeypatch.setattr('src.decorators.connected.socket.setdefaulttimeout', lambda timeout: None)
    monkeypatch.setattr('src.decorators.connected.socket.socket', FakeSocket)

    assert is_connected() is True


def test_is_connected_failure(monkeypatch):
    monkeypatch.setattr('src.decorators.connected.socket.setdefaulttimeout', lambda timeout: None)
    monkeypatch.setattr('src.decorators.connected.socket.socket', FakeSocketFail)

    assert is_connected() is False


def test_network_required_retries_until_connected(monkeypatch):
    calls = []
    states = [False, False, True]

    def fake_is_connected(*args, **kwargs):
        calls.append('check')
        return states.pop(0)

    sleep_calls = []

    monkeypatch.setattr('src.decorators.connected.is_connected', fake_is_connected)
    monkeypatch.setattr('src.decorators.connected.time.sleep', lambda seconds: sleep_calls.append(seconds))

    @network_required
    def target(value):
        return f"done:{value}"

    result = target('x')

    assert result == 'done:x'
    assert calls == ['check', 'check', 'check']
    assert sleep_calls == [5, 5]


def test_network_required_executes_immediately_when_connected(monkeypatch):
    monkeypatch.setattr('src.decorators.connected.is_connected', lambda *args, **kwargs: True)
    monkeypatch.setattr('src.decorators.connected.time.sleep', lambda seconds: pytest.skip('sleep should not be called'))

    executed = []

    @network_required
    def target(value):
        executed.append(value)
        return 'ok'

    result = target(123)

    assert result == 'ok'
    assert executed == [123]
