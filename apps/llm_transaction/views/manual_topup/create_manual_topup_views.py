#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: create_manual_topup_views.py
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

from django.views.generic import TemplateView

from apps.organization.models import Organization
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class Transactions_ManualTopUpCreate(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        try:
            selected_org = Organization.objects.filter(
                users__in=[self.request.user]
            ).first()

            context['selected_organization'] = selected_org

            orgs = Organization.objects.filter(
                users__in=[self.request.user]
            ).all()

            context['organizations'] = orgs

        except Exception as e:
            logger.error(f"Error getting context data for Manual Top Up: {e}")

            return context

        logger.info(f"Manual Top Up was created by User: {self.request.user.id}.")

        return context
