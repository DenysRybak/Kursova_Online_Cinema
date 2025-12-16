from abc import ABC, abstractmethod
from backend.models import Movie


class VideoPlayer(ABC):

    @abstractmethod
    def play(self, movie: Movie) -> str:
        pass
