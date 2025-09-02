"""Simple client for API-Football.com."""
from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests

API_FOOTBALL_HOST = os.getenv(
    "API_FOOTBALL_HOST", "https://api-football-v1.p.rapidapi.com/v3"
)


def fetch_leagues(country: Optional[str] = None) -> Dict[str, Any]:
    """Fetch league information from API-Football.

    Parameters
    ----------
    country: str | None
        Optional country filter.

    Returns
    -------
    dict
        Parsed JSON response from the API.
    """
    api_key = os.getenv("API_FOOTBALL_KEY")
    if not api_key:
        raise RuntimeError("API_FOOTBALL_KEY environment variable must be set")
    headers = {"x-rapidapi-key": api_key}
    params: Dict[str, Any] = {}
    if country:
        params["country"] = country
    url = f"{API_FOOTBALL_HOST}/leagues"
    resp = requests.get(url, headers=headers, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()
