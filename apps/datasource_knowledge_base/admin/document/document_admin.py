from django.contrib import admin

from apps._services.knowledge_base.document.knowledge_base_decoder import KnowledgeBaseSystemDecoder
from apps.datasource_knowledge_base.models import KnowledgeBaseDocument
from django.contrib.admin.actions import delete_selected as django_delete_selected


@admin.register(KnowledgeBaseDocument)
class KnowledgeBaseDocumentAdmin(admin.ModelAdmin):
    list_display = ['knowledge_base', 'document_type', 'document_file_name', 'document_description',
                    'document_metadata', 'document_uri', 'created_at', 'updated_at']
    list_filter = ['knowledge_base', 'document_type', 'document_file_name', 'document_description',
                   'document_metadata', 'document_uri', 'created_at', 'updated_at']
    search_fields = ['knowledge_base', 'document_type', 'document_file_name', 'document_description',
                     'document_metadata', 'document_uri', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']

    list_per_page = 20
    list_max_show_all = 100

    def delete_selected(self, request, queryset):
        for obj in queryset:
            client = KnowledgeBaseSystemDecoder.get(obj.knowledge_base)
            if client is not None:
                result = client.delete_weaviate_document(
                    class_name=obj.knowledge_base.class_name,
                    document_uuid=obj.document_uuid)
                if not result["status"]:
                    print(f"Error deleting Weaviate document: {result['error']}")
        return django_delete_selected(self, request, queryset)
