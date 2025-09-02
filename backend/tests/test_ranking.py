from backend.models import SessionLocal
from backend.models.matches import Match


def _insert_sample_matches():
    db = SessionLocal()
    db.add_all(
        [
            Match(home="Team A", away="Team B", home_goals=2, away_goals=1),
            Match(home="Team C", away="Team A", home_goals=0, away_goals=3),
            Match(home="Team B", away="Team C", home_goals=1, away_goals=1),
        ]
    )
    db.commit()
    db.close()


def test_ranking_endpoint_returns_sorted_table(client):
    _insert_sample_matches()
    resp = client.get("/ranking")
    assert resp.status_code == 200
    table = resp.json()
    assert len(table) == 3
    assert table[0]["team"] == "Team A"
    assert table[0]["points"] == 6
    assert table[1]["team"] == "Team B"
    assert table[2]["team"] == "Team C"
