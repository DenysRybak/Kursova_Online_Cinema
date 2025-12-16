from backend.routers.services.video_player.base import VideoPlayer
from backend.models import Movie


class MediumQualityPlayer(VideoPlayer):
    def play(self, movie: Movie) -> str:
        return f"Playing '{movie.title}' in MEDIUM quality (720p)"
