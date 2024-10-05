#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: urls.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:43
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

from django.urls import path

from .views import ListTransactionsView, CreateAutomatedTopUpPlan, ListAutomatedTopUpPlans, \
    ListTransactionInvoicesView, UpdateAutomatedTopUpPlan, CreateManualTopUpPlan, TransferBalanceView

app_name = "llm_transaction"

urlpatterns = [
    path('list/', ListTransactionsView.as_view(
        template_name="llm_transaction/transactions/list_transactions.html"),
         name='list'),
    path('auto_top_up/create/', CreateAutomatedTopUpPlan.as_view(
        template_name="llm_transaction/topup/create_auto_topup.html"),
         name='auto_top_up_create'),
    path('auto_top_up/update/<int:plan_id>/', UpdateAutomatedTopUpPlan.as_view(
        template_name="llm_transaction/topup/update_auto_topup.html"),
         name='auto_top_up_update'
         ),
    path('auto_top_up/list/', ListAutomatedTopUpPlans.as_view(
        template_name="llm_transaction/topup/manage_auto_topup_plans.html"),
         name='auto_top_up_list'),
    path('transaction_invoices/list/', ListTransactionInvoicesView.as_view(
        template_name="llm_transaction/invoices/list_transaction_invoices.html"),
         name='transaction_invoices_list'),
    path('top_up/create/', CreateManualTopUpPlan.as_view(
        template_name="llm_transaction/topup/create_topup.html"),
         name='create_top_up'),
    path('top_up/transfer/', TransferBalanceView.as_view(
        template_name="llm_transaction/topup/transfer_balance.html"),
         name='transfer_balance'),
]
