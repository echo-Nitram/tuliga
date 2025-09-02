"""Database setup for SQLAlchemy models."""

from __future__ import annotations

import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite database stored in the backend directory so that Alembic can manage
# migrations. The URL can be overridden via the ``DATABASE_URL`` environment
# variable. Tests are expected to provide an in-memory database
# (``sqlite:///:memory:``) through this variable.
BASE_DIR = Path(__file__).resolve().parent
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'app.db'}")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

__all__ = ["Base", "engine", "SessionLocal", "DATABASE_URL"]
