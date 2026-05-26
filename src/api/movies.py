from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.db_models.booking import Booking
from src.database import get_db
from src.db_models.movie import Movie
from src.schemas.movie import MovieCreate, MovieResponse


movie_router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
)


@movie_router.get("/", response_model=list[MovieResponse])
def get_movies(db: Session = Depends(get_db)):
    return db.query(Movie).all()


@movie_router.get("/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    return movie


@movie_router.get("/{movie_id}/bookings")
def get_movie_bookings(movie_id: int, db: Session = Depends(get_db)):
    return db.query(Booking).filter(Booking.movie_id == movie_id).all()


@movie_router.post("/", response_model=MovieResponse)
def create_movie(
    movie: MovieCreate,
    db: Session = Depends(get_db),
):
    new_movie = Movie(**movie.model_dump())

    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)

    return new_movie


@movie_router.put("/{movie_id}", response_model=MovieResponse)
def update_movie(
    movie_id: int,
    movie: MovieCreate,
    db: Session = Depends(get_db),
):
    current_movie = (
        db.query(Movie)
        .filter(Movie.id == movie_id)
        .first()
    )

    if not current_movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    current_movie.title = movie.title
    current_movie.description = movie.description
    current_movie.duration = movie.duration

    db.commit()
    db.refresh(current_movie)

    return current_movie


@movie_router.delete("/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = (
        db.query(Movie)
        .filter(Movie.id == movie_id)
        .first()
    )

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    db.delete(movie)
    db.commit()

    return {"message": "Movie deleted"}