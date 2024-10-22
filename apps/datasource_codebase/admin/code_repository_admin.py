#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: code_repository_admin.py
#  Last Modified: 2024-10-05 01:39:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:46
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
import logging

from django.contrib import admin

from apps.core.codebase.codebase_decoder import CodeBaseDecoder
from apps.datasource_codebase.models import CodeBaseRepository
from django.contrib.admin.actions import delete_selected as django_delete_selected

from apps.datasource_codebase.utils import CODEBASE_REPOSITORY_ADMIN_LIST, CODEBASE_REPOSITORY_ADMIN_FILTER, \
    CODEBASE_REPOSITORY_ADMIN_SEARCH


logger = logging.getLogger(__name__)


@admin.register(CodeBaseRepository)
class CodeBaseRepositoryAdmin(admin.ModelAdmin):
    list_display = CODEBASE_REPOSITORY_ADMIN_LIST
    list_filter = CODEBASE_REPOSITORY_ADMIN_FILTER
    search_fields = CODEBASE_REPOSITORY_ADMIN_SEARCH
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
                    logger.error(f"Failed to delete document from Weaviate.")
        return django_delete_selected(self, request, queryset)
