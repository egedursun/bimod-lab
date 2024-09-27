from django.contrib import admin

from apps._services.knowledge_base.memory.memory_executor import MemoryExecutor
from apps.datasource_knowledge_base.models import ContextHistoryKnowledgeBaseConnection
from apps.datasource_knowledge_base.utils import generate_chat_history_class_name


@admin.register(ContextHistoryKnowledgeBaseConnection)
class ContextHistoryKnowledgeBaseConnectionAdmin(admin.ModelAdmin):
    list_display = ["class_name", "vectorizer", "vectorizer_api_key", "created_at", "updated_at"]
    list_filter = ["class_name", "vectorizer"]
    search_fields = ["class_name", "vectorizer"]
    readonly_fields = ['created_at', 'updated_at']

    list_per_page = 20
    list_max_show_all = 100

    def save_model(self, request, obj, form, change):

        if obj.vectorizer is None:
            obj.vectorizer = "text2vec-openai"

        if obj.class_name is None:
            obj.class_name = generate_chat_history_class_name()
        super().save_model(request, obj, form, change)

        client = MemoryExecutor(connection=obj)
        if client is not None:
            result = client.create_chat_history_classes()
            if not result["status"]:
                print(f"Error creating Weaviate classes: {result['error']}")

    def delete_model(self, request, obj):
        client = MemoryExecutor(connection=self)
        if client is not None:
            result = client.delete_chat_history_classes(class_name=obj.class_name)
            if not result["status"]:
                print(f"Error deleting Chat History class: {result['error']}")
        super().delete_model(request, obj)
