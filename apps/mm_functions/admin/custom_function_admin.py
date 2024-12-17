#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: custom_function_admin.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:39
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

from apps.mm_functions.models import (
    CustomFunction
)

from apps.mm_functions.utils import (
    CUSTOM_FUNCTION_ADMIN_LIST,
    CUSTOM_FUNCTION_ADMIN_FILTER,
    CUSTOM_FUNCTION_ADMIN_SEARCH
)


@admin.register(CustomFunction)
class CustomFunctionAdmin(admin.ModelAdmin):
    list_display = CUSTOM_FUNCTION_ADMIN_LIST
    list_filter = CUSTOM_FUNCTION_ADMIN_FILTER
    search_fields = CUSTOM_FUNCTION_ADMIN_SEARCH

    ordering = ("-created_at",)
