#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: delete_all_export_assistants_views.py
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
#   For permission inquiries, please contact: admin@br6.in.
#


from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.export_assistants.models import ExportAssistantAPI
from apps.user_permissions.utils import PermissionNames


class SettingsView_DeleteAllExportAssistants(View, LoginRequiredMixin):
    def post(self, request, *args, **kwargs):
        user = request.user
        user_exp_agents = ExportAssistantAPI.objects.filter(assistant__organization__users__in=[user]).all()
        confirmation_field = request.POST.get('confirmation', None)
        if confirmation_field != 'CONFIRM DELETING ALL EXPORTED ASSISTANTS':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL EXPORTED ASSISTANTS'.")
            return redirect('user_settings:settings')

        ##############################
        # PERMISSION CHECK FOR - DELETE_EXPORT_ASSISTANT
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_EXPORT_ASSISTANT):
            messages.error(self.request, "You do not have permission to delete exported assistants.")
            return redirect('user_settings:settings')
        ##############################

        try:
            for exp_agent in user_exp_agents:
                exp_agent.delete()
            messages.success(request, "All exported assistants associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting exported assistants: {e}")
        return redirect('user_settings:settings')
