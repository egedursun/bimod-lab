#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: create_auto_topup_views.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:39
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: create_auto_topup_views.py
#  Last Modified: 2024-09-28 15:44:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:57:33
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import TemplateView

from apps.llm_transaction.models import AutoBalanceTopUpModel
from apps.organization.models import Organization
from web_project import TemplateLayout


class CreateAutomatedTopUpPlan(LoginRequiredMixin, TemplateView):
    """
    Handles the creation of an automated balance top-up plan for an organization.

    This view allows users to set up triggers and parameters for automatic balance top-ups, ensuring that organizations maintain a minimum balance.

    Methods:
        get_context_data(self, **kwargs): Prepares the context with the organizations associated with the current user.
        post(self, request, *args, **kwargs): Processes the form submission to create a new automated top-up plan, including setting the triggers and limits.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['organizations'] = Organization.objects.filter(users__in=[self.request.user])
        return context

    def post(self, request, *args, **kwargs):
        organization_id = request.POST.get('organization_id')

        # trigger parameters
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
            organization=organization, on_balance_threshold_trigger=on_balance_threshold_trigger,
            on_interval_by_days_trigger=on_interval_by_days_trigger,
            balance_lower_trigger_threshold_value=balance_lower_trigger_threshold_value,
            addition_on_balance_threshold_trigger=addition_on_balance_threshold_trigger,
            regular_by_days_interval=regular_by_days_interval,
            addition_on_interval_by_days_trigger=addition_on_interval_by_days_trigger,
            date_of_last_auto_top_up=date_of_last_auto_top_up, calendar_month_total_auto_addition_value=0,
            monthly_hard_limit_auto_addition_amount=monthly_hard_limit_auto_addition_amount
        )
        top_up_model.save()
        organization.auto_balance_topup = top_up_model
        organization.save()
        return redirect('llm_transaction:auto_top_up_list')
