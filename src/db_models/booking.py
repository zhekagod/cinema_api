from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey
from src.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))

    seat_number: Mapped[str] = mapped_column(String(10))
    show_time: Mapped[str] = mapped_column(String(100))