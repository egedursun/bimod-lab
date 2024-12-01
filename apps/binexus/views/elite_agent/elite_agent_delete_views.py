#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: elite_agent_delete_views.py
#  Last Modified: 2024-10-22 21:58:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-22 21:58:09
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
from django.views import View

from apps.binexus.models import BinexusEliteAgent
from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.user_permissions.utils import PermissionNames

logger = logging.getLogger(__name__)


class BinexusView_EliteAgentDelete(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - DELETE_BINEXUS_ELITES
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DELETE_BINEXUS_ELITES
        ):
            messages.error(self.request, "You do not have permission to execute Binexus Elite Agents.")
            return redirect('binexus:process_detail', pk=kwargs.get('pk'))
        ##############################

        agent_id = kwargs.get('pk')
        agent = BinexusEliteAgent.objects.get(id=agent_id)
        process_id = agent.binexus_process.id

        try:
            agent.delete()
            logger.info(f"Elite agent deleted successfully.")
            messages.success(request, "Elite agent deleted successfully.")

        except Exception as e:
            logger.error(f"Error deleting elite agent: {e}")
            messages.error(request, f"Error deleting elite agent: {e}")

        return redirect('binexus:process_detail', pk=process_id)
