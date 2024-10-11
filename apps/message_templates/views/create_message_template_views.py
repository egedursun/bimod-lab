#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: create_message_template_views.py
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
#
#
#

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.message_templates.forms import MessageTemplateForm
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class MessageTemplateView_Create(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['organizations'] = self.request.user.organizations.all()
        return context

    def post(self, request, *args, **kwargs):
        form = MessageTemplateForm(request.POST)

        ##############################
        # PERMISSION CHECK FOR - ADD_TEMPLATE_MESSAGES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_TEMPLATE_MESSAGES):
            messages.error(self.request, "You do not have permission to add template messages.")
            return redirect('message_templates:list')
        ##############################

        if form.is_valid():
            msg_tmpl = form.save(commit=False)
            msg_tmpl.user = request.user
            msg_tmpl.save()
            messages.success(request, "Message Template created successfully!")
            return redirect("message_templates:list")
        else:
            messages.error(request, "Please correct the errors below.")
            return self.render_to_response(self.get_context_data(form=form, error_messages=form.errors))
