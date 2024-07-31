from django.apps import AppConfig


class MultimodalChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.multimodal_chat'

    def ready(self):
        # Implicitly connect signal handlers decorated with @receiver.
        from . import signals
