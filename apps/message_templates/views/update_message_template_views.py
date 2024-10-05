#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: update_message_template_views.py
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
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.message_templates.forms import MessageTemplateForm
from apps.message_templates.models import MessageTemplate
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class UpdateMessageTemplateView(TemplateView, LoginRequiredMixin):
    """
    Handles the updating of an existing message template.

    This view allows users to update the content of their existing message templates. It ensures that the user is authorized to make changes before saving them.

    Methods:
        get_context_data(self, **kwargs): Prepares the context with the user's organizations and the message template to be updated.
        post(self, request, *args, **kwargs): Processes the form submission to update the message template.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        organizations = self.request.user.organizations.all()
        message_template = get_object_or_404(MessageTemplate, pk=self.kwargs['pk'])
        context['form'] = MessageTemplateForm(instance=message_template)
        context['message_template'] = message_template
        context['organizations'] = organizations
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - UPDATE_TEMPLATE_MESSAGES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_TEMPLATE_MESSAGES):
            messages.error(self.request, "You do not have permission to update template messages.")
            return redirect('message_templates:list')
        ##############################

        message_template = get_object_or_404(MessageTemplate, pk=self.kwargs['pk'])
        form = MessageTemplateForm(request.POST, instance=message_template)
        if form.is_valid():
            form.save()
            return redirect('message_templates:list')
        return render(request, self.template_name, {'form': form, 'message_template': message_template})
