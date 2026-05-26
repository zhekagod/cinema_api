import uvicorn
from fastapi import FastAPI

from src.api.auth import auth_router
from src.api.bookings import booking_router
from src.api.movies import movie_router
from src.config import config
from src.database import Base, engine


# Создание таблиц
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Cinema Tickets API",
)


app.include_router(auth_router)
app.include_router(movie_router)
app.include_router(booking_router)


@app.get("/")
def home():
    return {"message": "Cinema API works!"}


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="127.0.0.1",
        port=config.port,
        reload=True,
    )