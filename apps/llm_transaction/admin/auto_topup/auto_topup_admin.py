#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: auto_topup_admin.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:42
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

from apps.llm_transaction.models import AutoBalanceTopUpModel


@admin.register(AutoBalanceTopUpModel)
class AutoBalanceTopUpModelAdmin(admin.ModelAdmin):
    list_display = ["organization", "on_balance_threshold_trigger", "on_interval_by_days_trigger",
                    "balance_lower_trigger_threshold_value", "addition_on_balance_threshold_trigger"]
    ordering = ["-created_at"]
