#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: llm_transaction_models.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:43
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

import decimal

from django.db import models

from apps.core.internal_cost_manager.costs_map import TOOL_NAME_TO_COST_MAP
from apps.llm_transaction.utils import TOKENIZATION_ENCODING_ENGINES, LLM_TRANSACTION_ROLES_FOR_TYPE, SOURCES_OF_LLM_TRANSACTION, \
    process_and_calculate_number_of_billable_tokens, calculate_total_llm_model_costs, calculate_service_costs_of_platform, calculate_value_added_tax, \
    calculate_final_billable_cost, calculate_final_cost_total, InvoiceTypesNames, AcceptedMethodsOfPaymentNames


class LLMTransaction(models.Model):
    responsible_user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='transactions',
                                         null=True, blank=True)
    responsible_assistant = models.ForeignKey('assistants.Assistant', on_delete=models.SET_NULL,
                                              related_name='transactions',
                                              null=True, blank=True)
    organization = models.ForeignKey('organization.Organization', on_delete=models.SET_NULL,
                                     related_name='transactions',
                                     null=True)
    model = models.ForeignKey('llm_core.LLMCore', on_delete=models.SET_NULL, related_name='transactions',
                              null=True)
    encoding_engine = models.CharField(max_length=100, choices=TOKENIZATION_ENCODING_ENGINES, default="cl100k_base")
    transaction_context_content = models.TextField(default="", blank=True)
    number_of_tokens = models.IntegerField(null=True, blank=True)
    llm_cost = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    internal_service_cost = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    tax_cost = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    total_billable_cost = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    transaction_type = models.CharField(max_length=100, choices=LLM_TRANSACTION_ROLES_FOR_TYPE, default="system")
    transaction_source = models.CharField(max_length=100, choices=SOURCES_OF_LLM_TRANSACTION, default="application")
    created_at = models.DateTimeField(auto_now_add=True)
    is_tool_cost = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.organization} - {self.model} - {self.created_at}"

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['organization']),
            models.Index(fields=['model']),
            models.Index(fields=['created_at']),
            models.Index(fields=['organization', 'model', 'created_at']),
            models.Index(fields=['organization', 'created_at']),
            models.Index(fields=['model', 'created_at']),
        ]

    def save(self, *args, **kwargs):
        from apps.llm_transaction.models import TransactionInvoice
        if self.transaction_context_content and self.is_tool_cost is False:
            self.number_of_tokens = process_and_calculate_number_of_billable_tokens(self.encoding_engine, self.transaction_context_content)
            self.llm_cost = calculate_total_llm_model_costs(self.model.model_name, self.number_of_tokens)
            self.internal_service_cost = calculate_service_costs_of_platform(self.llm_cost)
            self.tax_cost = calculate_value_added_tax(self.internal_service_cost)
            self.total_billable_cost = calculate_final_billable_cost(self.internal_service_cost, self.tax_cost)
            self.total_cost = calculate_final_cost_total(self.llm_cost, self.total_billable_cost)
        if self.is_tool_cost:
            tool_cost = float(TOOL_NAME_TO_COST_MAP[self.transaction_source]) or 0.000000
            self.internal_service_cost = calculate_service_costs_of_platform(self.llm_cost, tool_service_fee_absolute_rate=tool_cost)
            self.tax_cost = calculate_value_added_tax(self.internal_service_cost)
            self.total_billable_cost = calculate_final_billable_cost(self.internal_service_cost, self.tax_cost)
            self.total_cost = calculate_final_cost_total(self.llm_cost, self.total_billable_cost)

        self.organization.balance -= decimal.Decimal().from_float(self.total_billable_cost)
        self.organization.save()
        if self.organization.auto_balance_topup and self.organization.auto_balance_topup.on_balance_threshold_trigger:
            if self.organization.balance <= self.organization.auto_balance_topup.balance_lower_trigger_threshold_value:
                if ((
                    self.organization.auto_balance_topup.calendar_month_total_auto_addition_value +
                    self.organization.auto_balance_topup.addition_on_balance_threshold_trigger) <=
                    self.organization.auto_balance_topup.monthly_hard_limit_auto_addition_amount):
                    self.organization.balance += self.organization.auto_balance_topup.addition_on_balance_threshold_trigger
                    self.organization.save()

                    TransactionInvoice.objects.create(
                        organization=self.organization,
                        responsible_user=self.responsible_user,
                        transaction_type=InvoiceTypesNames.AUTO_TOP_UP,
                        amount_added=self.organization.auto_balance_topup.addition_on_balance_threshold_trigger,
                        payment_method=AcceptedMethodsOfPaymentNames.CREDIT_CARD,
                    )

                    self.organization.auto_balance_topup.calendar_month_total_auto_addition_value += self.organization.auto_balance_topup.addition_on_balance_threshold_trigger
                    self.organization.auto_balance_topup.save()
                else:
                    reduced_addition_amount = (
                        self.organization.auto_balance_topup.monthly_hard_limit_auto_addition_amount - self.organization.auto_balance_topup.calendar_month_total_auto_addition_value)
                    if reduced_addition_amount > 0:
                        self.organization.balance += reduced_addition_amount
                        self.organization.save()

                        TransactionInvoice.objects.create(
                            organization=self.organization,
                            responsible_user=self.responsible_user,
                            transaction_type=InvoiceTypesNames.AUTO_TOP_UP,
                            amount_added=reduced_addition_amount,
                            payment_method=AcceptedMethodsOfPaymentNames.CREDIT_CARD,
                        )

                        self.organization.auto_balance_topup.calendar_month_total_auto_addition_value += reduced_addition_amount
                        self.organization.auto_balance_topup.save()
                    else:
                        pass
        self.transaction_context_content = ""
        super().save(*args, **kwargs)
