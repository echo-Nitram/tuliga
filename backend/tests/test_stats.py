from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

from backend.routes.stats import router
from backend.models import Base, engine, SessionLocal
from backend.models.players import Player
from backend.models.matches import Match

app = FastAPI()
app.include_router(router)


def _setup_sample_data():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    db.add_all(
        [
            Player(name="Juan Pérez", team="Team A", goals=12, assists=5),
            Player(name="Carlos Gómez", team="Team B", goals=10, assists=7),
            Player(name="Luis Rodríguez", team="Team C", goals=9, assists=4),
        ]
    )
    db.add_all(
        [
            Match(home="Team A", away="Team B", home_goals=2, away_goals=1),
            Match(home="Team C", away="Team A", home_goals=0, away_goals=3),
            Match(home="Team B", away="Team C", home_goals=1, away_goals=1),
        ]
    )
    db.commit()
    db.close()


def test_get_summary_stats():
    _setup_sample_data()
    client = TestClient(app)
    resp = client.get("/stats/summary")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_teams"] == 3
    assert data["total_players"] == 3
    assert data["total_matches"] == 3
    assert data["avg_goals_per_match"] == pytest.approx(8 / 3)


def test_get_top_players():
    _setup_sample_data()
    client = TestClient(app)
    resp = client.get("/stats/players/top")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 3
    assert data[0]["player"] == "Juan Pérez"
    assert data[0]["goals"] == 12
    assert data[0]["goals"] >= data[1]["goals"] >= data[2]["goals"]
