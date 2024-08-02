from django.contrib import admin

from apps.export_assistants.models import ExportAssistantAPI, RequestLog


@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = ("export_assistant", "timestamp")
    list_filter = ("export_assistant", "timestamp")
    search_fields = ("export_assistant", "timestamp")
    date_hierarchy = "timestamp"
    ordering = ["-timestamp"]

    list_per_page = 20
    list_max_show_all = 100
    list_editable = []


@admin.register(ExportAssistantAPI)
class ExportAssistantAPIAdmin(admin.ModelAdmin):
    list_display = (
        "assistant", "is_public", "request_limit_per_hour", "custom_api_key", "created_by_user",
        "is_online", "created_at", "updated_at")
    list_filter = (
        "assistant", "is_public", "request_limit_per_hour", "custom_api_key", "created_by_user",
        "is_online", "created_at", "updated_at")
    search_fields = (
        "assistant", "is_public", "request_limit_per_hour", "custom_api_key", "created_by_user",
        "is_online", "created_at", "updated_at")
    date_hierarchy = "created_at"
    ordering = ["-created_at"]

    list_per_page = 20
    list_max_show_all = 100
    list_editable = []
    list_display_links = ["assistant"]
    list_select_related = False
    list_display_links_details = False
