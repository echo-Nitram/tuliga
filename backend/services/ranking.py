from collections import defaultdict
from typing import Iterable, List, Dict

Match = Dict[str, int | str]

# Sample match data to illustrate ranking calculations
SAMPLE_MATCHES: List[Match] = [
    {"home": "Team A", "away": "Team B", "home_goals": 2, "away_goals": 1},
    {"home": "Team C", "away": "Team A", "home_goals": 0, "away_goals": 3},
    {"home": "Team B", "away": "Team C", "home_goals": 1, "away_goals": 1},
]


def calculate_ranking(matches: Iterable[Match]) -> List[Dict[str, int | str]]:
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
        home = m["home"]
        away = m["away"]
        hg = int(m["home_goals"])
        ag = int(m["away_goals"])

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
