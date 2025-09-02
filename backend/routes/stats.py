from fastapi import APIRouter

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/summary")
def get_summary_stats():
    """Return consolidated summary statistics for the dashboard."""
    return {
        "total_teams": 12,
        "total_players": 240,
        "total_matches": 66,
        "avg_goals_per_match": 3.2,
    }


@router.get("/players/top")
def get_top_players():
    """Return top players ordered by goals scored."""
    return [
        {"player": "Juan Pérez", "goals": 12, "assists": 5},
        {"player": "Carlos Gómez", "goals": 10, "assists": 7},
        {"player": "Luis Rodríguez", "goals": 9, "assists": 4},
    ]
