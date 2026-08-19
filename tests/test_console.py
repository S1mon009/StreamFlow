from src.utils.console import clear_console

def test_clear_console_uses_cls_on_windows(monkeypatch):
    called = []

    class FakeOS:
        name = 'nt'

        @staticmethod
        def system(command):
            called.append(command)
            return 0

    monkeypatch.setattr('src.utils.console.os', FakeOS)

    clear_console()

    assert called == ['cls']

def test_clear_console_uses_clear_on_unix(monkeypatch):
    called = []

    class FakeOS:
        name = 'posix'

        @staticmethod
        def system(command):
            called.append(command)
            return 0

    monkeypatch.setattr('src.utils.console.os', FakeOS)

    clear_console()

    assert called == ['clear']
