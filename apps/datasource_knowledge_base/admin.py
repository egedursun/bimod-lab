from django.contrib import admin

from apps._services.knowledge_base.document.knowledge_base_decoder import KnowledgeBaseSystemDecoder
from apps.datasource_knowledge_base.models import DocumentKnowledgeBaseConnection
from apps.datasource_knowledge_base.utils import generate_class_name


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
            self.vectorizer = "text2vec-openai"

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
