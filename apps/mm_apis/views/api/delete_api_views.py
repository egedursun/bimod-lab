#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: delete_api_views.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:32
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
#  File: delete_api_views.py
#  Last Modified: 2024-09-28 16:27:57
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:00:11
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
from apps.mm_apis.models import CustomAPI
from apps.user_permissions.models import UserPermission
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class DeleteCustomAPIView(LoginRequiredMixin, TemplateView):
    """
    Handles the deletion of custom APIs.

    This view allows users to delete specific custom APIs, provided they have the necessary permissions.

    Methods:
        get_context_data(self, **kwargs): Prepares the context for the deletion confirmation page.
        post(self, request, *args, **kwargs): Processes the deletion of the specified custom API.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        custom_api_id = self.kwargs.get('pk')
        custom_api = CustomAPI.objects.get(id=custom_api_id)
        context['custom_api'] = custom_api
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - DELETE_APIS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_APIS):
            messages.error(self.request, "You do not have permission to delete custom APIs.")
            return redirect('mm_apis:list')
        ##############################

        custom_api_id = self.kwargs.get('pk')
        # PERMISSION CHECK FOR - DELETE_APIS
        user_permissions = UserPermission.active_permissions.filter(user=request.user).all().values_list(
            'permission_type', flat=True
        )
        if PermissionNames.DELETE_APIS not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {"Permission Error": "You do not have permission to delete APIs."}
            return self.render_to_response(context)

        custom_api = CustomAPI.objects.get(id=custom_api_id)
        custom_api.delete()
        messages.success(request, "Custom API deleted successfully.")
        return redirect('mm_apis:list')
