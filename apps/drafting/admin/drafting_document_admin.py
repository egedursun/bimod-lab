#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: drafting_document_admin.py
#  Last Modified: 2024-10-14 18:31:54
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-14 18:31:55
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

from apps.drafting.models import DraftingDocument
from apps.drafting.utils import DRAFTING_DOCUMENT_ADMIN_LIST, DRAFTING_DOCUMENT_ADMIN_LIST_FILTER, \
    DRAFTING_DOCUMENT_ADMIN_SEARCH


@admin.register(DraftingDocument)
class DraftingDocumentAdmin(admin.ModelAdmin):
    list_display = DRAFTING_DOCUMENT_ADMIN_LIST
    list_filter = DRAFTING_DOCUMENT_ADMIN_LIST_FILTER
    search_fields = DRAFTING_DOCUMENT_ADMIN_SEARCH
    ordering = ('-created_at',)
