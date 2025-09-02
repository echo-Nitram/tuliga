"""Domain models for field management and bookings."""
from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel


class Field(BaseModel):
    """Represents a sports field available for booking."""
    id: int
    name: str
    location: str
    price_per_hour: float


class Booking(BaseModel):
    """Booking record for a field reservation."""
    id: int
    field_id: int
    start_time: datetime
    end_time: datetime
    paid: bool = False
    payment_id: str | None = None
