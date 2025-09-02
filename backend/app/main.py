"""Main FastAPI application including external API integrations."""
from __future__ import annotations

from fastapi import FastAPI

from backend.routes import fields, messages, referees, ranking, stats, tournaments
from backend.services.api_football import fetch_leagues

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
