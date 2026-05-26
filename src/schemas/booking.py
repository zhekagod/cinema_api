from pydantic import BaseModel


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

    class Config:
        from_attributes = True