from django.apps import AppConfig


class NotificationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Notification'

    def ready(self): #make signals work when Notification model works
        import Notification.signals
