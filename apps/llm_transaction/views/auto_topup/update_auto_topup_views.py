#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: update_auto_topup_views.py
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

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.shortcuts import (
    get_object_or_404,
    redirect
)

from django.utils import timezone
from django.views.generic import TemplateView

from apps.llm_transaction.models import (
    AutoBalanceTopUpModel
)

from apps.organization.models import Organization
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class Transactions_AutoTopUp_Update(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        user = self.request.user
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        p = get_object_or_404(
            AutoBalanceTopUpModel,
            id=kwargs.get('plan_id')
        )

        context.update(
            {
                'plan': p,
                'organizations': Organization.objects.filter(
                    users__in=[user]
                )
            }
        )

        return context

    def post(self, request, plan_id):

        try:
            p = get_object_or_404(
                AutoBalanceTopUpModel,
                id=plan_id
            )

            p.on_balance_threshold_trigger = request.POST.get('on_balance_threshold_trigger') == 'on' or False
            p.on_interval_by_days_trigger = request.POST.get('on_interval_by_days_trigger') == 'on' or False

            p.balance_lower_trigger_threshold_value = request.POST.get('balance_lower_trigger_threshold_value') or None
            p.addition_on_balance_threshold_trigger = request.POST.get('addition_on_balance_threshold_trigger') or None

            p.regular_by_days_interval = request.POST.get('regular_by_days_interval') or None
            p.addition_on_interval_by_days_trigger = request.POST.get('addition_on_interval_by_days_trigger') or None

            p.monthly_hard_limit_auto_addition_amount = request.POST.get(
                'monthly_hard_limit_auto_addition_amount') or 100_000

            p.date_of_last_auto_top_up = timezone.now()
            p.save()

        except Exception as e:
            logger.error(f"Error updating Auto Top Up: {e}")

            return redirect('llm_transaction:auto_top_up_list')

        logger.info(f"Auto Top Up was updated by User: {self.request.user.id}.")

        return redirect('llm_transaction:auto_top_up_list')
