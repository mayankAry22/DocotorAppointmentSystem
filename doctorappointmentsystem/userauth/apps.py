from django.apps import AppConfig

class UserauthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userauth'
    
    def ready(self):
        import userauth.signals  # Add this line to import the signals.py

    