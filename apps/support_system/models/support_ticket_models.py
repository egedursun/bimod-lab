#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: support_ticket_models.py
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

from apps.support_system.utils import STATUSES_FOR_SUPPORT_TICKETS, PRIORITY_CATEGORY_OF_SUPPORT_TICKETS


class SupportTicket(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    issue_description = models.TextField()
    status = models.CharField(max_length=50, choices=STATUSES_FOR_SUPPORT_TICKETS, default='open')
    priority = models.CharField(max_length=50, choices=PRIORITY_CATEGORY_OF_SUPPORT_TICKETS, default='low')
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
