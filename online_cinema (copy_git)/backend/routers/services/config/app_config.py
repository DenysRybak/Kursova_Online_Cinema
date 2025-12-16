class AppConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppConfig, cls).__new__(cls)

            # Тут ініціалізуємо конфігурацію
            cls._instance.service_name = "Online Cinema"
            cls._instance.default_video_quality = "medium"
            cls._instance.debug = True
            cls._instance.version = "1.0.0"

        return cls._instance
