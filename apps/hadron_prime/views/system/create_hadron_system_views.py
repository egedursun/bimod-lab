#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: create_hadron_system_views.py
#  Last Modified: 2024-10-17 22:52:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-17 22:52:07
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

from django.shortcuts import redirect
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


class HadronPrimeView_CreateHadronSystem(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        user_orgs = Organization.objects.filter(
            users__in=[self.request.user]
        )

        context['organizations'] = user_orgs

        return context

    def post(self, request, *args, **kwargs):
        organization_id = request.POST.get('organization')

        ##############################
        # PERMISSION CHECK FOR - CREATE_HADRON_SYSTEMS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.CREATE_HADRON_SYSTEMS
        ):
            messages.error(self.request, "You do not have permission to create Hadron Systems.")
            return redirect('hadron_prime:list_hadron_system')
        ##############################

        system_name = request.POST.get('system_name')
        system_description = request.POST.get('system_description')

        if not organization_id or not system_name:
            logger.error('The required fields are not filled out.')
            messages.error(request, 'Please fill out all required fields.')

            return redirect('create_hadron_system')

        try:
            organization = Organization.objects.get(
                id=organization_id
            )

            hadron_system = HadronSystem.objects.create(
                organization=organization,
                system_name=system_name,
                system_description=system_description,
                created_by_user=request.user
            )

        except Exception as e:
            logger.error(f"Error creating Hadron System: {e}")
            messages.error(request, f"Error creating Hadron System: {e}")

            return redirect('create_hadron_system')

        logger.info(f'Hadron System "{hadron_system.system_name}" created.')
        messages.success(request, f'Hadron System "{hadron_system.system_name}" created successfully.')

        return redirect('hadron_prime:list_hadron_system')
