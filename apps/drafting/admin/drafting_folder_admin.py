#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: drafting_folder_admin.py
#  Last Modified: 2024-10-14 18:32:55
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-14 18:32:55
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

from apps.drafting.models import DraftingFolder

from apps.drafting.utils import (
    DRAFTING_FOLDER_ADMIN_LIST,
    DRAFTING_FOLDER_ADMIN_FILTER,
    DRAFTING_FOLDER_ADMIN_SEARCH
)


@admin.register(DraftingFolder)
class DraftingFolderAdmin(admin.ModelAdmin):
    list_display = DRAFTING_FOLDER_ADMIN_LIST
    list_filter = DRAFTING_FOLDER_ADMIN_FILTER
    search_fields = DRAFTING_FOLDER_ADMIN_SEARCH
    ordering = ('-created_at',)
