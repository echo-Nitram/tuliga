import os

import pytest
from fastapi.testclient import TestClient

from . import run_migrations


@pytest.fixture(autouse=True)
def _run_migrations():
    """Apply database migrations before each test."""
    run_migrations()


@pytest.fixture
def client() -> TestClient:
    """Return a test client for the FastAPI app."""
    os.environ.setdefault("API_FOOTBALL_KEY", "test-key")
    from backend.app.main import app

    return TestClient(app)
