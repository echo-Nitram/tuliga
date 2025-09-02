"""Tournament routes for fixture generation."""
from fastapi import APIRouter
from pydantic import BaseModel

from ..core.fixtures import FixtureGenerator

router = APIRouter()


class TournamentCreate(BaseModel):
    name: str
    teams: list[str]
    format: str = "round_robin"


@router.post("/tournaments")
def create_tournament(tournament: TournamentCreate) -> dict:
    generator = FixtureGenerator(tournament.teams)
    if tournament.format == "elimination":
        fixtures = generator.elimination()
    else:
        fixtures = generator.round_robin()
    return {"name": tournament.name, "fixtures": fixtures}
