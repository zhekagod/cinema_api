from sqlalchemy.orm import Session
from src.database import SessionLocal, engine, Base
from src.db_models.movie import Movie
from src.db_models.user import User
from src.db_models.booking import Booking

import random
import string


def generate_username(length: int = 8) -> str:
    return "user_" + "".join(
        random.choices(string.ascii_lowercase + string.digits, k=length)
    )

def seed_db() -> None:
    db: Session = SessionLocal()

    try:
        # ---------------- USERS ----------------
        admin = User(username="admin", password="admin")

        users = [admin]

        for _ in range(9):
            users.append(
                User(
                    username=generate_username(),
                    password="1234"
                )
            )

        db.add_all(users)
        db.flush()

        # ---------------- MOVIES ----------------
        movie1 = Movie(
            title="Interstellar",
            description="Space exploration",
            duration=169
        )

        movie2 = Movie(
            title="Matrix",
            description="Simulation theory",
            duration=136
        )

        db.add_all([movie1, movie2])
        db.flush()

        # ---------------- BOOKINGS ----------------
        bookings = [
            Booking(
                user_id=users[0].id,
                movie_id=movie1.id,
                seat_number="A1",
                show_time="18:00"
            ),
            Booking(
                user_id=users[1].id,
                movie_id=movie2.id,
                seat_number="B5",
                show_time="20:00"
            )
        ]

        db.add_all(bookings)

        db.commit()

    except Exception as e:
        db.rollback()
        print(f"Seed error: {e}")

    finally:
        db.close()


def clear_db() -> None:
    db: Session = SessionLocal()

    try:
        # порядок важен из-за foreign keys
        db.query(Booking).delete()
        db.query(Movie).delete()
        db.query(User).delete()

        db.commit()

    except Exception as e:
        db.rollback()
        print(f"Clear error: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    import sys

    command = sys.argv[1] if len(sys.argv) > 1 else None

    if command == "seed":
        seed_db()
        print("DB seeded")

    elif command == "clear":
        clear_db()
        print("DB cleared")

    else:
        print("Use: python -m src.db.seed [seed|clear]")