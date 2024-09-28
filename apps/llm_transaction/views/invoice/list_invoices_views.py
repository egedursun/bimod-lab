from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.llm_transaction.models import TransactionInvoice
from apps.organization.models import Organization
from web_project import TemplateLayout


class ListTransactionInvoicesView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        # Get the organizations related to the current user
        organizations = Organization.objects.filter(users__in=[self.request.user]).all()
        context['invoices'] = TransactionInvoice.objects.filter(
            organization__in=organizations
        ).select_related('organization', 'responsible_user').order_by('-transaction_date')
        context['organizations'] = organizations
        return context
