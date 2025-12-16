from backend import models


class MovieFactory:
    """factory Method for movie creation"""

    @staticmethod
    def create_movie(data: dict) -> models.Movie:
        if "rating" not in data or data["rating"] is None:
            data["rating"] = 0.0

        return models.Movie(
            title=data.get("title"),
            genre=data.get("genre"),
            year=data.get("year"),
            country=data.get("country"),
            rating=data.get("rating"),
            description=data.get("description"),
        )
