from django.urls import path

from .views import ListTransactionsView, CreateAutomatedTopUpPlan, ListAutomatedTopUpPlans, \
    ListTransactionInvoicesView, UpdateAutomatedTopUpPlan

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
]
