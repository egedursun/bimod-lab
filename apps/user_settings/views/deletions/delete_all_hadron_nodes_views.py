#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_all_hadron_nodes_views.py
#  Last Modified: 2024-10-18 21:54:49
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-18 21:55:36
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
from django.views import View

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.hadron_prime.models import HadronNode
from apps.organization.models import Organization

from apps.user_permissions.utils import (
    PermissionNames
)

logger = logging.getLogger(__name__)


class SettingsView_DeleteAllHadronNodes(View, LoginRequiredMixin):

    def post(self, request, *args, **kwargs):
        user = request.user

        user_orgs = Organization.objects.filter(
            users__in=[user]
        )

        hadron_nodes = HadronNode.objects.filter(
            system__organization__in=user_orgs
        )

        confirmation_field = request.POST.get('confirmation', None)

        if confirmation_field != 'CONFIRM DELETING ALL HADRON NODES':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL HADRON NODES'.")
            logger.error(f"Invalid confirmation field: {confirmation_field}")

            return redirect('user_settings:settings')

        ##############################
        # PERMISSION CHECK FOR - DELETE_HADRON_NODES
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DELETE_HADRON_NODES
        ):
            messages.error(self.request, "You do not have permission to delete hadron nodes.")
            return redirect('user_settings:settings')
        ##############################

        try:
            for hadron_node in hadron_nodes:
                hadron_node.delete()

            logger.info(f"All hadron nodes associated with User: {user.id} have been deleted.")
            messages.success(request, "All hadron nodes associated with your account have been deleted.")

        except Exception as e:
            logger.error(f"Error deleting hadron nodes: {e}")
            messages.error(request, f"Error deleting hadron nodes: {e}")

        return redirect('user_settings:settings')
