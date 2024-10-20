#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_hadron_system_views.py
#  Last Modified: 2024-10-17 22:52:25
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-17 22:52:25
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
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class HadronPrimeView_DeleteHadronSystem(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        system_id = kwargs.get('pk')
        hadron_system = get_object_or_404(HadronSystem, id=system_id)
        context['hadron_system'] = hadron_system
        return context

    def post(self, request, *args, **kwargs):
        system_id = kwargs.get('pk')

        ##############################
        # PERMISSION CHECK FOR - DELETE_HADRON_SYSTEMS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_HADRON_SYSTEMS):
            messages.error(self.request, "You do not have permission to delete Hadron Systems.")
            return redirect('hadron_prime:list_hadron_system')
        ##############################

        hadron_system = get_object_or_404(HadronSystem, id=system_id)
        hadron_system.delete()
        logger.info(f'Hadron System "{hadron_system.system_name}" has been deleted successfully.')
        messages.success(request, f'Hadron System "{hadron_system.system_name}" has been deleted successfully.')
        return redirect('hadron_prime:list_hadron_system')
