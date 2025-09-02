"""Test utilities."""

from pathlib import Path

from alembic import command
from alembic.config import Config

from backend.models import DATABASE_URL


def run_migrations() -> None:
    """Apply Alembic migrations from a clean state for tests."""
    config = Config(str(Path(__file__).resolve().parents[1] / "alembic.ini"))
    config.set_main_option("sqlalchemy.url", DATABASE_URL)
    command.downgrade(config, "base")
    command.upgrade(config, "head")


__all__ = ["run_migrations"]