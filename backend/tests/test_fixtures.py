import itertools

from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.core.fixtures import FixtureGenerator
from backend.routes.tournaments import router


app = FastAPI()
app.include_router(router)


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


def test_route_integration_round_robin():
    client = TestClient(app)
    response = client.post(
        "/tournaments",
        json={"name": "League", "teams": ["A", "B", "C", "D"], "format": "round_robin"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "League"
    # total matches should be 6 (4 choose 2)
    matches = [m for r in data["fixtures"] for m in r]
    assert len(matches) == 6


def test_route_integration_elimination():
    client = TestClient(app)
    response = client.post(
        "/tournaments",
        json={"name": "Cup", "teams": ["A", "B", "C", "D"], "format": "elimination"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["fixtures"][1][0] == ["Winner R1M1", "Winner R1M2"]
