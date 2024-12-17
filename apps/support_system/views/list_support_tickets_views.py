#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: list_support_tickets_views.py
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

from django.core.paginator import Paginator
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.support_system.models import (
    SupportTicket
)

from apps.support_system.utils import (
    TICKET_STATUS_PRIORITY_MAP
)

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class SupportView_TicketList(LoginRequiredMixin, TemplateView):
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_SUPPORT_TICKETS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.LIST_SUPPORT_TICKETS
        ):
            messages.error(self.request, "You do not have permission to view support tickets.")

            return context
        ##############################

        queryset = SupportTicket.objects.filter(
            user=self.request.user
        )

        status_priority = TICKET_STATUS_PRIORITY_MAP

        sorted_queryset = sorted(
            queryset,
            key=lambda ticket: (
                status_priority.get(
                    ticket.status,
                    99
                ),
                ticket.updated_at,
                ticket.created_at,
                ticket.priority
            ),
            reverse=True
        )

        paginator = Paginator(
            sorted_queryset,
            self.paginate_by
        )

        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        logger.info(f"Support ticket list was viewed by User: {self.request.user.id}.")

        return context
