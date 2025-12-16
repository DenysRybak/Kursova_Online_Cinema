from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from backend.database import SessionLocal
from backend import models, schemas

# Strategy pattern imports
from backend.routers.services.video_player.low import LowQualityPlayer
from backend.routers.services.video_player.medium import MediumQualityPlayer
from backend.routers.services.video_player.high import HighQualityPlayer

# factory Method import
from backend.routers.services.factory.movie_factory import MovieFactory


router = APIRouter(prefix="/movies", tags=["Movies"])


# ---- DB Session dependency ----
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# SEARCH + FILTER
# -----------------------------
@router.get("/search", response_model=list[schemas.Movie])
def search_movies(
    title: Optional[str] = None,
    genre: Optional[str] = None,
    year: Optional[int] = None,
    country: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Movie)

    if title:
        query = query.filter(models.Movie.title.ilike(f"%{title}%"))
    if genre:
        query = query.filter(models.Movie.genre.ilike(f"%{genre}%"))
    if year:
        query = query.filter(models.Movie.year == year)
    if country:
        query = query.filter(models.Movie.country.ilike(f"%{country}%"))

    return query.all()


# -----------------------------
# CRUD
# -----------------------------

# ---- CREATE MOVIE ----
@router.post("/", response_model=schemas.Movie)
def create_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):

    movie_data = movie.dict()

    # factory Method (correct!)
    db_movie = MovieFactory.create_movie(movie_data)

    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


# ---- GET ALL MOVIES ----
@router.get("/", response_model=list[schemas.Movie])
def get_movies(db: Session = Depends(get_db)):
    return db.query(models.Movie).all()


# ---- GET MOVIE BY ID ----
@router.get("/{movie_id}", response_model=schemas.Movie)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    return movie


# ---- UPDATE MOVIE ----
@router.put("/{movie_id}", response_model=schemas.Movie)
def update_movie(movie_id: int, movie_data: schemas.MovieCreate, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    for key, value in movie_data.dict().items():
        setattr(movie, key, value)

    db.commit()
    db.refresh(movie)
    return movie


# ---- DELETE MOVIE ----
@router.delete("/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    db.delete(movie)
    db.commit()
    return {"message": "Movie deleted successfully!"}


# ---- PLAY MOVIE (Strategy Pattern) ----
@router.get("/{movie_id}/play")
def play_movie(movie_id: int, quality: str = "medium", db: Session = Depends(get_db)):

    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    if quality == "low":
        player = LowQualityPlayer()
    elif quality == "high":
        player = HighQualityPlayer()
    else:
        player = MediumQualityPlayer()

    return {"result": player.play(movie)}
