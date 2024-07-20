from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import TemplateView

from apps.llm_transaction.models import LLMTransaction, AutoBalanceTopUpModel
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


DEFAULT_PAGINATION_SIZE_LIST_TRANSACTIONS = 5
MAXIMUM_TOTAL_PAGES = 50


class ListTransactionsView(TemplateView, LoginRequiredMixin):

    def post(self, request, *args, **kwargs):
        filter_value = request.POST.get('filter')
        delta_specifier = request.POST.get('delta_specifier', "30")
        time_specifier = request.POST.get('time_specifier', 'days')
        context = self.get_context_data(filter_value=filter_value, **kwargs)
        context['filter'] = filter_value
        context['filter_types'] = FILTER_TYPES
        context['delta_specifier'] = delta_specifier
        context['time_specifier'] = time_specifier
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        organizations = Organization.objects.filter(users__in=[context_user])

        filter_value = self.request.POST.get('filter', 'specific')
        delta_specifier = self.request.POST.get('delta_specifier', "30")
        time_specifier = self.request.POST.get('time_specifier', 'days')
        filter_date = self.get_filter_date(filter_value, delta_specifier, time_specifier)

        data = []
        for organization in organizations:
            llm_models = organization.llm_cores.all()
            org_data = {
                'organization': organization,
                'llm_models': [],
                'cost_sums': sum_costs(LLMTransaction.objects.defer("transaction_context_content")
                                       .filter(organization=organization, created_at__gte=filter_date))
            }
            for llm_model in llm_models:
                transactions = LLMTransaction.objects.filter(
                    organization=organization,
                    model=llm_model,
                    created_at__gte=filter_date)[:(DEFAULT_PAGINATION_SIZE_LIST_TRANSACTIONS * MAXIMUM_TOTAL_PAGES)]

                # Paginate transactions (5 items per page)
                paginator = Paginator(transactions, DEFAULT_PAGINATION_SIZE_LIST_TRANSACTIONS)
                page_number = self.request.GET.get('page')
                page_obj = paginator.get_page(page_number)

                llm_data = {
                    'model': llm_model,
                    'transactions': page_obj,  # Use paginated transactions
                    'cost_sums': sum_costs(transactions)
                }
                org_data['llm_models'].append(llm_data)
            data.append(org_data)

        context['data'] = data
        context['user'] = context_user
        context["cost_sums"] = sum_costs(LLMTransaction.objects.filter(organization__in=organizations,
                                                                       created_at__gte=filter_date))
        context['filter_types'] = FILTER_TYPES
        context['filter'] = filter_value
        context['delta_specifier'] = delta_specifier
        context['time_specifier'] = time_specifier
        return context

    def get_filter_date(self, filter_value, delta_specifier, time_specifier):
        now = timezone.now()
        if filter_value == 'all':
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


class CreateAutomatedTopUpPlan(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['organizations'] = Organization.objects.filter(users__in=[self.request.user])
        return context

    def post(self, request, *args, **kwargs):
        organization_id = request.POST.get('organization_id')

        # trigger parameters
        on_balance_threshold_trigger = request.POST.get('on_balance_threshold_trigger')
        on_interval_by_days_trigger = request.POST.get('on_interval_by_days_trigger')

        if on_balance_threshold_trigger == 'on': on_balance_threshold_trigger = True
        else: on_balance_threshold_trigger = False

        if on_interval_by_days_trigger == 'on': on_interval_by_days_trigger = True
        else: on_interval_by_days_trigger = False

        # on balance threshold parameters
        balance_lower_trigger_threshold_value = None
        addition_on_balance_threshold_trigger = None
        if on_balance_threshold_trigger:
            balance_lower_trigger_threshold_value = request.POST.get('balance_lower_trigger_threshold_value')
            addition_on_balance_threshold_trigger = request.POST.get('addition_on_balance_threshold_trigger')

        # on interval by days parameters
        regular_by_days_interval = None
        addition_on_interval_by_days_trigger = None
        date_of_last_auto_top_up = None
        if on_interval_by_days_trigger:
            regular_by_days_interval = request.POST.get('regular_by_days_interval')
            addition_on_interval_by_days_trigger = request.POST.get('addition_on_interval_by_days_trigger')
            date_of_last_auto_top_up = timezone.now()


        # common parameters
        monthly_hard_limit_auto_addition_amount = request.POST.get('monthly_hard_limit_auto_addition_amount')

        organization = Organization.objects.get(id=organization_id)
        if organization.auto_balance_topup:
            organization.auto_balance_topup.delete()

        top_up_model = AutoBalanceTopUpModel.objects.create(
            organization=organization,
            on_balance_threshold_trigger=on_balance_threshold_trigger,
            on_interval_by_days_trigger=on_interval_by_days_trigger,
            balance_lower_trigger_threshold_value=balance_lower_trigger_threshold_value,
            addition_on_balance_threshold_trigger=addition_on_balance_threshold_trigger,
            regular_by_days_interval=regular_by_days_interval,
            addition_on_interval_by_days_trigger=addition_on_interval_by_days_trigger,
            date_of_last_auto_top_up=date_of_last_auto_top_up,
            calendar_month_total_auto_addition_value=0,
            monthly_hard_limit_auto_addition_amount=monthly_hard_limit_auto_addition_amount
        )
        top_up_model.save()
        organization.auto_balance_topup = top_up_model
        organization.save()
        return redirect('llm_transaction:auto_top_up_list')


class ListAutomatedTopUpPlans(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['organizations'] = Organization.objects.filter(users__in=[self.request.user])
        return context

    def post(self, request, *args, **kwargs):
        organization_id = request.POST.get('organization_id')
        organization = Organization.objects.get(id=organization_id)
        if 'delete' in request.POST:
            organization.auto_balance_topup.delete()
            organization.auto_balance_topup = None
            organization.save()
        return redirect('llm_transaction:auto_top_up_list')

