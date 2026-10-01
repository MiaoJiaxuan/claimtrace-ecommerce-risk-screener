"""Shared pytest fixtures; fail closed on unmocked network connections."""

import pytest
import socket


@pytest.fixture(autouse=True)
def block_unmocked_http(monkeypatch: pytest.MonkeyPatch) -> None:
    """Fail closed if a test accidentally tries real HTTP access."""
    def reject_request(*args: object, **kwargs: object) -> None:
        raise AssertionError("Unmocked network request attempted during test")

    monkeypatch.setattr(socket.socket, "connect", reject_request)
    monkeypatch.setattr(socket, "create_connection", reject_request)
    try:
        import requests
    except ModuleNotFoundError:
        return
    monkeypatch.setattr(requests.sessions.Session, "request", reject_request)
