#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: meta_kanban_change_log_models.py
#  Last Modified: 2024-10-26 21:49:34
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-26 21:49:35
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

from apps.metakanban.utils import (
    META_KANBAN_CHANGE_LOG_ACTION_TYPES
)


class MetaKanbanChangeLog(models.Model):
    board = models.ForeignKey(
        'MetaKanbanBoard',
        on_delete=models.CASCADE,
        related_name='meta_kanban_change_logs',
        null=True,
        blank=True
    )

    action_type = models.CharField(
        max_length=100,
        choices=META_KANBAN_CHANGE_LOG_ACTION_TYPES,
        default='update_task',
        null=True,
        blank=True
    )

    action_details = models.TextField(blank=True, null=True)

    change_by_user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='meta_kanban_changes_by_user',
        null=True,
        blank=True
    )

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.action_type + ' - ' + self.timestamp.strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        verbose_name = 'Meta Kanban Change Log'
        verbose_name_plural = 'Meta Kanban Change Logs'

        ordering = ['-timestamp']

        indexes = [
            models.Index(fields=[
                'timestamp'
            ]),
            models.Index(fields=[
                'board'
            ]),
            models.Index(fields=[
                'action_type'
            ]),
            models.Index(fields=[
                'change_by_user'
            ]),
            models.Index(fields=[
                'timestamp',
                'board'
            ]),
            models.Index(fields=[
                'timestamp',
                'action_type'
            ]),
            models.Index(fields=[
                'timestamp',
                'change_by_user'
            ]),
            models.Index(fields=[
                'timestamp',
                'board',
                'action_type'
            ]),
            models.Index(fields=[
                'timestamp',
                'board',
                'change_by_user'
            ]),
            models.Index(fields=[
                'timestamp',
                'action_type',
                'change_by_user'
            ]),
            models.Index(fields=[
                'timestamp',
                'board',
                'action_type',
                'change_by_user'
            ]),
        ]
