#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: voidforger_toggle_auto_execution_logs_admin.py
#  Last Modified: 2024-11-15 17:34:40
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-15 17:34:40
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

from apps.voidforger.models import VoidForgerToggleAutoExecutionLog
from apps.voidforger.utils import VOIDFORGER_TOGGLE_AUTO_EXECUTION_LOG_ADMIN_LIST, \
    VOIDFORGER_TOGGLE_AUTO_EXECUTION_LOG_ADMIN_FILTER, VOIDFORGER_TOGGLE_AUTO_EXECUTION_LOG_ADMIN_SEARCH


@admin.register(VoidForgerToggleAutoExecutionLog)
class VoidForgerToggleAutoExecutionLogAdmin(admin.ModelAdmin):
    list_display = VOIDFORGER_TOGGLE_AUTO_EXECUTION_LOG_ADMIN_LIST
    list_filter = VOIDFORGER_TOGGLE_AUTO_EXECUTION_LOG_ADMIN_FILTER
    search_fields = VOIDFORGER_TOGGLE_AUTO_EXECUTION_LOG_ADMIN_SEARCH
    ordering = ['-timestamp']
