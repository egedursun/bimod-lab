from django.urls import path

from .views import ListTransactionsView


app_name = "llm_transaction"


urlpatterns = [
    path('list/', ListTransactionsView.as_view(template_name="llm_transaction/list_transactions.html"), name='list'),
]
