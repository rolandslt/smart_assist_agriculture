from django.apps import AppConfig


class AgriAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'agri_app'

    def ready(self):
        import agri_app.signals
