#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
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
#   For permission inquiries, please contact: admin@Bimod.io.
#
#
#
#

from django.urls import path

from .views import Transactions_TransactionList, Transactions_AutoTopUpCreate, Transactions_AutoTopUpList, \
    Transactions_InvoiceList, Transactions_AutoTopUp_Update, Transactions_ManualTopUpCreate, Transactions_BalanceTransfer

app_name = "llm_transaction"

urlpatterns = [
    path('list/', Transactions_TransactionList.as_view(
        template_name="llm_transaction/transactions/list_transactions.html"), name='list'),
    path('auto_top_up/create/', Transactions_AutoTopUpCreate.as_view(
        template_name="llm_transaction/topup/create_auto_topup.html"), name='auto_top_up_create'),
    path('auto_top_up/update/<int:plan_id>/', Transactions_AutoTopUp_Update.as_view(
        template_name="llm_transaction/topup/update_auto_topup.html"), name='auto_top_up_update'),
    path('auto_top_up/list/', Transactions_AutoTopUpList.as_view(
        template_name="llm_transaction/topup/manage_auto_topup_plans.html"), name='auto_top_up_list'),
    path('transaction_invoices/list/', Transactions_InvoiceList.as_view(
        template_name="llm_transaction/invoices/list_transaction_invoices.html"), name='transaction_invoices_list'),
    path('top_up/create/', Transactions_ManualTopUpCreate.as_view(
        template_name="llm_transaction/topup/create_topup.html"), name='create_top_up'),
    path('top_up/transfer/', Transactions_BalanceTransfer.as_view(
        template_name="llm_transaction/topup/transfer_balance.html"), name='transfer_balance'),
]
