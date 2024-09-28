from django.contrib import admin

from apps.orchestrations.models import OrchestrationQueryLog


@admin.register(OrchestrationQueryLog)
class OrchestrationQueryLogAdmin(admin.ModelAdmin):
    list_display = ['orchestration_query', 'log_text_content', 'created_at']
    search_fields = ['orchestration_query', 'log_text_content']
    list_filter = ['orchestration_query', 'created_at']
