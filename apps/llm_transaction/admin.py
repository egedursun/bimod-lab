import decimal
from django.contrib import admin

from .models import LLMTransaction, AutoBalanceTopUpModel, OrganizationBalanceSnapshot
from .utils import calculate_number_of_tokens, calculate_llm_cost, calculate_internal_service_cost, calculate_tax_cost, \
    calculate_total_cost, calculate_billable_cost


@admin.register(LLMTransaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["responsible_user", "responsible_assistant", "organization", "model", "number_of_tokens",
                    "transaction_type", "transaction_source", "llm_cost", "internal_service_cost", "tax_cost",
                    "total_cost", "created_at"]
    list_filter = ["responsible_user", "responsible_assistant",
                   "transaction_type", "transaction_source",
                   "organization", "model", "created_at"]
    search_fields = ["organization__name", "model__nickname"]
    date_hierarchy = "created_at"
    readonly_fields = ["created_at"]
    fieldsets = (
        (None, {
            "fields": (
                "responsible_user", "responsible_assistant", "organization", "model", "transaction_type",
                "transaction_source", "encoding_engine", "transaction_context_content", "number_of_tokens",
                "llm_cost", "internal_service_cost", "tax_cost", "total_cost", "total_billable_cost",
            )
        }),
        ("Metadata", {"fields": ("created_at",)}),
    )
    ordering = ["-created_at"]

    def save_model(self, request, obj, form, change):
        if obj.transaction_context_content:
            obj.number_of_tokens = calculate_number_of_tokens(obj.encoding_engine, obj.transaction_context_content)
            # Calculate the costs
            obj.llm_cost = calculate_llm_cost(obj.model.model_name, obj.number_of_tokens)
            obj.internal_service_cost = calculate_internal_service_cost(obj.llm_cost)
            obj.tax_cost = calculate_tax_cost(obj.internal_service_cost)
            obj.total_billable_cost = calculate_billable_cost(obj.internal_service_cost, obj.tax_cost)
            obj.total_cost = calculate_total_cost(obj.llm_cost, obj.total_billable_cost)
        # Reduce the transaction billable amount from the organization's balance
        obj.organization.balance -= decimal.Decimal.from_float(obj.total_billable_cost)
        # Update the transaction's organization
        obj.organization.save()
        super().save_model(request, obj, form, change)


@admin.register(AutoBalanceTopUpModel)
class AutoBalanceTopUpModelAdmin(admin.ModelAdmin):
    list_display = ["organization", "on_balance_threshold_trigger", "on_interval_by_days_trigger",
                    "balance_lower_trigger_threshold_value", "addition_on_balance_threshold_trigger"]
    ordering = ["-created_at"]


@admin.register(OrganizationBalanceSnapshot)
class OrganizationBalanceSnapshotAdmin(admin.ModelAdmin):
    list_display = ["organization", "balance", "created_at"]
    ordering = ["-created_at"]
    date_hierarchy = "created_at"
