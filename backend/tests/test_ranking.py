from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.routes.ranking import router

app = FastAPI()
app.include_router(router)


def test_ranking_endpoint_returns_sorted_table():
    client = TestClient(app)
    resp = client.get("/ranking")
    assert resp.status_code == 200
    table = resp.json()
    assert len(table) > 0
    points = [row["points"] for row in table]
    assert points == sorted(points, reverse=True)
