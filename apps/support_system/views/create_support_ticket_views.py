#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: create_support_ticket_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:41
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import logging

from django.contrib import messages

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.support_system.forms.support_ticket_forms import (
    SupportTicketForm
)

from apps.support_system.models import SupportTicket

from apps.support_system.utils import (
    MAXIMUM_TICKET_FREQUENCY_ONCE_EVERY_HOURS_PER_USER
)

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class SupportView_TicketCreate(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['form'] = SupportTicketForm()
        return context

    def post(self, request, *args, **kwargs):

        max_freq = MAXIMUM_TICKET_FREQUENCY_ONCE_EVERY_HOURS_PER_USER

        ##############################
        # PERMISSION CHECK FOR - CREATE_SUPPORT_TICKETS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.CREATE_SUPPORT_TICKETS
        ):
            messages.error(self.request, "You do not have permission to create support tickets.")
            return redirect('support_system:list')
        ##############################

        # Get the date of the latest support ticket of the user
        latest_ticket_date: SupportTicket = SupportTicket.objects.filter(
            user=self.request.user
        ).latest('created_at')

        # If 12 hours have not passed since the last support ticket, return an error message
        if (latest_ticket_date.created_at + timezone.timedelta(
            hours=max_freq
        )) > timezone.now():
            messages.error(
                self.request,
                f"You have already created a support ticket in the last {max_freq} hours. You can only create one support ticket within {max_freq} hours."
            )

            return redirect('support_system:list')

        form = SupportTicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(
                commit=False
            )

            ticket.user = request.user

            ticket.save()

            logger.info(f"Support ticket was created by User: {self.request.user.id}.")

            return redirect('support_system:list')

        else:
            context = self.get_context_data()
            context['form'] = form

            logger.error(f"Support ticket creation failed for User: {self.request.user.id}.")

            return self.render_to_response(context)
