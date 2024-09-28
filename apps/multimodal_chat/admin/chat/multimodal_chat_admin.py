#  Copyright Policy & Ownership
#
#  Bimod.io is a product of BMD Holdings. All materials, including but not limited to software, code, documentation,
#  graphics, design elements, and user interfaces provided by Bimod.io are protected by copyright law and international
#  treaties.
#  All content within Bimod.io is the exclusive property of BMD Holdings, unless otherwise stated.
#  Unauthorized use, distribution, or reproduction of any material contained in this software without the express
#  written consent of BMD Holdings is strictly prohibited.
#  Users may not copy, modify, distribute, display, perform, or create derivative works of Bimod.io without prior
#  written permission from BMD Holdings.


from django.contrib import admin

from apps._services.knowledge_base.memory.memory_executor import MemoryExecutor
from apps.assistants.utils import ContextOverflowStrategyNames
from apps.multimodal_chat.models import MultimodalChat

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
