from django.contrib import admin

from apps.llm_transaction.models import OrganizationBalanceSnapshot


@admin.register(OrganizationBalanceSnapshot)
class OrganizationBalanceSnapshotAdmin(admin.ModelAdmin):
    list_display = ["organization", "balance", "created_at"]
    ordering = ["-created_at"]
    date_hierarchy = "created_at"
