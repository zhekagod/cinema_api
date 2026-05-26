from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.db_models.booking import Booking
from src.schemas.booking import (
    BookingCreate,
    BookingResponse,
)


booking_router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)


@booking_router.get("/", response_model=list[BookingResponse])
def get_bookings(db: Session = Depends(get_db)):
    return db.query(Booking).all()


@booking_router.post("/", response_model=BookingResponse)
def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db),
):
    # Проверка занятости места
    existing_booking = (
        db.query(Booking)
        .filter(
            Booking.movie_id == booking.movie_id,
            Booking.show_time == booking.show_time,
            Booking.seat_number == booking.seat_number,
        )
        .first()
    )

    if existing_booking:
        raise HTTPException(
            status_code=400,
            detail="Seat already booked",
        )

    new_booking = Booking(**booking.model_dump())

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    return new_booking


@booking_router.delete("/{booking_id}")
def delete_booking(
    booking_id: int,
    db: Session = Depends(get_db),
):
    booking = (
        db.query(Booking)
        .filter(Booking.id == booking_id)
        .first()
    )

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found",
        )

    db.delete(booking)
    db.commit()

    return {"message": "Booking deleted"}