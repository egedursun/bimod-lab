#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: document_chunk_admin.py
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

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
