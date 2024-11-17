#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: list_auto_topups_views.py
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
from django.views.generic import TemplateView

from apps.organization.models import Organization
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class Transactions_AutoTopUpList(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['organizations'] = Organization.objects.filter(users__in=[self.request.user])
        return context

    def post(self, request, *args, **kwargs):
        organization_id = request.POST.get('organization_id')
        organization = Organization.objects.get(id=organization_id)

        try:
            if 'delete' in request.POST:
                organization.auto_balance_topup.delete()
                organization.auto_balance_topup = None
                organization.save()
        except Exception as e:
            logger.error(f"Error deleting Auto Top Up: {e}")
            return redirect('llm_transaction:auto_top_up_list')

        logger.info(f"Auto Top Up was deleted by User: {self.request.user.id}.")
        return redirect('llm_transaction:auto_top_up_list')
