from django.urls import path
from django.contrib.auth.decorators import login_required
from apps.theme.transactions.transaction_list.views import TransactionListView
from apps.theme.transactions.transaction_add.views import TransactionAddView
from apps.theme.transactions.transaction_update.views import TransactionUpdateView
from apps.theme.transactions.transaction_delete.views import TransactionDeleteView

urlpatterns = [
    path(
        "llm_transaction/list/",
        login_required(TransactionListView.as_view(template_name="transactions_list.html")),
        name="llm_transaction",
    ),
    path(
        "llm_transaction/add/",
        login_required(TransactionAddView.as_view(template_name="transactions_add.html")),
        name="llm_transaction-add",
    ),
    path (
        "llm_transaction/update/<int:pk>",
        login_required(TransactionUpdateView.as_view(template_name="transactions_update.html")),
        name="llm_transaction-update",
    ),
    path (
        "llm_transaction/delete/<int:pk>/",
        login_required(TransactionDeleteView.as_view()),
        name="llm_transaction-delete",
    ),

]
