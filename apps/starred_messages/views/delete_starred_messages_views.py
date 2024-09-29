#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: delete_starred_messages_views.py
#  Last Modified: 2024-09-28 00:53:10
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:08:44
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DeleteView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.starred_messages.models import StarredMessage
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class DeleteStarredMessageView(LoginRequiredMixin, DeleteView):
    """
    Handles the deletion of starred messages.

    This view allows users to delete specific starred messages after confirming the action. Only starred messages that belong to the authenticated user can be deleted.

    Methods:
        get_context_data(self, **kwargs): Prepares the context for the starred message deletion confirmation page.
        get(self, request, *args, **kwargs): Processes the deletion of the specified starred message (GET request redirects to POST).
        post(self, request, *args, **kwargs): Processes the deletion of the specified starred message and updates the associated chat message.
    """

    model = StarredMessage
    success_url = 'starred_messages:list'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        context_user = request.user
        starred_message = get_object_or_404(StarredMessage, id=self.kwargs['pk'])

        ##############################
        # PERMISSION CHECK FOR - REMOVE_STARRED_MESSAGES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.REMOVE_STARRED_MESSAGES):
            messages.error(self.request, "You do not have permission to remove starred messages.")
            return redirect('starred_messages:list')
        ##############################

        starred_message.delete()
        print('[DeleteStarredMessageView.post] Starred message deleted successfully.')
        success_message = "Starred message deleted successfully."
        # assign the relevant message's starred field to False
        starred_message.chat_message.starred = False
        starred_message.chat_message.save()
        messages.success(request, success_message)
        return redirect(self.success_url)
