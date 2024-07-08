from django.contrib import admin

from apps.assistants.models import Assistant


# Register your models here.

@admin.register(Assistant)
class AssistantAdmin(admin.ModelAdmin):
    list_display = (
        "organization", "response_language", "llm_model", "name", "description", "instructions", "audience", "tone",
        "time_awareness", "place_awareness",
        "max_retry_count", "created_by_user", "last_updated_by_user", "created_at", "updated_at")
    list_filter = (
        "organization", "response_language", "llm_model", "name", "description", "instructions", "audience", "tone",
        "time_awareness", "place_awareness",
        "max_retry_count", "created_by_user", "last_updated_by_user", "created_at", "updated_at")
    search_fields = (
        "organization", "response_language", "llm_model", "name", "description", "instructions", "audience", "tone",
        "time_awareness", "place_awareness",
        "max_retry_count", "created_by_user", "last_updated_by_user", "created_at", "updated_at")
    date_hierarchy = "created_at"
    ordering = ["-created_at"]

    list_per_page = 20
    list_max_show_all = 100
    list_editable = []
    list_display_links = ["organization"]
    list_select_related = False
    list_display_links_details = False
