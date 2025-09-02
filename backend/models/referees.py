"""Domain models for referee management."""
from __future__ import annotations

from datetime import date
from pydantic import BaseModel


class Referee(BaseModel):
    """Represents a match official."""
    id: int
    name: str
    level: str = "regional"


class Availability(BaseModel):
    """Availability entry for a referee on a given date."""
    referee_id: int
    date: date


class Match(BaseModel):
    """Simplified match representation with assigned referee."""
    home: str
    away: str
    date: date
    referee_id: int | None = None
