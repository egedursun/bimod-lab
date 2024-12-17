#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_script_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:38
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
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.mm_scripts.models import (
    CustomScript
)

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class CustomScriptView_Delete(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        custom_script_id = self.kwargs.get('pk')

        custom_script = CustomScript.objects.get(
            id=custom_script_id
        )

        context['custom_script'] = custom_script

        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - DELETE_SCRIPTS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DELETE_SCRIPTS
        ):
            messages.error(self.request, "You do not have permission to delete scripts.")

            return redirect('mm_scripts:list')
        ##############################

        custom_script_id = self.kwargs.get('pk')

        custom_script = CustomScript.objects.get(
            id=custom_script_id
        )

        try:
            custom_script.delete()

        except Exception as e:
            messages.error(request, "An error occurred while deleting the custom script: " + str(e))

            return redirect("mm_scripts:list")

        logger.info(f"Custom Script was deleted by User: {self.request.user.id}.")
        messages.success(request, "Custom Script deleted successfully.")

        return redirect('mm_scripts:list')
