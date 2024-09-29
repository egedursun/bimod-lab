#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: support_ticket_models.py
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

from apps.support_system.utils import TICKET_STATUSES, PRIORITY_CHOICES


class SupportTicket(models.Model):
    """
    Model: SupportTicket

    The SupportTicket model represents a support ticket submitted by a user. It contains
    information about the user who submitted the ticket, the title, a detailed description
    of the issue, the status of the ticket, and the priority level. The model also includes
    fields for file attachments, creation date, and last updated date.

    Fields:
    - user: ForeignKey to the auth.User model representing the user who submitted the ticket.
    - title: CharField for the title of the support ticket.
    - issue_description: TextField for a detailed description of the issue.
    - status: CharField representing the current status of the ticket (e.g., open, in progress, closed, resolved).
    - priority: CharField indicating the priority level of the ticket (e.g., low, medium, high, critical).
    - attachment: FileField for optional file attachments related to the ticket.
    - created_at: DateTimeField automatically set to the timestamp when the ticket was created.
    - updated_at: DateTimeField automatically updated to the current timestamp whenever the ticket is modified.

    Meta Options:
    - ordering: Default ordering is by the creation date ('created_at').
    - verbose_name: Singular name of the model in the admin interface.
    - verbose_name_plural: Plural name of the model in the admin interface.
    - indexes: Database indexes to optimize querying based on status, priority, and timestamps.
    """

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    issue_description = models.TextField()
    status = models.CharField(max_length=50, choices=TICKET_STATUSES, default='open')
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default='low')

    attachment = models.FileField(upload_to='tickets/attachments/%Y/%m/%d/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} - {self.status} - {self.priority} - {self.created_at.strftime("%Y%m%d%H:%M")}'

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Support Ticket'
        verbose_name_plural = 'Support Tickets'

        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['status', 'updated_at']),
            models.Index(fields=['status', 'priority']),
            models.Index(fields=['status', 'priority', 'created_at']),
            models.Index(fields=['status', 'priority', 'updated_at']),
        ]
