#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: create_auto_topup_views.py
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
import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import TemplateView

from apps.llm_transaction.models import AutoBalanceTopUpModel
from apps.organization.models import Organization
from web_project import TemplateLayout


logger = logging.getLogger(__name__)


class Transactions_AutoTopUpCreate(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['organizations'] = Organization.objects.filter(users__in=[self.request.user])
        return context

    def post(self, request, *args, **kwargs):
        org_id = request.POST.get('organization_id')
        on_balance_threshold_trigger = request.POST.get('on_balance_threshold_trigger')
        on_interval_by_days_trigger = request.POST.get('on_interval_by_days_trigger')
        if on_balance_threshold_trigger == 'on':
            on_balance_threshold_trigger = True
        else:
            on_balance_threshold_trigger = False
        if on_interval_by_days_trigger == 'on':
            on_interval_by_days_trigger = True
        else:
            on_interval_by_days_trigger = False

        balance_lower_trigger_threshold_value = None
        addition_on_balance_threshold_trigger = None
        if on_balance_threshold_trigger:
            balance_lower_trigger_threshold_value = request.POST.get('balance_lower_trigger_threshold_value')
            addition_on_balance_threshold_trigger = request.POST.get('addition_on_balance_threshold_trigger')

        regular_by_days_interval = None
        addition_on_interval_by_days_trigger = None
        date_of_last_auto_top_up = None
        if on_interval_by_days_trigger:
            regular_by_days_interval = request.POST.get('regular_by_days_interval')
            addition_on_interval_by_days_trigger = request.POST.get('addition_on_interval_by_days_trigger')
            date_of_last_auto_top_up = timezone.now()

        monthly_hard_limit_auto_addition_amount = request.POST.get('monthly_hard_limit_auto_addition_amount')
        org = Organization.objects.get(id=org_id)
        if org.auto_balance_topup:
            org.auto_balance_topup.delete()

        top_up_model = AutoBalanceTopUpModel.objects.create(
            organization=org, on_balance_threshold_trigger=on_balance_threshold_trigger,
            on_interval_by_days_trigger=on_interval_by_days_trigger,
            balance_lower_trigger_threshold_value=balance_lower_trigger_threshold_value,
            addition_on_balance_threshold_trigger=addition_on_balance_threshold_trigger,
            regular_by_days_interval=regular_by_days_interval,
            addition_on_interval_by_days_trigger=addition_on_interval_by_days_trigger,
            date_of_last_auto_top_up=date_of_last_auto_top_up, calendar_month_total_auto_addition_value=0,
            monthly_hard_limit_auto_addition_amount=monthly_hard_limit_auto_addition_amount
        )
        top_up_model.save()
        org.auto_balance_topup = top_up_model
        org.save()
        logger.info(f"Auto Top Up Plan created for organization: {org.id}")
        return redirect('llm_transaction:auto_top_up_list')
