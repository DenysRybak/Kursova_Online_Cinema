from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import schemas, models
from backend.database import get_db

# === OBSERVER PATTERN ===
from backend.routers.services.observer.subject import Subject
from backend.routers.services.observer.notification import NotificationService

# створюємо Subject (менеджер подій)
event_manager = Subject()
# підключаємо NotificationService як Observer
event_manager.attach(NotificationService())

router = APIRouter(
    prefix="/favorites",
    tags=["Favorites"]
)


# -----------------------------
# Add movie to favorites
# -----------------------------
@router.post("/", response_model=schemas.Favorite)
def add_favorite(fav: schemas.FavoriteCreate, db: Session = Depends(get_db)):
    # перевірка чи існує юзер
    user = db.query(models.User).filter(models.User.id == fav.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # перевірка чи існує фільм
    movie = db.query(models.Movie).filter(models.Movie.id == fav.movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    # перевірка чи вже є у вибраному
    existing = db.query(models.Favorite).filter(
        models.Favorite.user_id == fav.user_id,
        models.Favorite.movie_id == fav.movie_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Already in favorites")

    new_fav = models.Favorite(
        user_id=fav.user_id,
        movie_id=fav.movie_id
    )

    db.add(new_fav)
    db.commit()
    db.refresh(new_fav)

    # OBSERVER повідомлення
    event_manager.notify(
        f"User {fav.user_id} added movie {fav.movie_id} to favorites!"
    )

    return new_fav


# -----------------------------
# Get favorites of user
# -----------------------------
@router.get("/{user_id}", response_model=list[schemas.Favorite])
def get_user_favorites(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Favorite).filter(models.Favorite.user_id == user_id).all()


# -----------------------------
# Remove from favorites
# -----------------------------
@router.delete("/{favorite_id}")
def delete_favorite(favorite_id: int, db: Session = Depends(get_db)):
    fav = db.query(models.Favorite).filter(models.Favorite.id == favorite_id).first()
    if not fav:
        raise HTTPException(status_code=404, detail="Favorite not found")

    db.delete(fav)
    db.commit()

    # OBSERVER повідомлення
    event_manager.notify(
        f"Favorite record {favorite_id} was removed!"
    )

    return {"message": "Favorite removed"}
