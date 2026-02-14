"""User model for authentication."""
from __future__ import annotations

from sqlalchemy import Column, DateTime, Integer, String, func

from . import Base


class User(Base):
    """Application user with hashed credentials."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True, index=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="user")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
