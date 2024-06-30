from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import TemplateView

from apps.llm_transaction.models import LLMTransaction
from apps.llm_transaction.utils import sum_costs
from apps.organization.models import Organization
from web_project import TemplateLayout


FILTER_TYPES = [
    ('seconds', 'seconds'),
    ('minutes', 'minutes'),
    ('hours', 'hours'),
    ('days', 'days'),
    ('weeks', 'weeks'),
    ('months', 'months'),
    ('years', 'years'),
]


class ListTransactionsView(TemplateView, LoginRequiredMixin):

    def post(self, request, *args, **kwargs):
        filter_value = request.POST.get('filter')
        delta_specifier = request.POST.get('delta_specifier')
        time_specifier = request.POST.get('time_specifier')
        context = self.get_context_data(filter_value=filter_value, **kwargs)
        context['filter'] = filter_value
        context['filter_types'] = FILTER_TYPES
        context['delta_specifier'] = delta_specifier
        context['time_specifier'] = time_specifier
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = self.request.user
        organizations = Organization.objects.filter(user=user)
        # get from context
        filter_value = self.request.POST.get('filter')
        delta_specifier = self.request.POST.get('delta_specifier')
        if not delta_specifier:
            delta_specifier = "30"
        time_specifier = self.request.POST.get('time_specifier')
        if not time_specifier:
            time_specifier = 'days'
        filter_date = self.get_filter_date(filter_value, delta_specifier, time_specifier)

        data = []
        for organization in organizations:
            llm_models = organization.llmcore_set.all()
            org_data = {
                'organization': organization,
                'llm_models': [],
                'cost_sums': sum_costs(LLMTransaction.objects.filter(organization=organization, created_at__gte=filter_date))
            }
            for llm_model in llm_models:
                transactions = LLMTransaction.objects.filter(organization=organization, model=llm_model, created_at__gte=filter_date)
                llm_data = {
                    'model': llm_model,
                    'transactions': transactions,
                    'cost_sums': sum_costs(transactions)
                }
                org_data['llm_models'].append(llm_data)
            data.append(org_data)

        context['data'] = data
        context['user'] = user
        context["cost_sums"] = sum_costs(LLMTransaction.objects.filter(organization__in=organizations, created_at__gte=filter_date))
        context['filter_types'] = FILTER_TYPES
        context['filter'] = filter_value
        context['delta_specifier'] = delta_specifier
        context['time_specifier'] = time_specifier
        return context

    def get_filter_date(self, filter_value, delta_specifier, time_specifier):
        now = timezone.now()
        if filter_value == 'all' or not delta_specifier or not time_specifier:
            return now - timedelta(hours=100_000)
        else:
            delta = int(delta_specifier.lower().strip())
            time_specifier = time_specifier.lower().strip()
            if time_specifier == 'seconds':
                return now - timedelta(seconds=delta)
            elif time_specifier == 'minutes':
                return now - timedelta(minutes=delta)
            elif time_specifier == 'hours':
                return now - timedelta(hours=delta)
            elif time_specifier == 'days':
                return now - timedelta(days=delta)
            elif time_specifier == 'weeks':
                return now - timedelta(weeks=delta)
            elif time_specifier == 'months':
                return now - timedelta(days=30 * delta)
            elif time_specifier == 'years':
                return now - timedelta(days=365 * delta)
            else:
                raise ValueError('Invalid time specifier: {}'.format(time_specifier))

