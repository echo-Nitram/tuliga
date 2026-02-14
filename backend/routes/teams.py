"""CRUD routes for teams."""
from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from ..models import SessionLocal
from ..models.teams import Team

router = APIRouter(prefix="/teams", tags=["teams"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class TeamCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    city: str = Field(..., min_length=2, max_length=100)
    coach: str | None = None


class TeamOut(BaseModel):
    id: int
    name: str
    city: str
    coach: str | None = None

    model_config = ConfigDict(from_attributes=True)


@router.post("", response_model=TeamOut, status_code=201)
def create_team(payload: TeamCreate, db: Session = Depends(get_db)):
    if db.query(Team).filter(Team.name == payload.name).first():
        raise HTTPException(status_code=400, detail="Team name already exists")
    team = Team(**payload.model_dump())
    db.add(team)
    db.commit()
    db.refresh(team)
    return TeamOut.model_validate(team)


@router.get("", response_model=List[TeamOut])
def list_teams(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    teams = db.query(Team).offset(skip).limit(limit).all()
    return [TeamOut.model_validate(t) for t in teams]


@router.get("/{team_id}", response_model=TeamOut)
def get_team(team_id: int, db: Session = Depends(get_db)):
    team = db.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return TeamOut.model_validate(team)


@router.put("/{team_id}", response_model=TeamOut)
def update_team(team_id: int, payload: TeamCreate, db: Session = Depends(get_db)):
    team = db.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    team.name = payload.name
    team.city = payload.city
    team.coach = payload.coach
    db.commit()
    db.refresh(team)
    return TeamOut.model_validate(team)


@router.delete("/{team_id}")
def delete_team(team_id: int, db: Session = Depends(get_db)):
    team = db.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    db.delete(team)
    db.commit()
    return {"status": "deleted"}
