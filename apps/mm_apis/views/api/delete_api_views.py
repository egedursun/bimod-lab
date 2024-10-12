#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: delete_api_views.py
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.mm_apis.models import CustomAPI
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class CustomAPIView_Delete(LoginRequiredMixin, TemplateView):

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
        custom_api = CustomAPI.objects.get(id=custom_api_id)
        custom_api.delete()
        messages.success(request, "Custom API deleted successfully.")
        return redirect('mm_apis:list')
