#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: ellma_script_admin.py
#  Last Modified: 2024-10-30 17:42:07
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-30 17:42:08
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

from apps.ellma.models import EllmaScript

from apps.ellma.utils import (
    ELLMA_SCRIPT_ADMIN_LIST,
    ELLMA_SCRIPT_ADMIN_SEARCH,
    ELLMA_SCRIPT_ADMIN_FILTER
)


@admin.register(EllmaScript)
class EllmaScriptAdmin(admin.ModelAdmin):
    list_display = ELLMA_SCRIPT_ADMIN_LIST
    search_fields = ELLMA_SCRIPT_ADMIN_SEARCH
    list_filter = ELLMA_SCRIPT_ADMIN_FILTER
    ordering = ['-created_at']
