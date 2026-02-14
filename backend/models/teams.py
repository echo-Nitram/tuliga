"""Database model for teams."""
from __future__ import annotations

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from . import Base


class Team(Base):
    """A team participating in tournaments."""

    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    city = Column(String, nullable=False)
    coach = Column(String, nullable=True)

    players = relationship("Player", back_populates="team_rel")
    registrations = relationship(
        "Registration", back_populates="team", cascade="all, delete-orphan"
    )
