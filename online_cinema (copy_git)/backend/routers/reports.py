from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from backend.database import get_db
from backend import models

router = APIRouter(prefix="/reports", tags=["Reports"])


# --------------------------
# 1) Найпопулярніші фільми
# --------------------------
@router.get("/popular-movies")
def popular_movies(db: Session = Depends(get_db)):
    rows = (
        db.query(
            models.Movie.id.label("movie_id"),
            models.Movie.title.label("title"),
            models.Movie.genre.label("genre"),
            func.count(models.Favorite.id).label("favorites_count")
        )
        .join(models.Favorite, models.Movie.id == models.Favorite.movie_id)
        .group_by(models.Movie.id)
        .order_by(desc("favorites_count"))
        .all()
    )

    return [
        {
            "movie_id": r.movie_id,
            "title": r.title,
            "genre": r.genre,
            "favorites_count": int(r.favorites_count)
        }
        for r in rows
    ]


# --------------------------
# 2) Найпопулярніші жанри
# --------------------------
@router.get("/popular-genres")
def popular_genres(db: Session = Depends(get_db)):
    rows = (
        db.query(
            models.Movie.genre.label("genre"),
            func.count(models.Favorite.id).label("count")
        )
        .join(models.Favorite, models.Movie.id == models.Favorite.movie_id)
        .group_by(models.Movie.genre)
        .order_by(desc("count"))
        .all()
    )

    return [{"genre": r.genre, "count": int(r.count)} for r in rows]


# --------------------------
# 3) Активність користувачів
# --------------------------
@router.get("/user-activity")
def user_activity(db: Session = Depends(get_db)):
    rows = (
        db.query(
            models.User.id.label("user_id"),
            models.User.username.label("username"),
            func.count(models.Favorite.id).label("favorites_count")
        )
        .join(models.Favorite, models.User.id == models.Favorite.user_id)
        .group_by(models.User.id)
        .order_by(desc("favorites_count"))
        .all()
    )

    return [
        {"user_id": r.user_id, "username": r.username, "favorites_count": int(r.favorites_count)}
        for r in rows
    ]


# --------------------------
# 4) Доходи від підписок
# --------------------------
@router.get("/subscription-income")
def subscription_income(db: Session = Depends(get_db)):
    # ціна підписки — налаштовувана константа
    PRICES = {"free": 0, "premium": 100}

    rows = (
        db.query(
            models.User.subscription_type.label("subscription_type"),
            func.count(models.User.id).label("users_count")
        )
        .group_by(models.User.subscription_type)
        .all()
    )

    details = []
    total = 0
    for r in rows:
        typ = r.subscription_type or "free"
        cnt = int(r.users_count)
        price = PRICES.get(typ, 0)
        subtotal = price * cnt
        total += subtotal
        details.append({
            "subscription_type": typ,
            "users": cnt,
            "price_per_user": price,
            "total_income": subtotal
        })

    return {"details": details, "total_income": total}
