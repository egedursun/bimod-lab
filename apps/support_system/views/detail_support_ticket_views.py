#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: detail_support_ticket_views.py
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.support_system.models import SupportTicket, SupportTicketResponse
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class SupportView_TicketDetail(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_SUPPORT_TICKETS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_SUPPORT_TICKETS):
            messages.error(self.request, "You do not have permission to view support tickets.")
            return context
        ##############################

        ticket = get_object_or_404(SupportTicket, pk=self.kwargs['pk'], user=self.request.user)
        context['ticket'] = ticket
        context['responses'] = ticket.responses.all().order_by('created_at')
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - UPDATE_SUPPORT_TICKETS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_SUPPORT_TICKETS):
            messages.error(self.request, "You do not have permission to update/modify support tickets.")
            return redirect('support_system:list')
        ##############################

        ticket = get_object_or_404(SupportTicket, pk=self.kwargs['pk'], user=request.user)
        output = request.POST.get('response')
        if output:
            SupportTicketResponse.objects.create(ticket=ticket, user=request.user, response=output)
        return redirect('support_system:detail', pk=ticket.pk)
