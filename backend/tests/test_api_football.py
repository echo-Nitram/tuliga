from fastapi.testclient import TestClient

from backend.app.main import app
from backend.services import api_football


def test_external_leagues(monkeypatch):
    def fake_get(url, headers=None, params=None, timeout=None):
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
