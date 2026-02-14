"""Main FastAPI application including external API integrations."""
from __future__ import annotations

import logging
import os
from pathlib import Path

from alembic import command
from alembic.config import Config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import backend.models.teams  # noqa: F401 - ensure Team model is registered
import backend.models.tournaments  # noqa: F401
import backend.models.users  # noqa: F401
from backend.routes import auth, fields, messages, referees, ranking, stats, teams, tournaments
from backend.services.api_football import fetch_leagues

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def run_migrations() -> None:
    """Apply database migrations at application startup."""
    cfg = Config(str(Path(__file__).resolve().parent.parent / "alembic.ini"))
    command.upgrade(cfg, "head")


run_migrations()

app = FastAPI(title="TuLiga API", version="0.3.0")

# CORS configuration
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(fields.router)
app.include_router(messages.router)
app.include_router(referees.router)
app.include_router(ranking.router)
app.include_router(stats.router)
app.include_router(teams.router)
app.include_router(tournaments.router)


@app.get("/health")
def health_check():
    """Health check endpoint for Docker / load balancers."""
    return {"status": "ok"}


@app.get("/external-leagues")
def external_leagues(country: str | None = None):
    """Return league data from API-Football."""
    return fetch_leagues(country)
