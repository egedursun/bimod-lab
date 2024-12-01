#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: meta_kanban_board_task_models.py
#  Last Modified: 2024-10-26 21:02:16
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-26 21:02:16
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

from apps.metakanban.utils import META_KANBAN_TASK_PRIORITIES, MetaKanbanTaskPrioritiesNames


class MetaKanbanTask(models.Model):
    board = models.ForeignKey('metakanban.MetaKanbanBoard', on_delete=models.CASCADE)
    status_column = models.ForeignKey('metakanban.MetaKanbanStatusColumn', on_delete=models.CASCADE)
    title = models.CharField(max_length=10000)
    labels = models.ManyToManyField('metakanban.MetaKanbanTaskLabel', related_name='metakanban_tasks', blank=True)
    description = models.TextField(null=True, blank=True)
    priority = models.CharField(max_length=100, choices=META_KANBAN_TASK_PRIORITIES,
                                default=MetaKanbanTaskPrioritiesNames.UNCATEGORIZED, null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    assignees = models.ManyToManyField('auth.User', related_name='metakanban_tasks', blank=True)

    task_image = models.ImageField(upload_to='metakanban/task_images/%Y/%m/%d/', null=True, blank=True)
    task_url = models.URLField(null=True, blank=True)
    task_file = models.FileField(upload_to='metakanban/task_files/%Y/%m/%d/', null=True, blank=True)

    created_by_user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + ' - ' + self.created_at.strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        verbose_name = 'Meta Kanban Task'
        verbose_name_plural = 'Meta Kanban Tasks'
        unique_together = [
            ["board", "title"],
        ]
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
            models.Index(fields=['board']),
            models.Index(fields=['status_column']),
            models.Index(fields=['created_by_user']),
            models.Index(fields=['title']),
            models.Index(fields=['created_at', 'updated_at']),
            models.Index(fields=['created_at', 'updated_at', 'board']),
            models.Index(fields=['created_at', 'updated_at', 'status_column']),
            models.Index(fields=['created_at', 'updated_at', 'created_by_user']),
            models.Index(fields=['created_at', 'updated_at', 'title']),
            models.Index(fields=['created_at', 'updated_at', 'board', 'status_column']),
            models.Index(fields=['created_at', 'updated_at', 'board', 'created_by_user']),
            models.Index(fields=['created_at', 'updated_at', 'board', 'title']),
            models.Index(fields=['created_at', 'updated_at', 'status_column', 'created_by_user']),
            models.Index(fields=['created_at', 'updated_at', 'status_column', 'title']),
            models.Index(fields=['created_at', 'updated_at', 'created_by_user', 'title']),
            models.Index(fields=['created_at', 'updated_at', 'board', 'status_column', 'created_by_user']),
            models.Index(fields=['created_at', 'updated_at', 'board', 'status_column', 'title']),
            models.Index(fields=['created_at', 'updated_at', 'board', 'created_by_user', 'title']),
            models.Index(fields=['created_at', 'updated_at', 'status_column', 'created_by_user', 'title']),
        ]
