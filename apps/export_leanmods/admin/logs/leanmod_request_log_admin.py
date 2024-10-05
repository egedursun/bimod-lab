#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: leanmod_request_log_admin.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:41
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from django.contrib import admin

from apps.export_leanmods.models import LeanmodRequestLog


@admin.register(LeanmodRequestLog)
class LeanmodRequestLogAdmin(admin.ModelAdmin):
    list_display = ("export_lean_assistant", "timestamp")
    list_filter = ("export_lean_assistant", "timestamp")
    search_fields = ("export_lean_assistant", "timestamp")
    date_hierarchy = "timestamp"
    ordering = ["-timestamp"]

    list_per_page = 20
    list_max_show_all = 100
    list_editable = []
