#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: delete_all_expert_networks_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:40
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#


from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.leanmod.models import ExpertNetwork
from apps.user_permissions.utils import PermissionNames


class SettingsView_DeleteAllExpertNets(View, LoginRequiredMixin):

    def post(self, request, *args, **kwargs):
        user = request.user
        expert_networks = ExpertNetwork.objects.filter(organization__users__in=[user]).all()
        confirmation_field = request.POST.get('confirmation', None)
        if confirmation_field != 'CONFIRM DELETING ALL EXPERT NETWORKS':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL EXPERT NETWORKS'.")
            return redirect('user_settings:settings')

        ##############################
        # PERMISSION CHECK FOR - DELETE_EXPERT_NETWORKS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_EXPERT_NETWORKS):
            messages.error(self.request, "You do not have permission to delete expert networks.")
            return redirect('user_settings:settings')
        ##############################

        try:
            for network in expert_networks:
                network.delete()
            messages.success(request, "All expert networks associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting expert networks: {e}")
        return redirect('user_settings:settings')
