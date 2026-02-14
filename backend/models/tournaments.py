"""Database models for tournaments and registrations."""
from __future__ import annotations

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from . import Base


class Tournament(Base):
    """A tournament with a specific format and set of teams."""

    __tablename__ = "tournaments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    format = Column(String, nullable=False, default="round_robin")
    status = Column(String, nullable=False, default="draft")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    registrations = relationship(
        "Registration", back_populates="tournament", cascade="all, delete-orphan"
    )
    fixtures = relationship(
        "Fixture", back_populates="tournament", cascade="all, delete-orphan"
    )


class Registration(Base):
    """Links a team to a tournament."""

    __tablename__ = "registrations"

    id = Column(Integer, primary_key=True, index=True)
    tournament_id = Column(
        Integer, ForeignKey("tournaments.id", ondelete="CASCADE"), nullable=False
    )
    team_id = Column(
        Integer, ForeignKey("teams.id", ondelete="CASCADE"), nullable=False
    )

    tournament = relationship("Tournament", back_populates="registrations")
    team = relationship("Team", back_populates="registrations")


class Fixture(Base):
    """A scheduled match within a tournament."""

    __tablename__ = "fixtures"

    id = Column(Integer, primary_key=True, index=True)
    tournament_id = Column(
        Integer, ForeignKey("tournaments.id", ondelete="CASCADE"), nullable=False
    )
    round = Column(Integer, nullable=False)
    home = Column(String, nullable=False)
    away = Column(String, nullable=False)
    home_goals = Column(Integer, nullable=True)
    away_goals = Column(Integer, nullable=True)

    tournament = relationship("Tournament", back_populates="fixtures")
