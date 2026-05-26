from contextlib import asynccontextmanager
import random
import string

import uvicorn
from fastapi import FastAPI

from src.db_models.booking import Booking
from src.config import config
from src.database import Base, engine

from src.api.auth import auth_router
from src.api.movies import movie_router
from src.api.bookings import booking_router
from src.api.users import user_router


from src.db_models.user import User
from src.db_models.movie import Movie

from src.utils.show_tables import print_all_tables
from sqlalchemy.orm import Session


# ----------------------------
# utils
# ----------------------------
def random_username(length: int = 6) -> str:
    return "user_" + "".join(
        random.choices(string.ascii_lowercase + string.digits, k=length)
    )


# ----------------------------
# seed DB
# ----------------------------

def seed_data():
    db = Session(bind=engine)

    # если уже есть данные — не seed’им
    if db.query(User).count() > 0:
        db.close()
        return

    admin = User(username="admin", password="admin")

    users = [
        User(username=f"user_{i}", password="1234")
        for i in range(9)
    ]

    movies = [
        Movie(title="Matrix", description="Матрица", duration=136),
        Movie(title="Inception", description="Начало", duration=148),
        Movie(title="Interstellar", description="Интерстеллар", duration=169),
    ]

    db.add(admin)
    db.add_all(users + movies)

    db.commit()
    db.close()


# ----------------------------
# LIFESPAN (startup logic)
# ----------------------------
@asynccontextmanager
async def lifespan(app):
    print("\n[STARTUP] Creating tables...")
    Base.metadata.create_all(bind=engine)

    if config.RESET_DB:
        print("[STARTUP] RESET_DB=1 → clearing database...")
        clear_db()

    print("[STARTUP] Seeding data...")
    seed_data()

    print("[STARTUP] Final DB state:")
    print_all_tables()

    yield

    print("\n[SHUTDOWN] Server stopped")

# ----------------------------
# FASTAPI APP
# ----------------------------
app = FastAPI(
    title="Cinema Tickets API",
    lifespan=lifespan,
)

def clear_db():
    # ⚠️ ВАЖНО: удаляем данные, но не таблицы
    db = Session(bind=engine)

    db.query(Booking).delete()
    db.query(Movie).delete()
    db.query(User).delete()

    db.commit()
    db.close()

# routers
app.include_router(auth_router)
app.include_router(movie_router)
app.include_router(booking_router)
app.include_router(user_router)

# ----------------------------
# TEST ENDPOINTS
# ----------------------------
@app.get("/")
def home():
    return {"message": "Cinema API works!"}


@app.get("/health")
def health():
    return {"status": "ok"}


# ----------------------------
# RUN
# ----------------------------
if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="127.0.0.1",
        port=config.port,
        reload=True,
    )