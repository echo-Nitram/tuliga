from sqlalchemy import Column, Integer, String

from . import Base


class Player(Base):
    """Persistent player statistics for leaderboard calculations."""

    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    team = Column(String, nullable=False)
    goals = Column(Integer, default=0, nullable=False)
    assists = Column(Integer, default=0, nullable=False)
