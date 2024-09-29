#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: llm_transaction_models.py
#  Last Modified: 2024-09-28 15:44:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:56:59
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

import decimal

from django.db import models


from apps.llm_transaction.utils import ENCODING_ENGINES, TRANSACTION_TYPE_ROLES, TRANSACTION_SOURCES, \
    calculate_number_of_tokens, calculate_llm_cost, calculate_internal_service_cost, calculate_tax_cost, \
    calculate_billable_cost, calculate_total_cost, InvoiceTypesNames, PaymentMethodsNames


class LLMTransaction(models.Model):
    """
    LLMTransaction Model:
    - Purpose: Represents a transaction related to language model operations, storing details such as the number of tokens used, costs associated with the transaction, and the source and type of the transaction.
    - Key Fields:
        - `responsible_user`: ForeignKey linking to the `User` who initiated the transaction.
        - `responsible_assistant`: ForeignKey linking to the `Assistant` involved in the transaction.
        - `organization`: ForeignKey linking to the `Organization` associated with the transaction.
        - `model`: ForeignKey linking to the `LLMCore` model used in the transaction.
        - `encoding_engine`: The encoding engine used for tokenizing the transaction content.
        - `transaction_context_content`: The content involved in the transaction.
        - `number_of_tokens`: The number of tokens used in the transaction.
        - `llm_cost`, `internal_service_cost`, `tax_cost`, `total_cost`, `total_billable_cost`: Fields for storing the calculated costs associated with the transaction.
        - `transaction_type`, `transaction_source`: Fields for categorizing the transaction.
        - `created_at`: Timestamp for when the transaction was created.
        - `is_tool_cost`: Boolean flag to indicate if the transaction is related to a tool.
    - Methods:
        - `save()`: Overridden to calculate tokens and costs, update the organization's balance, and handle auto-balance top-ups if needed.
    - Meta:
        - `verbose_name`: "Transaction"
        - `verbose_name_plural`: "Transactions"
        - `ordering`: Orders transactions by creation date in descending order.
        - `indexes`: Indexes on various fields for optimized queries.
    """

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
    encoding_engine = models.CharField(max_length=100, choices=ENCODING_ENGINES, default="cl100k_base")
    transaction_context_content = models.TextField(default="", blank=True)

    number_of_tokens = models.IntegerField(null=True, blank=True)
    llm_cost = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    internal_service_cost = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    tax_cost = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    total_billable_cost = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)

    transaction_type = models.CharField(max_length=100, choices=TRANSACTION_TYPE_ROLES, default="system")
    transaction_source = models.CharField(max_length=100, choices=TRANSACTION_SOURCES, default="application")

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
            self.number_of_tokens = calculate_number_of_tokens(self.encoding_engine, self.transaction_context_content)
            # Calculate the costs
            self.llm_cost = calculate_llm_cost(self.model.model_name, self.number_of_tokens)
            self.internal_service_cost = calculate_internal_service_cost(self.llm_cost)
            self.tax_cost = calculate_tax_cost(self.internal_service_cost)
            self.total_billable_cost = calculate_billable_cost(self.internal_service_cost, self.tax_cost)
            self.total_cost = calculate_total_cost(self.llm_cost, self.total_billable_cost)

        # for tool transactions
        if self.is_tool_cost:
            self.internal_service_cost = calculate_internal_service_cost(self.llm_cost)
            self.tax_cost = calculate_tax_cost(self.internal_service_cost)
            self.total_billable_cost = calculate_billable_cost(self.internal_service_cost, self.tax_cost)
            self.total_cost = calculate_total_cost(self.llm_cost, self.total_billable_cost)

        # Reduce the transaction billable amount from the organization's balance
        self.organization.balance -= decimal.Decimal().from_float(self.total_billable_cost)
        # Update the transaction's organization
        self.organization.save()

        # check if the organization's auto top-up is enabled
        if self.organization.auto_balance_topup and self.organization.auto_balance_topup.on_balance_threshold_trigger:
            if self.organization.balance <= self.organization.auto_balance_topup.balance_lower_trigger_threshold_value:
                # check if the addition amount is within the monthly hard limit
                if ((
                    self.organization.auto_balance_topup.calendar_month_total_auto_addition_value +
                    self.organization.auto_balance_topup.addition_on_balance_threshold_trigger) <=
                    self.organization.auto_balance_topup.monthly_hard_limit_auto_addition_amount):
                    # Perform the top-up
                    self.organization.balance += self.organization.auto_balance_topup.addition_on_balance_threshold_trigger
                    self.organization.save()

                    ############################################
                    # Create the invoice for the transaction
                    TransactionInvoice.objects.create(
                        organization=self.organization,
                        responsible_user=self.responsible_user,
                        transaction_type=InvoiceTypesNames.AUTO_TOP_UP,
                        amount_added=self.organization.auto_balance_topup.addition_on_balance_threshold_trigger,
                        payment_method=PaymentMethodsNames.CREDIT_CARD,
                    )
                    ############################################

                    # Update the  calendar month total
                    self.organization.auto_balance_topup.calendar_month_total_auto_addition_value += self.organization.auto_balance_topup.addition_on_balance_threshold_trigger
                    self.organization.auto_balance_topup.save()
                else:
                    # If the hard limit is reached, subtract the excess from the total
                    reduced_addition_amount = (
                        self.organization.auto_balance_topup.monthly_hard_limit_auto_addition_amount - self.organization.auto_balance_topup.calendar_month_total_auto_addition_value)
                    # Perform the top-up if there is still a balance that can be added
                    if reduced_addition_amount > 0:
                        # Perform the top-up
                        self.organization.balance += reduced_addition_amount
                        self.organization.save()

                        ############################################
                        # Create the invoice for the transaction
                        TransactionInvoice.objects.create(
                            organization=self.organization,
                            responsible_user=self.responsible_user,
                            transaction_type=InvoiceTypesNames.AUTO_TOP_UP,
                            amount_added=reduced_addition_amount,
                            payment_method=PaymentMethodsNames.CREDIT_CARD,
                        )
                        ############################################

                        # Update the calendar month total
                        self.organization.auto_balance_topup.calendar_month_total_auto_addition_value += reduced_addition_amount
                        self.organization.auto_balance_topup.save()
                    else:
                        # If the reduced addition amount is 0, do nothing
                        print("[LLMTransaction.save] Hard limit reached, no top-up performed for organization: ",
                              self.organization)
        self.transaction_context_content = ""
        super().save(*args, **kwargs)
