#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: document_admin.py
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

from django.contrib import admin

from apps.datasource_knowledge_base.models import (
    KnowledgeBaseDocument
)

from apps.datasource_knowledge_base.utils import (
    DOCUMENT_ADMIN_LIST,
    DOCUMENT_ADMIN_FILTER,
    DOCUMENT_ADMIN_SEARCH
)


@admin.register(KnowledgeBaseDocument)
class KnowledgeBaseDocumentAdmin(admin.ModelAdmin):
    list_display = DOCUMENT_ADMIN_LIST
    list_filter = DOCUMENT_ADMIN_FILTER
    search_fields = DOCUMENT_ADMIN_SEARCH

    readonly_fields = [
        'created_at',
        'updated_at'
    ]
