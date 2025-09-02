"""Domain models for field management and bookings."""
from __future__ import annotations

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from . import Base


class Field(Base):
    """Represents a sports field available for booking."""

    __tablename__ = "fields"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    price_per_hour = Column(Float, nullable=False)

    bookings = relationship(
        "Booking", back_populates="field", cascade="all, delete-orphan"
    )


class Booking(Base):
    """Booking record for a field reservation."""

    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    field_id = Column(Integer, ForeignKey("fields.id", ondelete="CASCADE"))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    paid = Column(Boolean, default=False, nullable=False)
    payment_id = Column(String, nullable=True)

    field = relationship("Field", back_populates="bookings")

