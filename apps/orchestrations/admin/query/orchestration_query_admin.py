from django.contrib import admin

from apps.orchestrations.models import OrchestrationQuery


@admin.register(OrchestrationQuery)
class OrchestrationQueryAdmin(admin.ModelAdmin):
    list_display = ['maestro', 'query_text', 'created_by_user', 'last_updated_by_user', 'created_at', 'updated_at']
    search_fields = ['maestro', 'query_text', 'created_by_user', 'last_updated_by_user']
    list_filter = ['maestro', 'created_by_user', 'last_updated_by_user', 'created_at', 'updated_at']
