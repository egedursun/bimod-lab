#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: support_ticket_response_models.py
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

from django.db import models

from apps.support_system.models.support_ticket_models import SupportTicket


class SupportTicketResponse(models.Model):
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
