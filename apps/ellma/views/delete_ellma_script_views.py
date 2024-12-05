#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_ellma_script_views.py
#  Last Modified: 2024-10-30 17:38:52
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-30 17:38:52
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.ellma.models import EllmaScript
from apps.user_permissions.utils import PermissionNames


class EllmaScriptView_DeleteScript(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        script_id = kwargs.get('pk')

        ##############################
        # PERMISSION CHECK FOR - DELETE_ELLMA_SCRIPTS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DELETE_ELLMA_SCRIPTS
        ):
            messages.error(self.request, "You do not have permission to delete eLLMa scripts.")
            return redirect('ellma:manage-scripts')
        ##############################

        try:
            ellma_script = EllmaScript.objects.get(id=script_id)

            ellma_script.delete()

            messages.success(request, "Script deleted successfully.")

        except EllmaScript.DoesNotExist:

            messages.error(request, "Script not found.")

        return redirect('ellma:manage-scripts')
