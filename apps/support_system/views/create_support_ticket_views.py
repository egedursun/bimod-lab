#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: create_support_ticket_views.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:39
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
#  File: create_support_ticket_views.py
#  Last Modified: 2024-09-28 00:53:10
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:09:26
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
from apps.support_system.forms.support_ticket_forms import SupportTicketForm
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class CreateSupportTicketView(LoginRequiredMixin, TemplateView):
    """
    View to handle the creation of new support tickets.

    This view renders a form for creating a new support ticket. Upon submission, if the form is valid,
    the support ticket is saved and the user is redirected to the ticket list page. If the form is invalid,
    the form is re-rendered with validation errors.

    Methods:
    - get_context_data: Adds the support ticket form to the context.
    - post: Handles the form submission and saves the ticket if valid.
    """

    template_name = 'support_system/create_support_ticket.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['form'] = SupportTicketForm()
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - CREATE_SUPPORT_TICKETS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.CREATE_SUPPORT_TICKETS):
            messages.error(self.request, "You do not have permission to create support tickets.")
            return redirect('support_system:list')
        ##############################

        form = SupportTicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            # Optionally, you can add a success message here
            return redirect('support_system:list')
        else:
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)
