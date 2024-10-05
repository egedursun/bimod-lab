#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: delete_lean_assistant_views.py
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

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.leanmod.models import LeanAssistant
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class DeleteLeanAssistantView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        assistant_id = kwargs.get('pk')
        context['lean_assistant'] = LeanAssistant.objects.get(id=assistant_id)
        return context

    def post(self, request, *args, **kwargs):
        assistant_id = kwargs.get('pk')

        ##############################
        # PERMISSION CHECK FOR - DELETE_LEAN_ASSISTANT
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_LEAN_ASSISTANT):
            messages.error(self.request, "You do not have permission to delete LeanMod assistants.")
            return redirect('leanmod:list')
        ##############################

        try:
            lean_assistant = LeanAssistant.objects.get(id=assistant_id)
            lean_assistant.delete()
            messages.success(request, f"Lean Assistant '{lean_assistant.name}' was deleted successfully.")
        except LeanAssistant.DoesNotExist:
            messages.error(request, "The Lean Assistant does not exist.")
        except Exception as e:
            messages.error(request, f"An error occurred while deleting the Lean Assistant: {e}")
        return redirect('leanmod:list')
