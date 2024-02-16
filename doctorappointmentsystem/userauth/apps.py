from django.apps import AppConfig

class UserauthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userauth'
    
    def ready(self):
        import doctorappointmentsystem.userauth.signals.signals  #To import the signals.py

    