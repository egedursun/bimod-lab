#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: context_history_base_admin.py
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

from apps.core.vector_operations.intra_context_memory.memory_executor import IntraContextMemoryExecutor
from apps.datasource_knowledge_base.models import ContextHistoryKnowledgeBaseConnection
from apps.datasource_knowledge_base.utils import build_weaviate_intra_memory_class_name, INTRA_MEMORY_ADMIN_LIST, \
    INTRA_MEMORY_ADMIN_FILTER, INTRA_MEMORY_ADMIN_SEARCH


@admin.register(ContextHistoryKnowledgeBaseConnection)
class ContextHistoryKnowledgeBaseConnectionAdmin(admin.ModelAdmin):
    list_display = INTRA_MEMORY_ADMIN_LIST
    list_filter = INTRA_MEMORY_ADMIN_FILTER
    search_fields = INTRA_MEMORY_ADMIN_SEARCH
    readonly_fields = ['created_at', 'updated_at']

    def save_model(self, request, obj, form, change):
        if obj.vectorizer is None:
            obj.vectorizer = "text2vec-openai"
        if obj.class_name is None:
            obj.class_name = build_weaviate_intra_memory_class_name()
        super().save_model(request, obj, form, change)
        c = IntraContextMemoryExecutor(connection=obj)
        if c is not None:
            result = c.create_chat_history_classes()
            if not result["status"]:
                pass

    def delete_model(self, request, obj):
        c = IntraContextMemoryExecutor(connection=self)
        if c is not None:
            o = c.delete_chat_history_classes(class_name=obj.class_name)
            if not o["status"]:
                pass
        super().delete_model(request, obj)
