from django.contrib import admin
from .models import Maestro, OrchestrationQuery, OrchestrationQueryLog


# Register your models here.

@admin.register(Maestro)
class MaestroAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization', 'llm_model', 'created_by_user', 'last_updated_by_user', 'created_at',
                    'updated_at']
    search_fields = ['name', 'organization', 'llm_model', 'created_by_user', 'last_updated_by_user']
    list_filter = ['organization', 'llm_model', 'created_by_user', 'last_updated_by_user', 'created_at', 'updated_at']


@admin.register(OrchestrationQuery)
class OrchestrationQueryAdmin(admin.ModelAdmin):
    list_display = ['maestro', 'query_text', 'created_by_user', 'last_updated_by_user', 'created_at', 'updated_at']
    search_fields = ['maestro', 'query_text', 'created_by_user', 'last_updated_by_user']
    list_filter = ['maestro', 'created_by_user', 'last_updated_by_user', 'created_at', 'updated_at']


@admin.register(OrchestrationQueryLog)
class OrchestrationQueryLogAdmin(admin.ModelAdmin):
    list_display = ['orchestration_query', 'log_text_content', 'created_at']
    search_fields = ['orchestration_query', 'log_text_content']
    list_filter = ['orchestration_query', 'created_at']


