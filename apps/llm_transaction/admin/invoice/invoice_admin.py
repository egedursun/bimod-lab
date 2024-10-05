#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: invoice_admin.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:42
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

from django.contrib import admin

from apps.llm_transaction.models import TransactionInvoice


@admin.register(TransactionInvoice)
class TransactionInvoiceAdmin(admin.ModelAdmin):
    list_display = ["organization", "responsible_user", "transaction_type", "amount_added", "payment_method",
                    "transaction_date", "invoice_number", "barcode_image", "transaction_paper"]
    ordering = ["-transaction_date"]
    date_hierarchy = "transaction_date"
    readonly_fields = ["transaction_date"]
