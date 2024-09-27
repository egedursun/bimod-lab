from django.contrib import admin

from apps.datasource_knowledge_base.models import DocumentProcessingLog


@admin.register(DocumentProcessingLog)
class DocumentProcessingLogAdmin(admin.ModelAdmin):
    list_display = ['document_full_uri', 'log_message', 'created_at']
    list_filter = ['document_full_uri', 'log_message', 'created_at']
    search_fields = ['document_full_uri', 'log_message']
    readonly_fields = ['created_at']

    list_per_page = 20
    list_max_show_all = 100
