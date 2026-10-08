from django.apps import AppConfig


class AccountAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "account_app"

    # Utilisation signal qui genere un profil dès qu'un user est créé
    def ready(self):
        from . import signals
