"""Routes for referee CRUD and match planning."""
from __future__ import annotations

import itertools
from datetime import date
from typing import Dict, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..models.referees import Availability, Match, Referee

router = APIRouter(prefix="/referees")

# in-memory storage
_referees: Dict[int, Referee] = {}
_availability: Dict[int, set[date]] = {}
_id_sequence = itertools.count(1)


class RefereeCreate(BaseModel):
    name: str
    level: str = "regional"


@router.post("", response_model=Referee)
def create_referee(payload: RefereeCreate) -> Referee:
    referee_id = next(_id_sequence)
    referee = Referee(id=referee_id, **payload.dict())
    _referees[referee_id] = referee
    return referee


@router.get("", response_model=List[Referee])
def list_referees() -> List[Referee]:
    return list(_referees.values())


@router.get("/{referee_id}", response_model=Referee)
def get_referee(referee_id: int) -> Referee:
    referee = _referees.get(referee_id)
    if not referee:
        raise HTTPException(status_code=404, detail="Referee not found")
    return referee


@router.put("/{referee_id}", response_model=Referee)
def update_referee(referee_id: int, payload: RefereeCreate) -> Referee:
    if referee_id not in _referees:
        raise HTTPException(status_code=404, detail="Referee not found")
    referee = Referee(id=referee_id, **payload.dict())
    _referees[referee_id] = referee
    return referee


@router.delete("/{referee_id}")
def delete_referee(referee_id: int) -> dict:
    if referee_id not in _referees:
        raise HTTPException(status_code=404, detail="Referee not found")
    _referees.pop(referee_id)
    _availability.pop(referee_id, None)
    return {"status": "deleted"}


class AvailabilityRequest(BaseModel):
    date: date


@router.post("/{referee_id}/availability", response_model=Availability)
def add_availability(referee_id: int, payload: AvailabilityRequest) -> Availability:
    if referee_id not in _referees:
        raise HTTPException(status_code=404, detail="Referee not found")
    _availability.setdefault(referee_id, set()).add(payload.date)
    return Availability(referee_id=referee_id, date=payload.date)


@router.get("/{referee_id}/availability", response_model=List[Availability])
def list_availability(referee_id: int) -> List[Availability]:
    if referee_id not in _referees:
        raise HTTPException(status_code=404, detail="Referee not found")
    dates = _availability.get(referee_id, set())
    return [Availability(referee_id=referee_id, date=d) for d in sorted(dates)]


class MatchCreate(BaseModel):
    home: str
    away: str
    date: date


@router.post("/schedule", response_model=List[Match])
def schedule_matches(matches: List[MatchCreate]) -> List[Match]:
    assigned: List[Match] = []
    for match in matches:
        referee_id = next((rid for rid, dates in _availability.items() if match.date in dates), None)
        if referee_id is None:
            raise HTTPException(status_code=400, detail=f"No referee available for {match.date}")
        _availability[referee_id].remove(match.date)
        assigned.append(Match(**match.dict(), referee_id=referee_id))
    return assigned
