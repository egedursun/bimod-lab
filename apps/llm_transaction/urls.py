from django.urls import path

from .views import ListTransactionsView, CreateAutomatedTopUpPlan, ListAutomatedTopUpPlans

app_name = "llm_transaction"

urlpatterns = [
    path('list/', ListTransactionsView.as_view(
        template_name="llm_transaction/transactions/list_transactions.html"),
         name='list'),

    path('auto_top_up/create/', CreateAutomatedTopUpPlan.as_view(
        template_name="llm_transaction/topup/create_auto_topup.html"),
         name='auto_top_up_create'),
    path('auto_top_up/list/', ListAutomatedTopUpPlans.as_view(
        template_name="llm_transaction/topup/manage_auto_topup_plans.html"),
         name='auto_top_up_list'),
]
