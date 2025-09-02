from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.routes.stats import router

app = FastAPI()
app.include_router(router)


def test_get_summary_stats():
    client = TestClient(app)
    resp = client.get("/stats/summary")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_teams"] == 12
    assert data["avg_goals_per_match"] == 3.2


def test_get_top_players():
    client = TestClient(app)
    resp = client.get("/stats/players/top")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert data[0]["goals"] >= data[1]["goals"]
