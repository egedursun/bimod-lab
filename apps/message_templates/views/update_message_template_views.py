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

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.message_templates.forms import MessageTemplateForm
from apps.message_templates.models import MessageTemplate
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class MessageTemplateView_Update(TemplateView, LoginRequiredMixin):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        orgs = self.request.user.organizations.all()
        msg_tmpl = get_object_or_404(MessageTemplate, pk=self.kwargs['pk'])
        context['form'] = MessageTemplateForm(instance=msg_tmpl)
        context['message_template'] = msg_tmpl
        context['organizations'] = orgs
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - UPDATE_TEMPLATE_MESSAGES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_TEMPLATE_MESSAGES):
            messages.error(self.request, "You do not have permission to update template messages.")
            return redirect('message_templates:list')
        ##############################

        msg_tmpl = get_object_or_404(MessageTemplate, pk=self.kwargs['pk'])
        form = MessageTemplateForm(request.POST, instance=msg_tmpl)
        if form.is_valid():
            form.save()
            return redirect('message_templates:list')
        return render(request, self.template_name, {'form': form, 'message_template': msg_tmpl})
