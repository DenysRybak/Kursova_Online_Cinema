from .observer import Observer

class NotificationService(Observer):

    def update(self, message: str):
        print(f"[NOTIFICATION] {message}")  # поки просто лог
