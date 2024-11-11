from django.apps import AppConfig


class SemantorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.semantor'

    def ready(self):
        from apps.semantor.signals.update_assistant_embedding_signals import update_assistant_embedding_after_save
        from apps.semantor.signals.update_integration_embedding_signals import update_integration_embedding_after_save
        from apps.semantor.signals.delete_assistant_embedding_signals import remove_vector_from_index_on_assistant_delete
        from apps.semantor.signals.delete_integration_embedding_signals import remove_vector_from_index_on_integration_delete
