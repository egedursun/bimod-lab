from django.contrib import admin

from apps._services.knowledge_base.memory.memory_executor import MemoryExecutor
from apps.assistants.models import ContextOverflowStrategyNames
from apps.multimodal_chat.models import MultimodalChat, MultimodalChatMessage, ChatCreationLog, ChatMessageCreationLog, \
    MultimodalLeanChat, MultimodalLeanChatMessage
from django.contrib.admin.actions import delete_selected as django_delete_selected


@admin.register(MultimodalChat)
class MultimodalChatAdmin(admin.ModelAdmin):
    list_display = ['organization', 'assistant', 'user', 'chat_name', 'created_by_user', 'created_at', 'updated_at']
    list_filter = ['organization', 'assistant', 'user', 'created_by_user', 'created_at', 'updated_at']
    search_fields = ['organization', 'assistant', 'user', 'chat_name', 'created_by_user', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']

    list_per_page = 20
    list_max_show_all = 100
    list_editable = []
    list_display_links = ["organization"]
    list_select_related = False
    list_display_links_details = False

    def save_model(self, request, obj, form, change):
        if obj.assistant.context_overflow_strategy == ContextOverflowStrategyNames.VECTORIZE:
            if obj.assistant.vectorizer_name is None:
                print("[MultimodalChatAdmin.save_model] The assistant does not have a vectorizer name set.")
                return
            if obj.assistant.vectorizer_api_key is None:
                print("[MultimodalChatAdmin.save_model] The assistant does not have a vectorizer API key set.")
                return
        super().save_model(request, obj, form, change)

    def delete_selected(self, request, queryset):
        for obj in queryset:
            # delete the context memory from Weaviate
            if obj.context_memory_connection:
                executor = MemoryExecutor(connection=obj.context_memory_connection)
                executor.delete_chat_history_classes(class_name=obj.context_memory_connection.class_name)
                obj.context_memory_connection.delete()
        return django_delete_selected(self, request, queryset)


@admin.register(MultimodalLeanChat)
class MultimodalLeanChatAdmin(admin.ModelAdmin):
    list_display = ['organization', 'lean_assistant', 'user', 'chat_name', 'created_by_user', 'created_at', 'updated_at']
    list_filter = ['organization', 'lean_assistant', 'user', 'created_by_user', 'created_at', 'updated_at']
    search_fields = ['organization', 'lean_assistant', 'user', 'chat_name', 'created_by_user', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']

    list_per_page = 20
    list_max_show_all = 100
    list_editable = []
    list_display_links = ["organization"]
    list_select_related = False
    list_display_links_details = False


@admin.register(MultimodalChatMessage)
class MultimodalChatMessageAdmin(admin.ModelAdmin):
    list_display = ['multimodal_chat', 'sender_type', 'sent_at']
    list_filter = ['multimodal_chat', 'sender_type', 'sent_at']
    search_fields = ['multimodal_chat', 'sender_type', 'sent_at']
    readonly_fields = ['sent_at']
    list_per_page = 20
    list_max_show_all = 100
    list_editable = []
    list_select_related = False
    list_display_links_details = False


@admin.register(MultimodalLeanChatMessage)
class MultimodalLeanChatMessageAdmin(admin.ModelAdmin):
    list_display = ['multimodal_lean_chat', 'sender_type', 'sent_at']
    list_filter = ['multimodal_lean_chat', 'sender_type', 'sent_at']
    search_fields = ['multimodal_lean_chat', 'sender_type', 'sent_at']
    readonly_fields = ['sent_at']
    list_per_page = 20
    list_max_show_all = 100
    list_editable = []
    list_select_related = False
    list_display_links_details = False


@admin.register(ChatCreationLog)
class ChatCreationLogAdmin(admin.ModelAdmin):
    list_display = ["organization", 'created_at']
    list_filter = ['created_at']
    search_fields = ['created_at']


@admin.register(ChatMessageCreationLog)
class ChatMessageCreationLogAdmin(admin.ModelAdmin):
    list_display = ["organization", 'created_at']
    list_filter = ['created_at']
    search_fields = ['created_at']
