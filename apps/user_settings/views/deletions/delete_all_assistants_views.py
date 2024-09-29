#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: delete_all_assistants_views.py
#  Last Modified: 2024-09-28 00:53:10
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:11:57
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
from django.views import View

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.user_permissions.utils import PermissionNames


class DeleteAllAssistantsView(View, LoginRequiredMixin):
    """
    Handles the deletion of all assistants associated with the user account.
    """

    def post(self, request, *args, **kwargs):
        user = request.user
        user_assistants = Assistant.objects.filter(organization__users__in=[user]).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL ASSISTANTS':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL ASSISTANTS'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - DELETE_ASSISTANTS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_ASSISTANTS):
            messages.error(self.request, "You do not have permission to delete assistants.")
            return redirect('user_settings:settings')
        ##############################

        # [3] Delete ALL items in the queryset
        try:
            for assistant in user_assistants:
                assistant.delete()
            messages.success(request, "All assistants associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting assistants: {e}")

        # [4] Redirect back to settings page
        return redirect('user_settings:settings')
