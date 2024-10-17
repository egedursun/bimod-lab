#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
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
#   For permission inquiries, please contact: admin@Bimod.io.
#
#
#
#

from django.contrib import admin

from apps.llm_transaction.models import AutoBalanceTopUpModel
from apps.llm_transaction.utils import AUTO_TOP_UP_ADMIN_LIST


@admin.register(AutoBalanceTopUpModel)
class AutoBalanceTopUpModelAdmin(admin.ModelAdmin):
    list_display = AUTO_TOP_UP_ADMIN_LIST
    ordering = ["-created_at"]
