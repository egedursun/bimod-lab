#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: binexus_process_delete_views.py
#  Last Modified: 2024-10-22 18:38:57
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-22 18:38:58
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
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.binexus.models import BinexusProcess
from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class BinexusView_ProcessDelete(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        process_id = self.kwargs.get('pk')
        binexus_process = BinexusProcess.objects.get(id=process_id)
        context['binexus_process'] = binexus_process
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - DELETE_BINEXUS_PROCESSES
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DELETE_BINEXUS_PROCESSES
        ):
            messages.error(self.request, "You do not have permission to delete Binexus Processes.")
            return redirect('binexus:process_list')
        ##############################

        try:
            process_id = self.kwargs.get('pk')
            binexus_process = BinexusProcess.objects.get(id=process_id)
            binexus_process.delete()

        except Exception as e:
            logger.error(f"[BinexusView_ProcessDelete] Error deleting the Binexus Process: {e}")
            messages.error(self.request, "Error deleting the Binexus Process.")
            return redirect('binexus:process_list')

        logger.info(f'Binexus Process deleted successfully.')
        return redirect('binexus:process_list')
