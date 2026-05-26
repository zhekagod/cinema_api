import pandas as pd
from sqlalchemy.orm import Session

from src.database import SessionLocal
from src.db_models.user import User
from src.db_models.movie import Movie
from src.db_models.booking import Booking


def show_table(model, db: Session):
    rows = db.query(model).all()

    data = [r.__dict__ for r in rows]
    for d in data:
        d.pop("_sa_instance_state", None)

    return pd.DataFrame(data)


def print_all_tables():
    db = SessionLocal()

    print("\n USERS")
    print(show_table(User, db))

    print("\n MOVIES")
    print(show_table(Movie, db))

    print("\n BOOKINGS")
    print(show_table(Booking, db))

    db.close()