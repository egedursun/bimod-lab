from django.contrib import admin

from apps._services.knowledge_base.document.knowledge_base_decoder import KnowledgeBaseSystemDecoder
from apps.datasource_knowledge_base.models import DocumentKnowledgeBaseConnection, KnowledgeBaseDocument, \
    KnowledgeBaseDocumentChunk
from apps.datasource_knowledge_base.utils import generate_class_name
from django.contrib.admin.actions import delete_selected as django_delete_selected


# Register your models here.


@admin.register(DocumentKnowledgeBaseConnection)
class DocumentKnowledgeBaseConnectionAdmin(admin.ModelAdmin):
    list_display = ['provider', 'host_url', 'provider_api_key', 'assistant', 'name', 'class_name', 'description',
                    'vectorizer', 'vectorizer_api_key', 'embedding_chunk_size', 'embedding_chunk_overlap',
                    'created_at', 'updated_at']
    list_filter = ['provider', 'host_url', 'provider_api_key', 'assistant', 'name', 'class_name', 'description',
                   'vectorizer', 'vectorizer_api_key', 'embedding_chunk_size', 'embedding_chunk_overlap',
                   'created_at', 'updated_at']
    search_fields = ['provider', 'host_url', 'provider_api_key', 'assistant', 'name', 'class_name', 'description',
                     'vectorizer', 'vectorizer_api_key', 'embedding_chunk_size', 'embedding_chunk_overlap',
                     'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']

    list_per_page = 20
    list_max_show_all = 100

    def save_model(self, request, obj, form, change):
        if obj.vectorizer is None:
            obj.vectorizer = "text2vec-openai"

        if obj.class_name is None:
            obj.class_name = generate_class_name(obj)

        client = KnowledgeBaseSystemDecoder.get(obj)
        if client is not None:
            result = client.create_weaviate_classes()
            if not result["status"]:
                print(f"Error creating Weaviate classes: {result['error']}")

        # Retrieve the schema
        obj.schema_json = client.retrieve_schema()
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        client = KnowledgeBaseSystemDecoder.get(obj)
        if client is not None:
            result = client.delete_weaviate_classes(class_name=obj.class_name)
            if not result["status"]:
                print(f"Error deleting Weaviate classes: {result['error']}")
        super().delete_model(request, obj)


@admin.register(KnowledgeBaseDocument)
class KnowledgeBaseDocumentAdmin(admin.ModelAdmin):
    list_display = ['knowledge_base', 'document_type', 'document_file_name', 'document_description',
                    'document_metadata', 'document_uri',
                    'created_at', 'updated_at']
    list_filter = ['knowledge_base', 'document_type', 'document_file_name', 'document_description',
                     'document_metadata', 'document_uri',
                     'created_at', 'updated_at']
    search_fields = ['knowledge_base', 'document_type', 'document_file_name', 'document_description',
                     'document_metadata', 'document_uri',
                     'created_at', 'updated_at']
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


@admin.register(KnowledgeBaseDocumentChunk)
class KnowledgeBaseDocumentChunkAdmin(admin.ModelAdmin):
    list_display = ['knowledge_base', 'document', 'chunk_document_type', 'chunk_document_uri', 'knowledge_base_uuid',
                    'document_uuid', 'created_at']
    list_filter = ['document', 'chunk_document_type', 'knowledge_base_uuid', 'document_uuid', 'created_at']
    search_fields = ['document', 'chunk_document_type', 'chunk_content', 'chunk_metadata', 'chunk_document_uri', 'knowledge_base_uuid', 'created_at']
    readonly_fields = ['created_at']

    list_per_page = 20
    list_max_show_all = 100
