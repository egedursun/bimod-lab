from django.apps import AppConfig


class VoidforgerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.voidforger'

    def ready(self):
        from apps.voidforger.signals import delete_toggle_auto_execution_memory_vector_embedding_signals
        from apps.voidforger.signals import delete_old_chat_messages_vector_embedding_signals
        from apps.voidforger.signals import delete_action_memory_vector_embedding_signals
        from apps.voidforger.signals import update_voidforger_toggle_auto_execution_memory_vector_embedding_after_save
        from apps.voidforger.signals import update_old_chat_messages_vector_embedding_signals
        from apps.voidforger.signals import update_action_memory_vector_embedding_signals
        pass
