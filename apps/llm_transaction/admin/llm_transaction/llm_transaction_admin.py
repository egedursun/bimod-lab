#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: llm_transaction_admin.py
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

from django.contrib import admin

from apps.llm_transaction.models import (
    LLMTransaction
)

from apps.llm_transaction.utils import (
    TRANSACTION_ADMIN_LIST,
    TRANSACTION_ADMIN_FILTER,
    TRANSACTION_ADMIN_SEARCH
)


@admin.register(LLMTransaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = TRANSACTION_ADMIN_LIST
    list_filter = TRANSACTION_ADMIN_FILTER
    search_fields = TRANSACTION_ADMIN_SEARCH

    ordering = ["-created_at"]
