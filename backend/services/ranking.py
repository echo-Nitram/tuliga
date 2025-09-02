from collections import defaultdict
from typing import Iterable, List, Dict

from sqlalchemy.orm import Session

from ..models.matches import Match


def calculate_ranking(matches: Iterable[Match | Dict[str, int | str]]) -> List[Dict[str, int | str]]:
    """Aggregate match results into a ranking table.

    Teams are ordered by points, goal difference and goals scored.
    """
    stats: Dict[str, Dict[str, int]] = defaultdict(
        lambda: {
            "played": 0,
            "wins": 0,
            "draws": 0,
            "losses": 0,
            "goals_for": 0,
            "goals_against": 0,
            "points": 0,
        }
    )

    for m in matches:
        if isinstance(m, dict):
            home = m["home"]
            away = m["away"]
            hg = int(m["home_goals"])
            ag = int(m["away_goals"])
        else:
            home = m.home
            away = m.away
            hg = int(m.home_goals)
            ag = int(m.away_goals)

        stats[home]["played"] += 1
        stats[away]["played"] += 1
        stats[home]["goals_for"] += hg
        stats[home]["goals_against"] += ag
        stats[away]["goals_for"] += ag
        stats[away]["goals_against"] += hg

        if hg > ag:
            stats[home]["wins"] += 1
            stats[away]["losses"] += 1
            stats[home]["points"] += 3
        elif hg < ag:
            stats[away]["wins"] += 1
            stats[home]["losses"] += 1
            stats[away]["points"] += 3
        else:
            stats[home]["draws"] += 1
            stats[away]["draws"] += 1
            stats[home]["points"] += 1
            stats[away]["points"] += 1

    table = []
    for team, s in stats.items():
        s["goal_difference"] = s["goals_for"] - s["goals_against"]
        table.append({"team": team, **s})

    return sorted(
        table,
        key=lambda t: (t["points"], t["goal_difference"], t["goals_for"]),
        reverse=True,
    )


def get_ranking(db: Session) -> List[Dict[str, int | str]]:
    """Fetch matches from the database and compute the ranking table."""
    matches = db.query(Match).all()
    return calculate_ranking(matches)
