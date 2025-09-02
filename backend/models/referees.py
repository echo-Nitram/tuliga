"""Database models for referee management and scheduling."""
from __future__ import annotations

from datetime import date as Date

from pydantic import BaseModel
from sqlalchemy import Column, Date as SA_Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from . import Base


class Referee(Base):
    """Referee persisted in the database."""

    __tablename__ = "referees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    level = Column(String, nullable=False, default="regional")

    availability = relationship(
        "Availability", back_populates="referee", cascade="all, delete-orphan"
    )


class Availability(Base):
    """Availability entry for a referee on a specific date."""

    __tablename__ = "availability"

    referee_id = Column(
        Integer, ForeignKey("referees.id", ondelete="CASCADE"), primary_key=True
    )
    date = Column(SA_Date, primary_key=True)

    referee = relationship("Referee", back_populates="availability")


class Match(Base):
    """Scheduled match with an assigned referee."""

    __tablename__ = "referee_matches"

    id = Column(Integer, primary_key=True, index=True)
    home = Column(String, nullable=False)
    away = Column(String, nullable=False)
    date = Column(SA_Date, nullable=False)
    referee_id = Column(Integer, ForeignKey("referees.id", ondelete="SET NULL"))

    referee = relationship("Referee")


class MatchSchema(BaseModel):
    """Pydantic schema for serialising scheduled matches."""

    id: int
    home: str
    away: str
    date: Date
    referee_id: int | None = None

    class Config:
        orm_mode = True


class RefereeSchema(BaseModel):
    """Pydantic schema for serialising referees."""

    id: int
    name: str
    level: str

    class Config:
        orm_mode = True


class AvailabilitySchema(BaseModel):
    """Pydantic schema for serialising availability entries."""

    referee_id: int
    date: Date

    class Config:
        orm_mode = True


__all__ = [
    "Referee",
    "Availability",
    "Match",
    "MatchSchema",
    "RefereeSchema",
    "AvailabilitySchema",
]

