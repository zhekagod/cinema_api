from pydantic import BaseModel

from src.schemas.movie import MovieResponse


class BookingCreate(BaseModel):
    user_id: int
    movie_id: int
    seat_number: str
    show_time: str


class BookingResponse(BaseModel):
    id: int
    user_id: int
    movie_id: int
    seat_number: str
    show_time: str
    movie: MovieResponse | None

    class Config:
        from_attributes = True