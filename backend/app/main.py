"""Main FastAPI application including external API integrations."""
from __future__ import annotations

from pathlib import Path

from alembic import command
from alembic.config import Config
from fastapi import FastAPI

from backend.routes import fields, messages, referees, ranking, stats, tournaments
from backend.services.api_football import fetch_leagues


def run_migrations() -> None:
    """Apply database migrations at application startup."""
    cfg = Config(str(Path(__file__).resolve().parent.parent / "alembic.ini"))
    command.upgrade(cfg, "head")


run_migrations()

app = FastAPI()

# Include existing routers
app.include_router(fields.router)
app.include_router(messages.router)
app.include_router(referees.router)
app.include_router(ranking.router)
app.include_router(stats.router)
app.include_router(tournaments.router)


@app.get("/external-leagues")
def external_leagues(country: str | None = None):
    """Return league data from API-Football."""
    return fetch_leagues(country)
