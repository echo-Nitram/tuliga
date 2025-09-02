"""Routes for field listing and booking with payment integration."""
from __future__ import annotations

import itertools
from datetime import datetime
from typing import Dict, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..core.payments import process_payment
from ..models.fields import Booking, Field

router = APIRouter(prefix="/fields")

# in-memory storage
_fields: Dict[int, Field] = {}
_bookings: Dict[int, Booking] = {}
_field_id_seq = itertools.count(1)
_booking_id_seq = itertools.count(1)


class FieldCreate(BaseModel):
    name: str
    location: str
    price_per_hour: float


class BookingRequest(BaseModel):
    start_time: datetime
    end_time: datetime
    provider: str


@router.post("", response_model=Field)
def create_field(payload: FieldCreate) -> Field:
    field_id = next(_field_id_seq)
    field = Field(id=field_id, **payload.dict())
    _fields[field_id] = field
    return field


@router.get("", response_model=List[Field])
def list_fields() -> List[Field]:
    return list(_fields.values())


@router.post("/{field_id}/bookings", response_model=Booking)
def book_field(field_id: int, payload: BookingRequest) -> Booking:
    field = _fields.get(field_id)
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")
    payment_id = process_payment(payload.provider, field.price_per_hour)
    booking_id = next(_booking_id_seq)
    booking = Booking(
        id=booking_id,
        field_id=field_id,
        start_time=payload.start_time,
        end_time=payload.end_time,
        paid=True,
        payment_id=payment_id,
    )
    _bookings[booking_id] = booking
    return booking


@router.get("/bookings", response_model=List[Booking])
def list_bookings() -> List[Booking]:
    return list(_bookings.values())
