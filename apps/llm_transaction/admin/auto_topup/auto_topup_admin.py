from django.contrib import admin

from apps.llm_transaction.models import AutoBalanceTopUpModel


@admin.register(AutoBalanceTopUpModel)
class AutoBalanceTopUpModelAdmin(admin.ModelAdmin):
    list_display = ["organization", "on_balance_threshold_trigger", "on_interval_by_days_trigger",
                    "balance_lower_trigger_threshold_value", "addition_on_balance_threshold_trigger"]
    ordering = ["-created_at"]
