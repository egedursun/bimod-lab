#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: slider_document_admin.py
#  Last Modified: 2024-10-17 16:15:05
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-02 19:56:11
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

from apps.slider.models import SliderDocument
from apps.slider.utils import SLIDER_DOCUMENT_ADMIN_LIST, SLIDER_DOCUMENT_ADMIN_LIST_FILTER, \
    SLIDER_DOCUMENT_ADMIN_SEARCH


@admin.register(SliderDocument)
class SliderDocumentAdmin(admin.ModelAdmin):
    list_display = SLIDER_DOCUMENT_ADMIN_LIST
    list_filter = SLIDER_DOCUMENT_ADMIN_LIST_FILTER
    search_fields = SLIDER_DOCUMENT_ADMIN_SEARCH
    ordering = ('-created_at',)
