#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: create_message_template_views.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:42
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
#  File: create_message_template_views.py
#  Last Modified: 2024-09-28 00:53:10
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:59:13
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
from apps.message_templates.forms import MessageTemplateForm
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class CreateMessageTemplateView(TemplateView, LoginRequiredMixin):
    """
    Handles the creation of new message templates.

    This view allows users to create message templates that they can use in their interactions. The view checks user permissions before allowing the creation of a new template.

    Methods:
        get_context_data(self, **kwargs): Prepares the context with the user's organizations.
        post(self, request, *args, **kwargs): Processes the form submission to create a new message template and associates it with the user.
    """

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
            message_template = form.save(commit=False)
            message_template.user = request.user
            message_template.save()
            messages.success(request, "Message Template created successfully!")
            print('[CreateMessageTemplateView.post] Message Template created successfully.')
            return redirect("message_templates:list")
        else:
            messages.error(request, "Please correct the errors below.")
            return self.render_to_response(self.get_context_data(form=form, error_messages=form.errors))
