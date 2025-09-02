"""Tests for the API-Football service integration."""
from fastapi.testclient import TestClient
import pytest


def test_external_leagues(monkeypatch):
    """Ensure the endpoint returns data when the API key is set."""
    monkeypatch.setenv("API_FOOTBALL_KEY", "test-key")

    # Import after setting the environment variable so the endpoint uses the test key
    from backend.app.main import app  # pylint: disable=import-error
    import backend.services.api_football as api_football

    def fake_get(url, headers=None, params=None, timeout=None):  # noqa: D401
        class FakeResp:
            def raise_for_status(self):
                pass

            def json(self):
                return {"response": [{"league": {"name": "Test League"}}]}

        return FakeResp()

    monkeypatch.setattr(api_football.requests, "get", fake_get)
    client = TestClient(app)
    resp = client.get("/external-leagues")
    assert resp.status_code == 200
    assert resp.json()["response"][0]["league"]["name"] == "Test League"


def test_missing_api_key(monkeypatch):
    """fetch_leagues should raise if the API key is absent."""
    monkeypatch.delenv("API_FOOTBALL_KEY", raising=False)
    from backend.services import api_football

    with pytest.raises(RuntimeError):
        api_football.fetch_leagues()

