import datetime
import decimal

from django.db import models

from apps.llm_transaction.utils import calculate_number_of_tokens, calculate_llm_cost, calculate_internal_service_cost, \
    calculate_tax_cost, calculate_total_cost, calculate_billable_cost

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
    GENERATION = "generation"
    SQL_READ = "sql-read"
    SQL_WRITE = "sql-write"
    STORE_MEMORY = "store-memory"
    INTERPRET_CODE = "interpret-code"
    DOWNLOAD_FILE = "download-file"
    FILE_SYSTEM_COMMANDS = "file-system-commands"
    KNOWLEDGE_BASE_SEARCH = "knowledge-base-search"
    RETRIEVE_MEMORY = "retrieve-memory"
    CODE_REPOSITORY_SEARCH = "code-repository-search"
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
    GENERATE_IMAGE = "generate-image"
    MODIFY_IMAGE = "modify-image"
    VARIATE_IMAGE = "variate-image"


# Create your models here.

class LLMTransaction(models.Model):
    responsible_user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='transactions', null=True, blank=True)
    responsible_assistant = models.ForeignKey('assistants.Assistant', on_delete=models.SET_NULL,
                                              related_name='transactions',
                                              null=True, blank=True)
    organization = models.ForeignKey('organization.Organization', on_delete=models.SET_NULL, related_name='transactions',
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
                if (self.organization.auto_balance_topup.calendar_month_total_auto_addition_value + self.organization.auto_balance_topup.addition_on_balance_threshold_trigger) <= self.organization.auto_balance_topup.monthly_hard_limit_auto_addition_amount:
                    # Perform the top-up
                    self.organization.balance += self.organization.auto_balance_topup.addition_on_balance_threshold_trigger
                    self.organization.save()
                    # Update the  calendar month total
                    self.organization.auto_balance_topup.calendar_month_total_auto_addition_value += self.organization.auto_balance_topup.addition_on_balance_threshold_trigger
                    self.organization.auto_balance_topup.save()
                else:
                    # If the hard limit is reached, subtract the excess from the total
                    reduced_addition_amount = (self.organization.auto_balance_topup.monthly_hard_limit_auto_addition_amount - self.organization.auto_balance_topup.calendar_month_total_auto_addition_value)
                    # Perform the top-up if there is still a balance that can be added
                    if reduced_addition_amount > 0:
                        # Perform the top-up
                        self.organization.balance += reduced_addition_amount
                        self.organization.save()
                        # Update the calendar month total
                        self.organization.auto_balance_topup.calendar_month_total_auto_addition_value += reduced_addition_amount
                        self.organization.auto_balance_topup.save()
                    else:
                        # If the reduced addition amount is 0, do nothing
                        print("Hard limit reached, no top-up performed for organization: ", self.organization)

        self.transaction_context_content = ""
        super().save(*args, **kwargs)


class AutoBalanceTopUpModel(models.Model):
    organization = models.ForeignKey('organization.Organization', on_delete=models.SET_NULL, related_name='auto_balance_top_ups',
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
    calendar_month_total_auto_addition_value = models.DecimalField(max_digits=12, decimal_places=6, null=True, blank=True)
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
    organization = models.ForeignKey('organization.Organization', on_delete=models.SET_NULL, related_name='balance_snapshots',
                                        null=True)
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
