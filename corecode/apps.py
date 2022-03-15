from django.apps import apps, AppConfig

class CorecodeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'corecode'

    def ready(self) -> None:
        from corecode import signals