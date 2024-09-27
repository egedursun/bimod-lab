from django.contrib import admin

from apps.export_assistants.models import RequestLog


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
