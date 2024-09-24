from django.apps import AppConfig

from config import settings


class ExportLeanmodsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.export_leanmods'

    def ready(self):
        # Schedule the command to run after the server starts
        if settings.TESTING:
            return

        from threading import Thread
        from django.core.management import call_command

        def run_initialization_command():
            call_command('start_exported_leanmods')

        # Use a separate thread to avoid blocking the server startup
        thread = Thread(target=run_initialization_command)
        thread.start()
