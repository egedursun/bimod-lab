from django.contrib import admin

from apps.datasource_codebase.models import RepositoryProcessingLog


@admin.register(RepositoryProcessingLog)
class RepositoryProcessingLogAdmin(admin.ModelAdmin):
    list_display = ['repository_full_uri', 'log_message', 'created_at']
    list_filter = ['repository_full_uri', 'log_message', 'created_at']
    search_fields = ['repository_full_uri', 'log_message']
    readonly_fields = ['created_at']

    list_per_page = 20
    list_max_show_all = 100
