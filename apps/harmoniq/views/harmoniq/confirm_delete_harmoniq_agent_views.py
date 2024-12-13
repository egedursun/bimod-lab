#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: confirm_delete_harmoniq_agent_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:34
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

from django.shortcuts import (
    get_object_or_404,
    redirect
)

from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.harmoniq.models import Harmoniq

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class HarmoniqView_ConfirmDelete(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        harmoniq_agent = get_object_or_404(
            Harmoniq,
            id=self.kwargs['pk']
        )

        context['assistant'] = harmoniq_agent
        return context

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - DELETE_HARMONIQ_AGENTS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DELETE_HARMONIQ_AGENTS
        ):
            messages.error(self.request, "You do not have permission to delete Harmoniq Agents.")
            return redirect('harmoniq:list')
        ##############################

        harmoniq_agent = get_object_or_404(
            Harmoniq,
            id=self.kwargs['pk']
        )

        try:
            harmoniq_agent.delete()

        except Exception as e:
            logger.error(f"Error deleting Harmoniq agent: {e}")
            messages.error(request, f"Error deleting Harmoniq agent: {e}")

            return redirect('harmoniq:detail', pk=self.kwargs['pk'])

        logger.info(f"The Harmoniq agent was deleted by User: {request.user.id}.")
        messages.success(request, f'The Harmoniq agent "{harmoniq_agent.name}" has been successfully deleted.')

        return redirect('harmoniq:list')
