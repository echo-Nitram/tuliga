"""Routes for field listing and booking with payment integration."""
from __future__ import annotations

from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from ..core.payments import process_payment
from ..models import SessionLocal
from ..models.fields import Booking as BookingModel, Field as FieldModel

router = APIRouter(prefix="/fields")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class FieldCreate(BaseModel):
    name: str
    location: str
    price_per_hour: float


class FieldOut(FieldCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class BookingRequest(BaseModel):
    start_time: datetime
    end_time: datetime
    provider: str


class BookingOut(BaseModel):
    id: int
    field_id: int
    start_time: datetime
    end_time: datetime
    paid: bool
    payment_id: str | None = None

    model_config = ConfigDict(from_attributes=True)


@router.post("", response_model=FieldOut)
def create_field(payload: FieldCreate, db: Session = Depends(get_db)) -> FieldOut:
    field = FieldModel(**payload.model_dump())
    db.add(field)
    db.commit()
    db.refresh(field)
    return FieldOut.model_validate(field)


@router.get("", response_model=List[FieldOut])
def list_fields(db: Session = Depends(get_db)) -> List[FieldOut]:
    fields = db.query(FieldModel).all()
    return [FieldOut.model_validate(f) for f in fields]


@router.post("/{field_id}/bookings", response_model=BookingOut)
def book_field(
    field_id: int, payload: BookingRequest, db: Session = Depends(get_db)
) -> BookingOut:
    field = db.get(FieldModel, field_id)
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")
    conflict = (
        db.query(BookingModel)
        .filter(
            BookingModel.field_id == field_id,
            BookingModel.start_time < payload.end_time,
            BookingModel.end_time > payload.start_time,
        )
        .first()
    )
    if conflict:
        raise HTTPException(status_code=400, detail="Field already booked for this time")
    payment_id = process_payment(payload.provider, field.price_per_hour)
    booking = BookingModel(
        field_id=field_id,
        start_time=payload.start_time,
        end_time=payload.end_time,
        paid=True,
        payment_id=payment_id,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return BookingOut.model_validate(booking)


@router.get("/bookings", response_model=List[BookingOut])
def list_bookings(db: Session = Depends(get_db)) -> List[BookingOut]:
    bookings = db.query(BookingModel).all()
    return [BookingOut.model_validate(b) for b in bookings]

