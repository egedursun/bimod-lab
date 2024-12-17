#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
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

from django.urls import path

from .views import (
    SupportView_TicketCreate,
    SupportView_TicketList,
    SupportView_TicketDetail
)

app_name = 'support_system'

urlpatterns = [
    path(
        'create/',
        SupportView_TicketCreate.as_view(
            template_name='support_system/create_support_ticket.html'
        ),
        name='create'
    ),

    path(
        'list/',
        SupportView_TicketList.as_view(
            template_name='support_system/list_support_tickets.html'
        ),
        name='list'
    ),

    path(
        'list/<int:pk>/',
        SupportView_TicketDetail.as_view(
            template_name='support_system/support_ticket_detail.html'
        ),
        name='detail'
    ),
]
