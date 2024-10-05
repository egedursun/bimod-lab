#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: support_ticket_response_models.py
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
#  File: support_ticket_response_models.py
#  Last Modified: 2024-09-27 16:47:28
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:09:09
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.db import models

from apps.support_system.models.support_ticket_models import SupportTicket


class SupportTicketResponse(models.Model):
    """
    Model: SupportTicketResponse

    The SupportTicketResponse model represents a response to a support ticket. It contains
    a reference to the corresponding SupportTicket, the user who submitted the response, and
    the response content itself. The model also tracks the timestamp when the response was created.

    Fields:
    - ticket: ForeignKey to the SupportTicket model, representing the ticket this response is associated with.
    - user: ForeignKey to the auth.User model, representing the user who submitted the response.
    - response: TextField for the content of the response.
    - created_at: DateTimeField automatically set to the timestamp when the response was created.

    Meta Options:
    - ordering: Default ordering is by the creation date ('created_at').
    - verbose_name: Singular name of the model in the admin interface.
    - verbose_name_plural: Plural name of the model in the admin interface.
    - indexes: Database indexes to optimize querying based on the ticket, user, and creation date.
    """

    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='responses')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    response = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Support Ticket Response'
        verbose_name_plural = 'Support Ticket Responses'

        indexes = [
            models.Index(fields=['ticket', 'created_at']),
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['ticket', 'user', 'created_at']),
        ]

    def __str__(self):
        return f'{self.ticket.title} - {self.user.username} - {self.created_at.strftime("%Y%m%d%H:%M")}'
