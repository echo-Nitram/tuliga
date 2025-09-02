"""Routes for referee CRUD and match planning."""
from __future__ import annotations

from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..models import SessionLocal
from ..models.referees import (
    Availability,
    AvailabilitySchema,
    Match,
    Referee,
    RefereeSchema,
)

router = APIRouter(prefix="/referees")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class RefereeCreate(BaseModel):
    name: str
    level: str = "regional"


@router.post("", response_model=RefereeSchema)
def create_referee(payload: RefereeCreate, db: Session = Depends(get_db)) -> Referee:
    referee = Referee(name=payload.name, level=payload.level)
    db.add(referee)
    db.commit()
    db.refresh(referee)
    return referee


@router.get("", response_model=List[RefereeSchema])
def list_referees(db: Session = Depends(get_db)) -> List[Referee]:
    return db.query(Referee).all()


@router.get("/{referee_id}", response_model=RefereeSchema)
def get_referee(referee_id: int, db: Session = Depends(get_db)) -> Referee:
    referee = db.get(Referee, referee_id)
    if not referee:
        raise HTTPException(status_code=404, detail="Referee not found")
    return referee


@router.put("/{referee_id}", response_model=RefereeSchema)
def update_referee(
    referee_id: int, payload: RefereeCreate, db: Session = Depends(get_db)
) -> Referee:
    referee = db.get(Referee, referee_id)
    if not referee:
        raise HTTPException(status_code=404, detail="Referee not found")
    referee.name = payload.name
    referee.level = payload.level
    db.commit()
    db.refresh(referee)
    return referee


@router.delete("/{referee_id}")
def delete_referee(referee_id: int, db: Session = Depends(get_db)) -> dict:
    referee = db.get(Referee, referee_id)
    if not referee:
        raise HTTPException(status_code=404, detail="Referee not found")
    db.delete(referee)
    db.commit()
    return {"status": "deleted"}


class AvailabilityRequest(BaseModel):
    date: date


@router.post("/{referee_id}/availability", response_model=AvailabilitySchema)
def add_availability(
    referee_id: int, payload: AvailabilityRequest, db: Session = Depends(get_db)
) -> Availability:
    if not db.get(Referee, referee_id):
        raise HTTPException(status_code=404, detail="Referee not found")
    availability = Availability(referee_id=referee_id, date=payload.date)
    db.merge(availability)
    db.commit()
    return availability


@router.get("/{referee_id}/availability", response_model=List[AvailabilitySchema])
def list_availability(referee_id: int, db: Session = Depends(get_db)) -> List[Availability]:
    if not db.get(Referee, referee_id):
        raise HTTPException(status_code=404, detail="Referee not found")
    return (
        db.query(Availability)
        .filter(Availability.referee_id == referee_id)
        .order_by(Availability.date)
        .all()
    )


class MatchCreate(BaseModel):
    home: str
    away: str
    date: date


@router.post("/schedule", response_model=List[Match])
def schedule_matches(
    matches: List[MatchCreate], db: Session = Depends(get_db)
) -> List[Match]:
    assigned: List[Match] = []
    for match in matches:
        avail = (
            db.query(Availability)
            .filter(Availability.date == match.date)
            .first()
        )
        if avail is None:
            raise HTTPException(
                status_code=400, detail=f"No referee available for {match.date}"
            )
        referee_id = avail.referee_id
        db.delete(avail)
        db.commit()
        assigned.append(Match(**match.dict(), referee_id=referee_id))
    return assigned
