from django.apps import AppConfig


class UsersAppConfig(AppConfig):

    name = "stock_price_alert.users"
    verbose_name = "Users"

    def ready(self):
        try:
            import users.signals  # noqa F401
        except ImportError:
            pass
