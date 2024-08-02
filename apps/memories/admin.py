from django.contrib import admin

from apps.memories.models import AssistantMemory


@admin.register(AssistantMemory)
class AssistantMemoryAdmin(admin.ModelAdmin):
    list_display = ["user", "assistant", "memory_type", "created_at", "memory_text_content", "created_at"]
    list_filter = ["memory_type"]
    search_fields = ["user__username", "assistant__name"]
    date_hierarchy = "created_at"
    list_per_page = 20
    list_max_show_all = 100
    list_select_related = ["user", "assistant"]
    list_display_links = ["user", "assistant"]
    list_editable = ["memory_type"]
    readonly_fields = ["created_at"]
