from django.contrib import admin

from apps.datasource_knowledge_base.models import KnowledgeBaseDocumentChunk


@admin.register(KnowledgeBaseDocumentChunk)
class KnowledgeBaseDocumentChunkAdmin(admin.ModelAdmin):
    list_display = ['knowledge_base', 'document', 'chunk_document_type', 'chunk_document_uri', 'knowledge_base_uuid',
                    'document_uuid', 'created_at']
    list_filter = ['document', 'chunk_document_type', 'knowledge_base_uuid', 'document_uuid', 'created_at']
    search_fields = ['document', 'chunk_document_type', 'chunk_content', 'chunk_metadata', 'chunk_document_uri',
                     'knowledge_base_uuid', 'created_at']
    readonly_fields = ['created_at']

    list_per_page = 20
    list_max_show_all = 100
