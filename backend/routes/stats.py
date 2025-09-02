from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..models import SessionLocal
from ..models.matches import Match
from ..models.players import Player

router = APIRouter(prefix="/stats", tags=["stats"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/summary")
def get_summary_stats(db: Session = Depends(get_db)):
    """Return consolidated summary statistics for the dashboard."""
    total_teams = db.query(func.count(func.distinct(Player.team))).scalar() or 0
    total_players = db.query(func.count(Player.id)).scalar() or 0
    total_matches = db.query(func.count(Match.id)).scalar() or 0
    total_goals = db.query(func.coalesce(func.sum(Match.home_goals + Match.away_goals), 0)).scalar()
    avg_goals_per_match = total_goals / total_matches if total_matches else 0

    return {
        "total_teams": total_teams,
        "total_players": total_players,
        "total_matches": total_matches,
        "avg_goals_per_match": avg_goals_per_match,
    }


@router.get("/players/top")
def get_top_players(db: Session = Depends(get_db)):
    """Return top players ordered by goals scored."""
    players = (
        db.query(Player)
        .order_by(Player.goals.desc())
        .limit(10)
        .all()
    )
    return [
        {"player": p.name, "goals": p.goals, "assists": p.assists} for p in players
    ]
