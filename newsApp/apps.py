from django.apps import AppConfig

class NewsappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newsApp'

    # If you need signals, import them in ready()
    def ready(self):
        import newsApp.signals  # ✅ if you have signals
