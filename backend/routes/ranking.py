from fastapi import APIRouter

from ..services.ranking import SAMPLE_MATCHES, calculate_ranking

router = APIRouter()


@router.get("/ranking")
def get_ranking():
    """Expose ranking computed from tournament results."""
    return calculate_ranking(SAMPLE_MATCHES)
