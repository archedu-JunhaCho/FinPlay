from django.apps import AppConfig


class RatesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rates'
    # def ready(self):
    #     from .views import main
    #     main()
