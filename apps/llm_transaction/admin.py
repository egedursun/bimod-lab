from django.contrib import admin
from django.contrib.admin import widgets

from .models import LLMTransaction
from .utils import calculate_number_of_tokens, calculate_llm_cost, calculate_internal_service_cost, calculate_tax_cost, \
    calculate_total_cost, calculate_billable_cost


@admin.register(LLMTransaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["organization", "model", "number_of_tokens", "llm_cost", "internal_service_cost", "tax_cost", "total_cost", "created_at"]
    list_filter = ["organization", "model", "created_at"]
    search_fields = ["organization__name", "model__nickname"]
    date_hierarchy = "created_at"
    readonly_fields = ["created_at"]
    fieldsets = (
        (None, {
            "fields": (
                "organization",
                "model",
                "encoding_engine",
                "transaction_context_content",
                "number_of_tokens",
                "llm_cost",
                "internal_service_cost",
                "tax_cost",
                "total_cost",
                "total_billable_cost",
            )
        }),
        ("Metadata", {
            "fields": (
                "created_at",
            )
        }),
    )
    ordering = ["-created_at"]

    def save_model(self, request, obj, form, change):
        if obj.transaction_context_content:
            obj.number_of_tokens = calculate_number_of_tokens(obj.encoding_engine, obj.transaction_context_content)
            # calculate the costs
            obj.llm_cost = calculate_llm_cost(obj.model.model_name, obj.number_of_tokens)
            obj.internal_service_cost = calculate_internal_service_cost(obj.llm_cost)
            obj.tax_cost = calculate_tax_cost(obj.internal_service_cost)
            obj.total_billable_cost = calculate_billable_cost(obj.internal_service_cost, obj.tax_cost)
            obj.total_cost = calculate_total_cost(obj.llm_cost, obj.total_billable_cost)
        super().save_model(request, obj, form, change)
