"""Test utilities.

By default tests run against an in-memory SQLite database. This is achieved by
setting the ``DATABASE_URL`` environment variable before importing the models
module.
"""

import os
from pathlib import Path

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

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
