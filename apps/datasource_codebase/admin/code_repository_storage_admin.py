#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: code_repository_storage_admin.py
#  Last Modified: 2024-09-26 20:30:21
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:36:44
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib import admin

from apps._services.codebase.codebase_decoder import CodeBaseDecoder
from apps.datasource_codebase.models import CodeRepositoryStorageConnection
from apps.datasource_codebase.utils import generate_class_name


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
                print(
                    f"[CodeRepositoryStorageConnectionAdmin.save_model] Error creating Weaviate classes: {result['error']}")

        # Retrieve the schema
        obj.schema_json = client.retrieve_schema()
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        client = CodeBaseDecoder.get(obj)
        if client is not None:
            result = client.delete_weaviate_classes(class_name=obj.class_name)
            if not result["status"]:
                print(
                    f"[CodeRepositoryStorageConnectionAdmin.delete_model] Error deleting Weaviate classes: {result['error']}")
        super().delete_model(request, obj)
