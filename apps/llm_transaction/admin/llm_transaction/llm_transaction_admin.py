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
#
#
#

import decimal

from django.contrib import admin

from apps.llm_transaction.models import LLMTransaction
from apps.llm_transaction.utils import process_and_calculate_number_of_billable_tokens, calculate_total_llm_model_costs, calculate_service_costs_of_platform, \
    calculate_value_added_tax, calculate_final_billable_cost, calculate_final_cost_total, TRANSACTION_ADMIN_LIST, \
    TRANSACTION_ADMIN_FILTER, TRANSACTION_ADMIN_SEARCH


@admin.register(LLMTransaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = TRANSACTION_ADMIN_LIST
    list_filter = TRANSACTION_ADMIN_FILTER
    search_fields = TRANSACTION_ADMIN_SEARCH
    ordering = ["-created_at"]

    def save_model(self, request, obj, form, change):
        if obj.transaction_context_content:
            obj.number_of_tokens = process_and_calculate_number_of_billable_tokens(obj.encoding_engine, obj.transaction_context_content)
            obj.llm_cost = calculate_total_llm_model_costs(obj.model.model_name, obj.number_of_tokens)
            obj.internal_service_cost = calculate_service_costs_of_platform(obj.llm_cost)
            obj.tax_cost = calculate_value_added_tax(obj.internal_service_cost)
            obj.total_billable_cost = calculate_final_billable_cost(obj.internal_service_cost, obj.tax_cost)
            obj.total_cost = calculate_final_cost_total(obj.llm_cost, obj.total_billable_cost)
        obj.organization.balance -= decimal.Decimal.from_float(obj.total_billable_cost)
        obj.organization.save()
        super().save_model(request, obj, form, change)
