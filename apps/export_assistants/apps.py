from threading import Thread

from django.apps import AppConfig
from django.core.management import call_command


class ExportAssistantsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.export_assistants'

    def ready(self):
        # Schedule the command to run after the server starts
        def run_initialization_command():
            call_command('start_exported_assistants')
        # Use a separate thread to avoid blocking the server startup
        thread = Thread(target=run_initialization_command)
        thread.start()
