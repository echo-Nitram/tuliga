"""Tournament routes with full CRUD and fixture persistence."""
from __future__ import annotations

from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from ..core.fixtures import FixtureGenerator
from ..models import SessionLocal
from ..models.tournaments import Fixture, Registration, Tournament

router = APIRouter(prefix="/tournaments", tags=["tournaments"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class TournamentCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=200)
    format: str = Field("round_robin", pattern="^(round_robin|elimination)$")


class TournamentOut(BaseModel):
    id: int
    name: str
    format: str
    status: str
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class FixtureOut(BaseModel):
    id: int
    round: int
    home: str
    away: str
    home_goals: int | None = None
    away_goals: int | None = None

    model_config = ConfigDict(from_attributes=True)


class RegisterTeamRequest(BaseModel):
    team_id: int


class FixtureScoreUpdate(BaseModel):
    home_goals: int = Field(..., ge=0)
    away_goals: int = Field(..., ge=0)


@router.post("", response_model=TournamentOut, status_code=201)
def create_tournament(payload: TournamentCreate, db: Session = Depends(get_db)):
    tournament = Tournament(name=payload.name, format=payload.format)
    db.add(tournament)
    db.commit()
    db.refresh(tournament)
    return TournamentOut.model_validate(tournament)


@router.get("", response_model=List[TournamentOut])
def list_tournaments(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    tournaments = db.query(Tournament).offset(skip).limit(limit).all()
    return [TournamentOut.model_validate(t) for t in tournaments]


@router.get("/{tournament_id}", response_model=TournamentOut)
def get_tournament(tournament_id: int, db: Session = Depends(get_db)):
    t = db.get(Tournament, tournament_id)
    if not t:
        raise HTTPException(status_code=404, detail="Tournament not found")
    return TournamentOut.model_validate(t)


@router.delete("/{tournament_id}")
def delete_tournament(tournament_id: int, db: Session = Depends(get_db)):
    t = db.get(Tournament, tournament_id)
    if not t:
        raise HTTPException(status_code=404, detail="Tournament not found")
    db.delete(t)
    db.commit()
    return {"status": "deleted"}


@router.post("/{tournament_id}/teams", status_code=201)
def register_team(
    tournament_id: int, payload: RegisterTeamRequest, db: Session = Depends(get_db)
):
    t = db.get(Tournament, tournament_id)
    if not t:
        raise HTTPException(status_code=404, detail="Tournament not found")
    exists = (
        db.query(Registration)
        .filter(
            Registration.tournament_id == tournament_id,
            Registration.team_id == payload.team_id,
        )
        .first()
    )
    if exists:
        raise HTTPException(status_code=400, detail="Team already registered")
    reg = Registration(tournament_id=tournament_id, team_id=payload.team_id)
    db.add(reg)
    db.commit()
    db.refresh(reg)
    return {"id": reg.id, "tournament_id": reg.tournament_id, "team_id": reg.team_id}


@router.post("/{tournament_id}/generate", response_model=List[FixtureOut])
def generate_fixtures(tournament_id: int, db: Session = Depends(get_db)):
    """Generate and persist fixtures for a tournament."""
    t = db.get(Tournament, tournament_id)
    if not t:
        raise HTTPException(status_code=404, detail="Tournament not found")

    regs = (
        db.query(Registration).filter(Registration.tournament_id == tournament_id).all()
    )
    if len(regs) < 2:
        raise HTTPException(status_code=400, detail="Need at least 2 registered teams")

    from ..models.teams import Team

    team_names = []
    for reg in regs:
        team = db.get(Team, reg.team_id)
        if team:
            team_names.append(team.name)

    # Clear any previous fixtures
    db.query(Fixture).filter(Fixture.tournament_id == tournament_id).delete()

    generator = FixtureGenerator(team_names)
    if t.format == "elimination":
        rounds = generator.elimination()
    else:
        rounds = generator.round_robin()

    fixtures = []
    for round_num, matches in enumerate(rounds, 1):
        for home, away in matches:
            f = Fixture(
                tournament_id=tournament_id,
                round=round_num,
                home=home,
                away=away,
            )
            db.add(f)
            fixtures.append(f)

    t.status = "in_progress"
    db.commit()
    for f in fixtures:
        db.refresh(f)
    return [FixtureOut.model_validate(f) for f in fixtures]


@router.get("/{tournament_id}/fixtures", response_model=List[FixtureOut])
def list_fixtures(tournament_id: int, db: Session = Depends(get_db)):
    t = db.get(Tournament, tournament_id)
    if not t:
        raise HTTPException(status_code=404, detail="Tournament not found")
    fixtures = (
        db.query(Fixture)
        .filter(Fixture.tournament_id == tournament_id)
        .order_by(Fixture.round, Fixture.id)
        .all()
    )
    return [FixtureOut.model_validate(f) for f in fixtures]


@router.put("/{tournament_id}/fixtures/{fixture_id}", response_model=FixtureOut)
def update_fixture_score(
    tournament_id: int,
    fixture_id: int,
    payload: FixtureScoreUpdate,
    db: Session = Depends(get_db),
):
    f = (
        db.query(Fixture)
        .filter(Fixture.id == fixture_id, Fixture.tournament_id == tournament_id)
        .first()
    )
    if not f:
        raise HTTPException(status_code=404, detail="Fixture not found")
    f.home_goals = payload.home_goals
    f.away_goals = payload.away_goals
    db.commit()
    db.refresh(f)
    return FixtureOut.model_validate(f)
