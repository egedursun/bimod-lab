#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: update_hadron_system_views.py
#  Last Modified: 2024-10-17 22:52:14
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-17 22:52:14
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
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.hadron_prime.models import HadronSystem
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class HadronPrimeView_UpdateHadronSystem(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        system_id = kwargs.get('pk')
        hadron_system = get_object_or_404(HadronSystem, id=system_id)
        user_orgs = Organization.objects.filter(users__in=[self.request.user])

        context['hadron_system'] = hadron_system
        context['organizations'] = user_orgs
        return context

    def post(self, request, *args, **kwargs):
        system_id = kwargs.get('pk')

        ##############################
        # PERMISSION CHECK FOR - UPDATE_HADRON_SYSTEMS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_HADRON_SYSTEMS):
            messages.error(self.request, "You do not have permission to update Hadron Systems.")
            return redirect('hadron_prime:list_hadron_system')
        ##############################

        hadron_system = get_object_or_404(HadronSystem, id=system_id)
        organization_id = request.POST.get('organization')
        system_name = request.POST.get('system_name')
        system_description = request.POST.get('system_description')
        if not organization_id or not system_name:
            logger.error('The required fields are not filled out.')
            messages.error(request, 'Please fill out all required fields.')
            return redirect('hadron_prime:update_hadron_system', pk=system_id)

        organization = Organization.objects.get(id=organization_id)
        hadron_system.organization = organization
        hadron_system.system_name = system_name
        hadron_system.system_description = system_description
        hadron_system.save()

        logger.info(f'Hadron System "{hadron_system.system_name}" updated.')
        messages.success(request, f'Hadron System "{hadron_system.system_name}" updated successfully.')
        return redirect('hadron_prime:list_hadron_system')
