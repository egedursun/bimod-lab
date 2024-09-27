from django.contrib import admin

from apps._services.knowledge_base.memory.memory_executor import MemoryExecutor
from apps.datasource_knowledge_base.models import ContextHistoryMemory
from django.contrib.admin.actions import delete_selected as django_delete_selected


@admin.register(ContextHistoryMemory)
class ContextHistoryMemoryAdmin(admin.ModelAdmin):
    list_display = ["knowledge_base_memory_uuid", "knowledge_base_memory_uuid", "created_at", "updated_at"]
    search_fields = ["knowledge_base_memory_uuid", "knowledge_base_memory_uuid", "created_at", "updated_at"]
    readonly_fields = ['created_at', 'updated_at']

    list_per_page = 20
    list_max_show_all = 100

    def delete_selected(self, request, queryset):
        for obj in queryset:
            # delete the document from Weaviate
            client = MemoryExecutor(connection=obj.context_history_base)
            if client is not None:
                result = client.delete_chat_history_document(
                    class_name=obj.context_history_base.class_name,
                    document_uuid=obj.knowledge_base_memory_uuid)
                if not result["status"]:
                    print(f"Error deleting chat history document: {result['error']}")
        return django_delete_selected(self, request, queryset)
