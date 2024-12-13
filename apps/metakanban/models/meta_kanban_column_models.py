#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: meta_kanban_column_models.py
#  Last Modified: 2024-10-26 21:04:54
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-26 21:04:55
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


class MetaKanbanStatusColumn(models.Model):
    board = models.ForeignKey(
        'MetaKanbanBoard',
        on_delete=models.CASCADE
    )

    column_name = models.CharField(max_length=10000, unique=True)
    position_id = models.IntegerField(default=0)

    created_by_user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.column_name + ' - ' + self.created_at.strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        verbose_name = 'Meta Kanban Status Column'
        verbose_name_plural = 'Meta Kanban Status Columns'
        ordering = ['position_id']

        indexes = [
            models.Index(fields=[
                'created_at'
            ]),
            models.Index(fields=[
                'updated_at'
            ]),
            models.Index(fields=[
                'created_by_user'
            ]),
            models.Index(fields=[
                'column_name'
            ]),
            models.Index(fields=[
                'created_at',
                'updated_at'
            ]),
            models.Index(fields=[
                'created_at',
                'updated_at',
                'created_by_user'
            ]),
            models.Index(fields=[
                'created_at',
                'updated_at',
                'column_name'
            ]),
            models.Index(fields=[
                'created_at',
                'updated_at',
                'column_name',
                'created_by_user'
            ]),
        ]
