#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: delete_message_template_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:44
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
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import DeleteView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.message_templates.models import MessageTemplate
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class MessageTemplateView_Delete(DeleteView, LoginRequiredMixin):
    model = MessageTemplate
    success_url = 'message_templates:list'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - REMOVE_TEMPLATE_MESSAGES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.REMOVE_TEMPLATE_MESSAGES):
            messages.error(self.request, "You do not have permission to delete template messages.")
            return redirect('message_templates:list')
        ##############################

        msg_tmpl = get_object_or_404(MessageTemplate, id=self.kwargs['pk'])
        msg_tmpl.delete()
        success_message = "Message template deleted successfully."
        messages.success(request, success_message)
        return redirect(self.success_url)
