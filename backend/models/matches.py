from sqlalchemy import Column, Integer, String

from . import Base


class Match(Base):
    """Persistent match representation used for ranking calculations."""

    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    home = Column(String, nullable=False)
    away = Column(String, nullable=False)
    home_goals = Column(Integer, nullable=False)
    away_goals = Column(Integer, nullable=False)
