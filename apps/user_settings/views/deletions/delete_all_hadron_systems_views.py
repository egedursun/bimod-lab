#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_all_hadron_systems_views.py
#  Last Modified: 2024-10-18 21:54:27
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-18 21:54:29
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

from apps.hadron_prime.models import HadronSystem
from apps.organization.models import Organization

from apps.user_permissions.utils import (
    PermissionNames
)

logger = logging.getLogger(__name__)


class SettingsView_DeleteAllHadronSystems(View, LoginRequiredMixin):

    def post(self, request, *args, **kwargs):
        user = request.user

        user_orgs = Organization.objects.filter(
            users__in=[user]
        )

        hadron_systems = HadronSystem.objects.filter(
            organization__in=user_orgs
        )

        confirmation_field = request.POST.get('confirmation', None)

        if confirmation_field != 'CONFIRM DELETING ALL HADRON SYSTEMS':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL HADRON SYSTEMS'.")
            logger.error(f"Invalid confirmation field: {confirmation_field}")

            return redirect('user_settings:settings')

        ##############################
        # PERMISSION CHECK FOR - DELETE_HADRON_SYSTEMS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DELETE_HADRON_SYSTEMS
        ):
            messages.error(self.request, "You do not have permission to delete hadron systems.")
            return redirect('user_settings:settings')
        ##############################

        try:
            for hadron_system in hadron_systems:
                hadron_system.delete()

            logger.info(f"All hadron systems associated with User: {user.id} have been deleted.")
            messages.success(request, "All hadron systems associated with your account have been deleted.")

        except Exception as e:
            logger.error(f"Error deleting hadron systems: {e}")
            messages.error(request, f"Error deleting hadron systems: {e}")

        return redirect('user_settings:settings')
