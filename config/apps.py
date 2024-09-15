
from django.apps import AppConfig


class MainAppConfig(AppConfig):
    name = 'config'

    def ready(self):
        from data.loader import BoilerplateDataLoader
        BoilerplateDataLoader.load()
