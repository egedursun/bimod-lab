from django.contrib import admin

from apps.export_orchestrations.models import OrchestratorRequestLog, ExportOrchestrationAPI


# Register your models here.
@admin.register(OrchestratorRequestLog)
class OrchestratorRequestLogAdmin(admin.ModelAdmin):
    list_display = ("export_orchestration", "timestamp")
    list_filter = ("export_orchestration", "timestamp")
    search_fields = ("export_orchestration", "timestamp")
    date_hierarchy = "timestamp"
    ordering = ["-timestamp"]

    list_per_page = 20
    list_max_show_all = 100
    list_editable = []


@admin.register(ExportOrchestrationAPI)
class ExportOrchestrationAssistantAPIAdmin(admin.ModelAdmin):
    list_display = (
        "orchestrator", "is_public", "request_limit_per_hour", "custom_api_key", "created_by_user",
        "is_online", "created_at", "updated_at")
    list_filter = (
        "orchestrator", "is_public", "request_limit_per_hour", "custom_api_key", "created_by_user",
        "is_online", "created_at", "updated_at")
    search_fields = (
        "orchestrator", "is_public", "request_limit_per_hour", "custom_api_key", "created_by_user",
        "is_online", "created_at", "updated_at")
    date_hierarchy = "created_at"
    ordering = ["-created_at"]

    list_per_page = 20
    list_max_show_all = 100
    list_editable = []
    list_display_links = ["orchestrator"]
    list_select_related = False
    list_display_links_details = False
