#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: custom_script_admin.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:38
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

from apps.mm_scripts.models import CustomScript
from apps.mm_scripts.utils import CUSTOM_SCRIPT_ADMIN_LIST, CUSTOM_SCRIPT_ADMIN_SEARCH, CUSTOM_SCRIPT_ADMIN_LIST_FILTER


@admin.register(CustomScript)
class CustomScriptAdmin(admin.ModelAdmin):
    list_display = CUSTOM_SCRIPT_ADMIN_LIST
    list_filter = CUSTOM_SCRIPT_ADMIN_LIST_FILTER
    search_fields = CUSTOM_SCRIPT_ADMIN_SEARCH
    ordering = ("-created_at",)
