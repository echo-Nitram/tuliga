from datetime import date

from backend.models import SessionLocal
from backend.models.referees import Match


def test_referee_crud_flow(client):
    # create
    resp = client.post("/referees", json={"name": "Ana", "level": "senior"})
    assert resp.status_code == 200
    referee = resp.json()
    rid = referee["id"]
    # read
    assert client.get(f"/referees/{rid}").json()["name"] == "Ana"
    # update
    resp = client.put(f"/referees/{rid}", json={"name": "Ana B", "level": "senior"})
    assert resp.json()["name"] == "Ana B"
    # list
    assert len(client.get("/referees").json()) == 1
    # delete
    assert client.delete(f"/referees/{rid}").status_code == 200
    assert client.get(f"/referees/{rid}").status_code == 404
    assert client.get("/referees").json() == []


def test_schedule_with_availability(client):
    # create referee and availability
    rid = client.post("/referees", json={"name": "Luis"}).json()["id"]
    avail_date = date(2024, 1, 1).isoformat()
    client.post(f"/referees/{rid}/availability", json={"date": avail_date})
    assert client.get(f"/referees/{rid}/availability").json() == [
        {"referee_id": rid, "date": avail_date}
    ]
    # plan match
    resp = client.post(
        "/referees/schedule",
        json=[{"home": "A", "away": "B", "date": avail_date}],
    )
    assert resp.status_code == 200
    assigned = resp.json()[0]
    assert assigned["referee_id"] == rid
    assert client.get(f"/referees/{rid}/availability").json() == []

    db = SessionLocal()
    stored = db.query(Match).all()
    assert len(stored) == 1
    persisted = stored[0]
    assert persisted.home == "A"
    assert persisted.away == "B"
    assert persisted.referee_id == rid
    assert persisted.date.isoformat() == avail_date
    db.close()

