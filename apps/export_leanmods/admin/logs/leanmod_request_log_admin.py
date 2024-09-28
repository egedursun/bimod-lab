from django.contrib import admin

from apps.export_leanmods.models import LeanmodRequestLog


@admin.register(LeanmodRequestLog)
class LeanmodRequestLogAdmin(admin.ModelAdmin):
    list_display = ("export_lean_assistant", "timestamp")
    list_filter = ("export_lean_assistant", "timestamp")
    search_fields = ("export_lean_assistant", "timestamp")
    date_hierarchy = "timestamp"
    ordering = ["-timestamp"]

    list_per_page = 20
    list_max_show_all = 100
    list_editable = []
