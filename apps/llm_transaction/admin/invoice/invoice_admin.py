from django.contrib import admin

from apps.llm_transaction.models import TransactionInvoice


@admin.register(TransactionInvoice)
class TransactionInvoiceAdmin(admin.ModelAdmin):
    list_display = ["organization", "responsible_user", "transaction_type", "amount_added", "payment_method",
                    "transaction_date", "invoice_number", "barcode_image", "transaction_paper"]
    ordering = ["-transaction_date"]
    date_hierarchy = "transaction_date"
    readonly_fields = ["transaction_date"]
