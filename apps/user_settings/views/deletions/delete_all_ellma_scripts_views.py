#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_all_ellma_scripts_views.py
#  Last Modified: 2024-10-30 22:59:38
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-30 22:59:38
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

from apps.ellma.models import EllmaScript

from apps.user_permissions.utils import (
    PermissionNames
)

logger = logging.getLogger(__name__)


class SettingsView_DeleteAllEllmaScripts(View, LoginRequiredMixin):
    def post(self, request, *args, **kwargs):
        user = request.user

        user_ellma_scripts = EllmaScript.objects.filter(
            organization__users__in=[user]
        )

        confirmation_field = request.POST.get('confirmation', None)

        if confirmation_field != 'CONFIRM DELETING ALL ELLMA SCRIPTS':
            logger.error(f"Invalid confirmation field: {confirmation_field}")
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL ELLMA SCRIPTS'.")

            return redirect('user_settings:settings')

        ##############################
        # PERMISSION CHECK FOR - DELETE_ELLMA_SCRIPTS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DELETE_ELLMA_SCRIPTS
        ):
            messages.error(self.request, "You do not have permission to delete eLLMa scripts.")

            return redirect('user_settings:settings')
        ##############################

        try:
            for ellma_script in user_ellma_scripts:
                ellma_script.delete()

            logger.info(f"All eLLMa scripts associated with User: {user.id} have been deleted.")
            messages.success(request, "All eLLMa scripts associated with your account have been deleted.")

        except Exception as e:
            logger.error(f"Error deleting eLLMa scripts: {e}")
            messages.error(request, f"Error deleting eLLMa scripts: {e}")

        return redirect('user_settings:settings')
