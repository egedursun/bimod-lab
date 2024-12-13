#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: voidforger_admin.py
#  Last Modified: 2024-11-15 17:33:10
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-15 17:33:10
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

from apps.voidforger.models import (
    VoidForger
)

from apps.voidforger.utils import (
    VOIDFORGER_ADMIN_LIST,
    VOIDFORGER_ADMIN_FILTER,
    VOIDFORGER_ADMIN_SEARCH
)


@admin.register(VoidForger)
class VoidForgerAdmin(admin.ModelAdmin):
    list_display = VOIDFORGER_ADMIN_LIST
    list_filter = VOIDFORGER_ADMIN_FILTER
    search_fields = VOIDFORGER_ADMIN_SEARCH

    ordering = ('-created_at',)
