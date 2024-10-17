#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: knowledge_base_admin.py
#  Last Modified: 2024-10-05 01:39:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:47
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
#
#
#

from django.contrib import admin

from apps.core.vector_operations.vector_document.vector_store_decoder import KnowledgeBaseSystemDecoder
from apps.datasource_knowledge_base.models import DocumentKnowledgeBaseConnection
from apps.datasource_knowledge_base.utils import build_weaviate_class_name, DOCUMENT_VECTOR_STORE_CONNECTION_ADMIN_LIST, \
    DOCUMENT_VECTOR_STORE_CONNECTION_ADMIN_FILTER, DOCUMENT_VECTOR_STORE_CONNECTION_ADMIN_SEARCH


@admin.register(DocumentKnowledgeBaseConnection)
class DocumentKnowledgeBaseConnectionAdmin(admin.ModelAdmin):
    list_display = DOCUMENT_VECTOR_STORE_CONNECTION_ADMIN_LIST
    list_filter = DOCUMENT_VECTOR_STORE_CONNECTION_ADMIN_FILTER
    search_fields = DOCUMENT_VECTOR_STORE_CONNECTION_ADMIN_SEARCH
    readonly_fields = ['created_at', 'updated_at']

    def save_model(self, request, obj, form, change):
        if obj.vectorizer is None:
            obj.vectorizer = "text2vec-openai"
        if obj.class_name is None:
            obj.class_name = build_weaviate_class_name(obj)

        c = KnowledgeBaseSystemDecoder.get(obj)
        if c is not None:
            o = c.create_weaviate_classes()
            if not o["status"]:
                pass

        obj.schema_json = c.retrieve_schema()
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        c = KnowledgeBaseSystemDecoder.get(obj)
        if c is not None:
            o = c.delete_weaviate_classes(class_name=obj.class_name)
            if not o["status"]:
                pass
        super().delete_model(request, obj)
