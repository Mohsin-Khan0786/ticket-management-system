from django.apps import AppConfig


class QuerrypracticeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'querrypractice'

    def ready(self):
        import querrypractice.signals
