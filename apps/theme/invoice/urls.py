#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:31
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.urls import path
from .views import InvoiceView, InvoicePrintView
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path(
        "app/invoice/list/",
        login_required(InvoiceView.as_view(template_name="app_invoice_list.html")),
        name="app-invoice-list",
    ),
    path(
        "app/invoice/preview/",
        login_required(InvoiceView.as_view(template_name="app_invoice_preview.html")),
        name="app-invoice-preview",
    ),
    path(
        "app/invoice/edit/",
        login_required(InvoiceView.as_view(template_name="app_invoice_edit.html")),
        name="app-invoice-edit",
    ),
    path(
        "app/invoice/add/",
        login_required(InvoiceView.as_view(template_name="app_invoice_add.html")),
        name="app-invoice-add",
    ),
    path(
        "app/invoice/print/",
        login_required(InvoicePrintView.as_view(template_name="app_invoice_print.html")),
        name="app-invoice-print",
    ),
]
