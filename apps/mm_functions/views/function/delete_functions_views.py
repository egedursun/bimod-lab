#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_functions_views.py
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
#   For permission inquiries, please contact: admin@Bimod.io.
#
import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.mm_functions.models import CustomFunction
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class CustomFunctionView_Delete(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        custom_function_id = self.kwargs.get('pk')
        custom_function = CustomFunction.objects.get(id=custom_function_id)
        context['custom_function'] = custom_function
        return context

    def post(self, request, *args, **kwargs):
        custom_function_id = self.kwargs.get('pk')

        ##############################
        # PERMISSION CHECK FOR - DELETE_FUNCTIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_FUNCTIONS):
            messages.error(self.request, "You do not have permission to delete custom functions.")
            return redirect('mm_functions:list')
        ##############################

        custom_function = CustomFunction.objects.get(id=custom_function_id)

        try:
            custom_function.delete()
        except Exception as e:
            messages.error(request, "An error occurred while deleting the custom function: " + str(e))
            return redirect("mm_functions:list")

        logger.info(f"Custom Function was deleted by User: {self.request.user.id}.")
        messages.success(request, "Custom Function deleted successfully.")
        return redirect('mm_functions:list')
