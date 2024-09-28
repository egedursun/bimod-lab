from django.contrib import admin

from apps.export_orchestrations.models import OrchestratorRequestLog


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
