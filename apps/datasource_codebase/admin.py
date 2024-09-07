from django.contrib import admin

from apps._services.codebase.codebase_decoder import CodeBaseDecoder
from apps.datasource_codebase.models import CodeRepositoryStorageConnection, CodeBaseRepository, \
    CodeBaseRepositoryChunk, RepositoryProcessingLog
from apps.datasource_codebase.utils import generate_class_name
from django.contrib.admin.actions import delete_selected as django_delete_selected


@admin.register(CodeRepositoryStorageConnection)
class CodeRepositoryStorageConnectionAdmin(admin.ModelAdmin):
    list_display = ['provider', 'host_url', 'provider_api_key', 'assistant', 'name', 'class_name', 'description',
                    'vectorizer', 'vectorizer_api_key', 'embedding_chunk_size', 'embedding_chunk_overlap',
                    'search_instance_retrieval_limit', 'created_at', 'updated_at']
    list_filter = ['provider', 'host_url', 'provider_api_key', 'assistant', 'name', 'class_name', 'description',
                   'vectorizer', 'vectorizer_api_key', 'embedding_chunk_size', 'embedding_chunk_overlap',
                   'created_at', 'updated_at']
    search_fields = ['provider', 'host_url', 'provider_api_key', 'assistant', 'name', 'class_name', 'description',
                     'vectorizer', 'vectorizer_api_key', 'embedding_chunk_size', 'embedding_chunk_overlap',
                     'search_instance_retrieval_limit', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']

    list_per_page = 20
    list_max_show_all = 100

    def save_model(self, request, obj, form, change):
        if obj.vectorizer is None:
            obj.vectorizer = "text2vec-openai"

        if obj.class_name is None:
            obj.class_name = generate_class_name(obj)

        client = CodeBaseDecoder.get(obj)
        if client is not None:
            result = client.create_weaviate_classes()
            if not result["status"]:
                print(f"[CodeRepositoryStorageConnectionAdmin.save_model] Error creating Weaviate classes: {result['error']}")

        # Retrieve the schema
        obj.schema_json = client.retrieve_schema()
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        client = CodeBaseDecoder.get(obj)
        if client is not None:
            result = client.delete_weaviate_classes(class_name=obj.class_name)
            if not result["status"]:
                print(f"[CodeRepositoryStorageConnectionAdmin.delete_model] Error deleting Weaviate classes: {result['error']}")
        super().delete_model(request, obj)


@admin.register(CodeBaseRepository)
class CodeBaseRepositoryAdmin(admin.ModelAdmin):
    list_display = ['knowledge_base', 'repository_name', 'repository_description',
                    'repository_metadata', 'repository_uri', 'created_at', 'updated_at']
    list_filter = ['knowledge_base', 'repository_name', 'repository_description',
                    'repository_metadata', 'repository_uri', 'created_at', 'updated_at']
    search_fields = ['knowledge_base', 'repository_name', 'repository_description',
                    'repository_metadata', 'repository_uri', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']

    list_per_page = 20
    list_max_show_all = 100

    def delete_selected(self, request, queryset):
        for obj in queryset:
            client = CodeBaseDecoder.get(obj.knowledge_base)
            if client is not None:
                result = client.delete_weaviate_document(
                    class_name=obj.knowledge_base.class_name,
                    document_uuid=obj.document_uuid)
                if not result["status"]:
                    print(f"Error deleting Weaviate document: {result['error']}")
        return django_delete_selected(self, request, queryset)


@admin.register(CodeBaseRepositoryChunk)
class CodeBaseRepositoryChunkAdmin(admin.ModelAdmin):
    list_display = ['knowledge_base', 'repository', 'chunk_repository_uri', 'knowledge_base_uuid',
                    'repository_uuid', 'created_at']
    list_filter = ['repository', 'knowledge_base_uuid', 'repository_uuid', 'created_at']
    search_fields = ['repository', 'chunk_content', 'chunk_metadata', 'chunk_repository_uri',
                     'knowledge_base_uuid', 'created_at']
    readonly_fields = ['created_at']

    list_per_page = 20
    list_max_show_all = 100


@admin.register(RepositoryProcessingLog)
class RepositoryProcessingLogAdmin(admin.ModelAdmin):
    list_display = ['repository_full_uri', 'log_message', 'created_at']
    list_filter = ['repository_full_uri', 'log_message', 'created_at']
    search_fields = ['repository_full_uri', 'log_message']
    readonly_fields = ['created_at']

    list_per_page = 20
    list_max_show_all = 100
