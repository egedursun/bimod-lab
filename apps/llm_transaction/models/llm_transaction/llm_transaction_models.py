#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
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
#   For permission inquiries, please contact: admin@Bimod.io.
#

import decimal

from django.db import models

from apps.llm_transaction.utils import (
    TOKENIZATION_ENCODING_ENGINES,
    LLM_TRANSACTION_ROLES_FOR_TYPE,
    SOURCES_OF_LLM_TRANSACTION,
    calculate_total_tokens,
    calculate_tool_cost,
    InvoiceTypesNames,
    AcceptedMethodsOfPaymentNames,
    LLM_TOKEN_TYPES,
    calculate_billable_cost,
)


class LLMTransaction(models.Model):
    responsible_user = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        related_name='transactions',
        null=True,
        blank=True
    )

    responsible_assistant = models.ForeignKey(
        'assistants.Assistant',
        on_delete=models.SET_NULL,
        related_name='transactions',
        null=True,
        blank=True
    )

    organization = models.ForeignKey(
        'organization.Organization',
        on_delete=models.SET_NULL,
        related_name='transactions',
        null=True
    )

    model = models.ForeignKey(
        'llm_core.LLMCore',
        on_delete=models.SET_NULL,
        related_name='transactions',
        null=True
    )

    encoding_engine = models.CharField(
        max_length=100,
        choices=TOKENIZATION_ENCODING_ENGINES,
        default="cl100k_base"
    )

    transaction_context_content = models.TextField(default="", blank=True)
    number_of_tokens = models.IntegerField(null=True, blank=True)

    total_billable_cost = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=True,
        blank=True
    )

    transaction_type = models.CharField(
        max_length=100,
        choices=LLM_TRANSACTION_ROLES_FOR_TYPE,
        default="system"
    )

    llm_token_type = models.CharField(
        max_length=100,
        choices=LLM_TOKEN_TYPES,
        default="output",
    )

    transaction_source = models.CharField(
        max_length=100,
        choices=SOURCES_OF_LLM_TRANSACTION,
        default="application"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    is_tool_cost = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.organization} - {self.model} - {self.created_at}"

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=[
                'organization'
            ]),
            models.Index(fields=[
                'model'
            ]),
            models.Index(fields=[
                'created_at'
            ]),
            models.Index(fields=[
                'organization',
                'model',
                'created_at'
            ]),
            models.Index(fields=[
                'organization',
                'created_at'
            ]),
            models.Index(fields=[
                'model',
                'created_at'
            ]),
        ]

    def save(self, *args, **kwargs):
        from apps.llm_transaction.models import (
            TransactionInvoice
        )

        if self.organization.balance < 0:
            raise ValueError("Organization does not have enough balance to perform this transaction.")

        try:
            if (
                self.is_tool_cost is False
            ):
                if not self.transaction_context_content:
                    self.transaction_context_content = ""

                self.number_of_tokens = calculate_total_tokens(
                    encoding_engine=self.encoding_engine,
                    text=self.transaction_context_content
                )

                self.total_billable_cost = calculate_billable_cost(
                    total_tokens=self.number_of_tokens,
                    token_type=self.llm_token_type,
                )

        except Exception as e:
            raise ValueError(f"Failed to calculate the cost of the transaction (Standard Transaction). Error: {e}")

        try:
            if self.is_tool_cost:
                self.total_billable_cost = calculate_tool_cost(
                    transaction_source=self.transaction_source,
                )

        except Exception as e:
            raise ValueError(f"Failed to calculate the cost of the transaction (Tool Cost Transaction). Error: {e}")

        try:
            self.organization.balance -= decimal.Decimal().from_float(
                self.total_billable_cost
            )

            self.organization.save()

        except Exception as e:
            raise ValueError(f"Failed to deduct the cost from the organization's balance. Error: {e}")

        try:
            if (
                self.organization.auto_balance_topup and
                self.organization.auto_balance_topup.on_balance_threshold_trigger
            ):
                if self.organization.balance <= self.organization.auto_balance_topup.balance_lower_trigger_threshold_value:
                    if (
                        (
                            self.organization.auto_balance_topup.calendar_month_total_auto_addition_value +
                            self.organization.auto_balance_topup.addition_on_balance_threshold_trigger
                        ) <=
                        self.organization.auto_balance_topup.monthly_hard_limit_auto_addition_amount
                    ):

                        self.organization.balance += (
                            self.organization.auto_balance_topup.addition_on_balance_threshold_trigger
                        )

                        self.organization.save()

                        TransactionInvoice.objects.create(
                            organization=self.organization,
                            responsible_user=self.responsible_user,
                            transaction_type=InvoiceTypesNames.AUTO_TOP_UP,
                            amount_added=self.organization.auto_balance_topup.addition_on_balance_threshold_trigger,
                            payment_method=AcceptedMethodsOfPaymentNames.CREDIT_CARD,
                        )

                        self.organization.auto_balance_topup.calendar_month_total_auto_addition_value += (
                            self.organization.auto_balance_topup.addition_on_balance_threshold_trigger
                        )

                        self.organization.auto_balance_topup.save()

                    else:
                        reduced_addition_amount = (
                            self.organization.auto_balance_topup.monthly_hard_limit_auto_addition_amount - self.organization.auto_balance_topup.calendar_month_total_auto_addition_value
                        )

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

                            self.organization.auto_balance_topup.calendar_month_total_auto_addition_value += (
                                reduced_addition_amount
                            )

                            self.organization.auto_balance_topup.save()

                        else:
                            pass

        except Exception as e:
            raise ValueError(f"Failed to auto top-up the organization's balance. Error: {e}")

        self.transaction_context_content = ""

        super().save(*args, **kwargs)
