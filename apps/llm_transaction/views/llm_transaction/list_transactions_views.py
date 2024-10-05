#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: list_transactions_views.py
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

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.utils import timezone
from django.views.generic import TemplateView
from datetime import timedelta

from apps.llm_transaction.models import LLMTransaction
from apps.llm_transaction.utils import FILTER_TYPES, sum_costs, DEFAULT_PAGINATION_SIZE_LIST_TRANSACTIONS, \
    MAXIMUM_TOTAL_PAGES
from apps.organization.models import Organization
from web_project import TemplateLayout


class ListTransactionsView(TemplateView, LoginRequiredMixin):
    """
    Displays a filtered list of LLM transactions for the user's organizations.

    This view allows users to filter transactions by a specific time range, with pagination support to manage large datasets.

    Methods:
        get_context_data(self, **kwargs): Retrieves the filtered transactions for the user's organizations and adds them to the context.
        get_filter_date(self, filter_value, delta_specifier, time_specifier): Calculates the filter date based on the user's selected filter options.
        post(self, request, *args, **kwargs): Processes the form submission to filter transactions and update the context accordingly.
    """

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
                'organization': organization, 'llm_models': [],
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
                    'model': llm_model, 'transactions': page_obj,
                    'cost_sums': sum_costs(LLMTransaction.objects.filter(
                        organization=organization, model=llm_model, created_at__gte=filter_date)
                    )
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
        context['user_organizations'] = organizations
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
