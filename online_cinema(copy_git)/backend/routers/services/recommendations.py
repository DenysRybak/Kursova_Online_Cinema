from sqlalchemy.orm import Session
from backend import models
from typing import List

class RecommendationService:

    def recommend_for(self, user_id: int, db: Session) -> List[models.Movie]:
        # переконаємось що юзер є
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            return []

        # дістаємо list favorite movie ids і самі Movies
        fav_movies = (
            db.query(models.Movie)
            .join(models.Favorite, models.Favorite.movie_id == models.Movie.id)
            .filter(models.Favorite.user_id == user_id)
            .all()
        )

        if not fav_movies:
            # топ-5 за рейтинг (попередньо приведемо rating до float якщо можливо)
            try:
                # якщо rating зберігається як рядок — конвертуємо у float за допомогою CASE в SQL не робимо, простіше у Python
                all_movies = db.query(models.Movie).all()
                # сортуємо за rating, якщо rating пустий — ставимо 0
                def r_val(m):
                    try:
                        return float(m.rating) if m.rating is not None else 0.0
                    except:
                        return 0.0
                all_movies_sorted = sorted(all_movies, key=r_val, reverse=True)
                return all_movies_sorted[:5]
            except Exception:
                return db.query(models.Movie).limit(5).all()

        fav_genres = {m.genre for m in fav_movies if m.genre}
        fav_ids = {m.id for m in fav_movies}

        # рекомендовані — інші фільми в тих жанрах, яких ще немає в favorites
        recommended = (
            db.query(models.Movie)
            .filter(models.Movie.genre.in_(list(fav_genres)))
            .filter(~models.Movie.id.in_(list(fav_ids)))
            .limit(10)
            .all()
        )

        # якщо мало результатів — доповнимо топ-5
        if len(recommended) < 5:
            extras = (
                db.query(models.Movie)
                .filter(~models.Movie.id.in_(list(fav_ids)))
                .limit(5)
                .all()
            )
            # додаємо ті, які ще не в recommended
            ids_rec = {m.id for m in recommended}
            for m in extras:
                if m.id not in ids_rec:
                    recommended.append(m)
                    ids_rec.add(m.id)
                    if len(recommended) >= 5:
                        break

        return recommended[:5]
