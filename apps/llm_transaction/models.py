"""
Module Overview: This module defines models related to transactions, auto-balance top-ups, and balance snapshots for organizations within an assistant-based application. It includes functionality for calculating transaction costs, managing auto-balance top-ups, and recording balance snapshots for organizations.

Dependencies:
- `decimal`: Python's module for decimal fixed-point and floating-point arithmetic.
- `django.db.models`: Django's ORM for defining database models.
- `apps.llm_transaction.utils`: Utility functions for calculating tokens, costs, and other transaction-related values.
"""

import decimal
import uuid
from decimal import Decimal

from django.db import models
from django.utils import timezone

from apps.llm_transaction.utils import calculate_number_of_tokens, calculate_llm_cost, calculate_internal_service_cost, \
    calculate_tax_cost, calculate_total_cost, calculate_billable_cost, invoice_paper_generator
from .utils import barcode_generator


ENCODING_ENGINES = [
    ("cl100k_base", "cl100k_base"),
    ("p50k_base", "p50k_base"),
    ("r50k_base", "r50k_base"),
]

TRANSACTION_TYPE_ROLES = [
    ("user", "User"),
    ("assistant", "Assistant"),
    ("system", "System"),
]

TRANSACTION_SOURCES = [
    ("app", "Application"),
    ("api", "API"),
    ("generation", "Generation"),
    ("sql-read", "SQL Read"),
    ("sql-write", "SQL Write"),
    ("store-memory", "Store Memory"),
    ("interpret-code", "Interpret Code"),
    ("download-file", "Download File"),
    ("file-system-commands", "File System Commands"),
    ("knowledge-base-search", "Knowledge Base Search"),
    ("retrieve-memory", "Retrieve Memory"),
    ("ml-model-prediction", "ML Model Prediction"),
    ("internal-function-execution", "Internal Function Execution"),
    ("external-function-execution", "External Function Execution"),
    ("interpret-file", "Interpret File"),
    ("interpret-image", "Interpret Image"),
]


class TransactionTypeRolesNames:
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class TransactionSourcesNames:
    APP = "app"
    API = "api"
    ############################
    GENERATION = "generation"
    SQL_READ = "sql-read"
    SQL_WRITE = "sql-write"
    STORE_MEMORY = "store-memory"
    INTERPRET_CODE = "interpret-code"
    UPLOAD_FILE = "upload-file"
    DOWNLOAD_FILE = "download-file"
    FILE_SYSTEM_COMMANDS = "file-system-commands"
    KNOWLEDGE_BASE_SEARCH = "knowledge-base-search"
    CODE_BASE_SEARCH = "code-base-search"
    RETRIEVE_MEMORY = "retrieve-memory"
    ML_MODEL_PREDICTION = "ml-model-prediction"
    BROWSING = "browsing"
    INTERNAL_FUNCTION_EXECUTION = "internal-function-execution"
    EXTERNAL_FUNCTION_EXECUTION = "external-function-execution"
    INTERNAL_API_EXECUTION = "internal-api-execution"
    EXTERNAL_API_EXECUTION = "external-api-execution"
    INTERNAL_SCRIPT_RETRIEVAL = "internal-script-retrieval"
    EXTERNAL_SCRIPT_RETRIEVAL = "external-script-retrieval"
    INTERPRET_FILE = "interpret-file"
    INTERPRET_IMAGE = "interpret-image"
    SCHEDULED_JOB_EXECUTION = "scheduled-job-execution"
    TRIGGER_JOB_EXECUTION = "trigger-job-execution"
    GENERATE_IMAGE = "generate-image"
    MODIFY_IMAGE = "modify-image"
    VARIATE_IMAGE = "variate-image"

    @staticmethod
    def as_list():
        return [
            TransactionSourcesNames.APP,
            TransactionSourcesNames.API,
            TransactionSourcesNames.GENERATION,
            TransactionSourcesNames.SQL_READ,
            TransactionSourcesNames.SQL_WRITE,
            TransactionSourcesNames.STORE_MEMORY,
            TransactionSourcesNames.INTERPRET_CODE,
            TransactionSourcesNames.UPLOAD_FILE,
            TransactionSourcesNames.DOWNLOAD_FILE,
            TransactionSourcesNames.FILE_SYSTEM_COMMANDS,
            TransactionSourcesNames.KNOWLEDGE_BASE_SEARCH,
            TransactionSourcesNames.RETRIEVE_MEMORY,
            TransactionSourcesNames.CODE_BASE_SEARCH,
            TransactionSourcesNames.ML_MODEL_PREDICTION,
            TransactionSourcesNames.BROWSING,
            TransactionSourcesNames.INTERNAL_FUNCTION_EXECUTION,
            TransactionSourcesNames.EXTERNAL_FUNCTION_EXECUTION,
            TransactionSourcesNames.INTERNAL_API_EXECUTION,
            TransactionSourcesNames.EXTERNAL_API_EXECUTION,
            TransactionSourcesNames.INTERNAL_SCRIPT_RETRIEVAL,
            TransactionSourcesNames.EXTERNAL_SCRIPT_RETRIEVAL,
            TransactionSourcesNames.INTERPRET_FILE,
            TransactionSourcesNames.INTERPRET_IMAGE,
            TransactionSourcesNames.SCHEDULED_JOB_EXECUTION,
            TransactionSourcesNames.TRIGGER_JOB_EXECUTION,
            TransactionSourcesNames.GENERATE_IMAGE,
            TransactionSourcesNames.MODIFY_IMAGE,
            TransactionSourcesNames.VARIATE_IMAGE,
        ]


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
                if (
                    self.organization.auto_balance_topup.calendar_month_total_auto_addition_value + self.organization.auto_balance_topup.addition_on_balance_threshold_trigger) <= self.organization.auto_balance_topup.monthly_hard_limit_auto_addition_amount:
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


class AutoBalanceTopUpModel(models.Model):
    """
    AutoBalanceTopUpModel:
    - Purpose: Represents the configuration for automatically topping up an organization's balance, with triggers based on balance thresholds or regular intervals.
    - Key Fields:
        - `organization`: ForeignKey linking to the `Organization` that the top-up configuration applies to.
        - `on_balance_threshold_trigger`: Boolean flag indicating if the top-up is triggered by a balance threshold.
        - `on_interval_by_days_trigger`: Boolean flag indicating if the top-up is triggered by regular intervals.
        - `balance_lower_trigger_threshold_value`, `addition_on_balance_threshold_trigger`: Fields related to the balance threshold trigger.
        - `regular_by_days_interval`, `addition_on_interval_by_days_trigger`, `date_of_last_auto_top_up`: Fields related to the interval trigger.
        - `calendar_month_total_auto_addition_value`, `monthly_hard_limit_auto_addition_amount`: Fields for tracking and limiting the total auto-addition value within a month.
        - `created_at`, `updated_at`: Timestamps for creation and last update.
    - Meta:
        - `verbose_name`: "Auto Balance Top Up"
        - `verbose_name_plural`: "Auto Balance Top Ups"
        - `ordering`: Orders top-up configurations by creation date in descending order.
    """

    organization = models.ForeignKey('organization.Organization', on_delete=models.SET_NULL,
                                     related_name='auto_balance_top_ups',
                                     null=True)

    # trigger types
    on_balance_threshold_trigger = models.BooleanField(default=False)
    on_interval_by_days_trigger = models.BooleanField(default=False)

    # on balance threshold parameters
    balance_lower_trigger_threshold_value = models.DecimalField(max_digits=12, decimal_places=6, null=True, blank=True)
    addition_on_balance_threshold_trigger = models.DecimalField(max_digits=12, decimal_places=6, null=True, blank=True)

    # on interval by days parameters
    regular_by_days_interval = models.IntegerField(null=True, blank=True)
    addition_on_interval_by_days_trigger = models.DecimalField(max_digits=12, decimal_places=6, null=True, blank=True)
    date_of_last_auto_top_up = models.DateTimeField(null=True, blank=True)

    # common parameters
    calendar_month_total_auto_addition_value = models.DecimalField(max_digits=12, decimal_places=6, null=True,
                                                                   blank=True)
    monthly_hard_limit_auto_addition_amount = models.DecimalField(max_digits=12, decimal_places=6, null=True,
                                                                  blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.organization} - {self.created_at}"

    class Meta:
        verbose_name = "Auto Balance Top Up"
        verbose_name_plural = "Auto Balance Top Ups"
        ordering = ["-created_at"]


class OrganizationBalanceSnapshot(models.Model):
    """
    OrganizationBalanceSnapshot:
    - Purpose: Represents a snapshot of an organization's balance at a specific point in time, used for tracking financial activity and historical records.
    - Key Fields:
        - `organization`: ForeignKey linking to the `Organization` associated with the balance snapshot.
        - `balance`: The balance of the organization at the time of the snapshot.
        - `created_at`: Timestamp for when the snapshot was created.
    - Meta:
        - `verbose_name`: "Organization Balance Snapshot"
        - `verbose_name_plural`: "Organization Balance Snapshots"
        - `ordering`: Orders balance snapshots by creation date in descending order.
        - `indexes`: Indexes on various fields for optimized queries.
    """

    organization = models.ForeignKey('organization.Organization', on_delete=models.SET_NULL,
                                     related_name='balance_snapshots', null=True)
    balance = models.DecimalField(max_digits=12, decimal_places=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.organization} - {self.balance} - {self.created_at}"

    class Meta:
        verbose_name = "Organization Balance Snapshot"
        verbose_name_plural = "Organization Balance Snapshots"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['organization']),
            models.Index(fields=['created_at']),
            models.Index(fields=['organization', 'created_at']),
        ]


INVOICE_TYPES = [
    ("auto-top-up", "Auto Top-Up"),
    ("top-up", "Top-Up"),
    ("gift-credits", "Gift Credits"),
    ("transferred-credits", "Transferred Credits"),
]


class InvoiceTypesNames:
    AUTO_TOP_UP = "auto-top-up"
    TOP_UP = "top-up"
    GIFT_CREDITS = "gift-credits"
    TRANSFERRED_CREDITS = "transferred-credits"

    @staticmethod
    def as_list():
        return [
            InvoiceTypesNames.AUTO_TOP_UP,
            InvoiceTypesNames.TOP_UP,
            InvoiceTypesNames.GIFT_CREDITS,
            InvoiceTypesNames.TRANSFERRED_CREDITS,
        ]


PAYMENT_METHODS = [
    ("credit-card", "Credit Card"),
    ("internal-transfer", "Internal Transfer"),
]


class PaymentMethodsNames:
    CREDIT_CARD = "credit-card"
    INTERNAL_TRANSFER = "internal-transfer"

    @staticmethod
    def as_list():
        return [
            PaymentMethodsNames.CREDIT_CARD,
            PaymentMethodsNames.INTERNAL_TRANSFER,
        ]


class TransactionInvoice(models.Model):
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE,
                                     related_name='transaction_invoices')
    responsible_user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='transaction_invoices',
                                         null=True, blank=True)
    transaction_type = models.CharField(max_length=50, choices=INVOICE_TYPES, default="top-up")
    amount_added = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS, default="credit-card")
    transaction_date = models.DateTimeField(auto_now_add=True)
    invoice_number = models.CharField(max_length=2000, null=True, blank=True)
    barcode_image = models.ImageField(upload_to='invoice_barcodes/%Y/%m/%d/', null=True, blank=True)
    transaction_paper = models.FileField(upload_to='transaction_papers/%Y/%m/%d/', null=True, blank=True)

    def __str__(self):
        return f"Invoice {self.invoice_number} @ {self.organization} by {self.responsible_user} on {self.transaction_date}"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.pk:
            # Handle new record creation
            self.transaction_date = timezone.now()
            current_date = self.transaction_date.strftime("%Y%m%d")
            current_year = self.transaction_date.strftime("%Y")
            current_month = self.transaction_date.strftime("%m")
            current_day = self.transaction_date.strftime("%d")
            hashed_date = str(hash(current_date))
            org_id = str(self.organization.id)
            hashed_org_id = str(hash(org_id))
            user_id = str(self.responsible_user.id)
            hashed_user_id = str(hash(user_id))
            random_uuid = str(uuid.uuid4().hex)
            hashed_amount = str(hash(self.amount_added))
            hashed_payment_method = str(hash(self.payment_method))

            # Combine all the hashes
            combined_hash = f"BIMOD-{current_year}{current_month}{current_day}-{org_id}{user_id}{random_uuid}-{hashed_date}{hashed_org_id}{hashed_user_id}{hashed_amount}{hashed_payment_method}".upper()
            self.invoice_number = combined_hash

            # Generate the barcode image
            barcode = barcode_generator(combined_hash)
            if barcode:
                self.barcode_image = barcode

            # Generate the invoice paper
            filename, invoice_paper = invoice_paper_generator(self, barcode)
            if invoice_paper:
                self.transaction_paper.save(filename, invoice_paper, save=False)

            # Call save with update_fields when all fields are initially set
            super().save(force_insert, force_update, using, update_fields)
        else:
            # For existing records, just call the base class save method
            super().save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = "Transaction Invoice"
        verbose_name_plural = "Transaction Invoices"
        ordering = ["-transaction_date"]
        indexes = [
            models.Index(fields=['organization']),
            models.Index(fields=['responsible_user']),
            models.Index(fields=['transaction_date']),
            models.Index(fields=['organization', 'transaction_date']),
            models.Index(fields=['organization', 'responsible_user', 'transaction_date']),
        ]
