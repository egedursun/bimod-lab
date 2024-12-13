#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: list_hadron_system_views.py
#  Last Modified: 2024-10-17 22:52:19
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-17 22:52:20
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

from django.contrib import messages

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.hadron_prime.models import HadronSystem
from apps.organization.models import Organization

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class HadronPrimeView_ListHadronSystem(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_HADRON_SYSTEMS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.LIST_HADRON_SYSTEMS
        ):
            messages.error(self.request, "You do not have permission to list Hadron Systems.")
            return context
        ##############################

        try:
            user_orgs = Organization.objects.filter(
                users__in=[self.request.user]
            )

            systems_by_org = {
                org: HadronSystem.objects.filter(
                    organization=org
                ) for org in user_orgs
            }

            context['systems_by_org'] = systems_by_org

        except Exception as e:
            messages.error(self.request, f"Error listing Hadron Systems: {e}")
            logger.error(f"Error listing Hadron Systems: {e}")

            return context

        return context
