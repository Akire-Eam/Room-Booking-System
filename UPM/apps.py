from django.apps import AppConfig


class UpmConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'UPM'

    def ready(self):
        from .tasks import start
        # The start() initiates auto-reject function from tasks.py asynchronously
        start()