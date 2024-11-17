#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_expert_network_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:33
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
from apps.leanmod.models import ExpertNetwork
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class ExpertNetworkView_Delete(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        nw_id = kwargs.get('pk')
        nw = get_object_or_404(ExpertNetwork, id=nw_id)
        context['expert_network'] = nw
        return context

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - DELETE_EXPERT_NETWORKS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_EXPERT_NETWORKS):
            messages.error(self.request, "You do not have permission to delete Expert Network.")
            return redirect('leanmod:list_expert_networks')
        ##############################

        nw_id = kwargs.get('pk')
        nw = get_object_or_404(ExpertNetwork, id=nw_id)

        try:
            nw.delete()
        except Exception as e:
            logger.error(f"An error occurred while deleting Expert Network {nw.name}. Error: {str(e)}")
            messages.error(request, f"An error occurred while deleting Expert Network {nw.name}. Error: {str(e)}")
            return redirect('leanmod:list_expert_networks')

        logger.info(f"Expert Network {nw.name} was deleted by User: {self.request.user.id}.")
        messages.success(request, f'The expert network "{nw.name}" has been deleted successfully.')
        return redirect('leanmod:list_expert_networks')
