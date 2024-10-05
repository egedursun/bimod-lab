#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: delete_script_views.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:35
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: delete_script_views.py
#  Last Modified: 2024-09-28 00:53:10
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:03:36
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.mm_scripts.models import CustomScript
from apps.user_permissions.models import UserPermission
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class DeleteCustomScriptView(LoginRequiredMixin, TemplateView):
    """
    Handles the deletion of custom scripts.

    This view allows users to delete specific custom scripts, provided they have the necessary permissions.

    Methods:
        get_context_data(self, **kwargs): Prepares the context for the deletion confirmation page.
        post(self, request, *args, **kwargs): Processes the deletion of the specified custom script.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        custom_script_id = self.kwargs.get('pk')
        custom_script = CustomScript.objects.get(id=custom_script_id)
        context['custom_script'] = custom_script
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - DELETE_SCRIPTS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_SCRIPTS):
            messages.error(self.request, "You do not have permission to delete scripts.")
            return redirect('mm_scripts:list')
        ##############################

        custom_script_id = self.kwargs.get('pk')
        # PERMISSION CHECK FOR - DELETE_SCRIPTS
        user_permissions = UserPermission.active_permissions.filter(user=request.user).all().values_list(
            'permission_type', flat=True
        )
        if PermissionNames.DELETE_SCRIPTS not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {"Permission Error": "You do not have permission to delete scripts."}
            return self.render_to_response(context)

        custom_script = CustomScript.objects.get(id=custom_script_id)
        custom_script.delete()
        messages.success(request, "Custom Script deleted successfully.")
        return redirect('mm_scripts:list')
