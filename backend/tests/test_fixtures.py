import itertools

from backend.core.fixtures import FixtureGenerator


def test_round_robin_generator():
    teams = ["A", "B", "C", "D"]
    generator = FixtureGenerator(teams)
    schedule = generator.round_robin()
    pairs = [tuple(sorted(match)) for round_ in schedule for match in round_]
    expected_pairs = set(itertools.combinations(teams, 2))
    assert set(pairs) == expected_pairs


def test_elimination_generator():
    teams = ["A", "B", "C", "D"]
    generator = FixtureGenerator(teams)
    bracket = generator.elimination()
    assert len(bracket) == 2  # semi-finals and final
    assert len(bracket[0]) == 2
    assert bracket[1][0] == ("Winner R1M1", "Winner R1M2")


def test_route_tournament_crud(client):
    # Create teams first
    teams = []
    for name, city in [("Team A", "City A"), ("Team B", "City B"), ("Team C", "City C"), ("Team D", "City D")]:
        resp = client.post("/teams", json={"name": name, "city": city})
        assert resp.status_code == 201
        teams.append(resp.json())

    # Create tournament
    resp = client.post("/tournaments", json={"name": "League", "format": "round_robin"})
    assert resp.status_code == 201
    tournament = resp.json()
    tournament_id = tournament["id"]

    # Register teams
    for t in teams:
        resp = client.post(f"/tournaments/{tournament_id}/teams", json={"team_id": t["id"]})
        assert resp.status_code == 201

    # Generate fixtures
    resp = client.post(f"/tournaments/{tournament_id}/generate")
    assert resp.status_code == 200
    fixtures = resp.json()
    assert len(fixtures) == 6  # 4 choose 2

    # List fixtures
    resp = client.get(f"/tournaments/{tournament_id}/fixtures")
    assert resp.status_code == 200
    assert len(resp.json()) == 6
