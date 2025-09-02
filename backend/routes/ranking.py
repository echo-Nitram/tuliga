from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..models import Base, SessionLocal, engine
from ..services.ranking import get_ranking as compute_ranking

router = APIRouter()

# Ensure tables exist
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/ranking")
def get_ranking(db: Session = Depends(get_db)):
    """Expose ranking computed from tournament results."""
    return compute_ranking(db)
