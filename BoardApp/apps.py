from django.apps import AppConfig


class BoardappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'BoardApp'

    def ready(self):
        from . import signals  # выполнение модуля -> регистрация сигналов
