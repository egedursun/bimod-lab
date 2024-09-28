from django.contrib import admin

from apps.export_leanmods.models import ExportLeanmodAssistantAPI


@admin.register(ExportLeanmodAssistantAPI)
class ExportLeanmodAssistantAPIAdmin(admin.ModelAdmin):
    list_display = (
        "lean_assistant", "is_public", "request_limit_per_hour", "custom_api_key", "created_by_user",
        "is_online", "created_at", "updated_at")
    list_filter = (
        "lean_assistant", "is_public", "request_limit_per_hour", "custom_api_key", "created_by_user",
        "is_online", "created_at", "updated_at")
    search_fields = (
        "lean_assistant", "is_public", "request_limit_per_hour", "custom_api_key", "created_by_user",
        "is_online", "created_at", "updated_at")
    date_hierarchy = "created_at"
    ordering = ["-created_at"]

    list_per_page = 20
    list_max_show_all = 100
    list_editable = []
    list_display_links = ["lean_assistant"]
    list_select_related = False
    list_display_links_details = False
