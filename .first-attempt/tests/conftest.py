import pytest


@pytest.fixture
def tmp_home(tmp_path, monkeypatch):
    """Redirect $HOME so anything that calls Path.expanduser() lands in tmp."""
    monkeypatch.setenv("HOME", str(tmp_path))
    return tmp_path
