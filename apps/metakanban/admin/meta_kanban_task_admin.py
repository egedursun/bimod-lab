#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: meta_kanban_task_models.py
#  Last Modified: 2024-10-26 21:57:16
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-26 21:57:16
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


"""
class MetaKanbanTask(models.Model):
    board = models.ForeignKey('metakanban.MetaKanbanBoard', on_delete=models.CASCADE)
    status_column = models.ForeignKey('metakanban.MetaKanbanStatusColumn', on_delete=models.CASCADE)
    title = models.CharField(max_length=10000)
    description = models.TextField(null=True, blank=True)
    priority = models.CharField(max_length=100, choices=META_KANBAN_TASK_PRIORITIES,
                                default=MetaKanbanTaskPrioritiesNames.UNCATEGORIZED)
    due_date = models.DateTimeField(null=True, blank=True)
    assignee = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True,
                                 related_name='assigned_tasks')

    created_by_user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + ' - ' + self.created_at.strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        verbose_name = 'Meta Kanban Task'
        verbose_name_plural = 'Meta Kanban Tasks'
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

"""

from django.contrib import admin

from apps.metakanban.models.meta_kanban_task_models import MetaKanbanTask
from apps.metakanban.utils import META_KANBAN_TASK_ADMIN_LIST, META_KANBAN_TASK_ADMIN_FILTER, \
    META_KANBAN_TASK_ADMIN_SEARCH


@admin.register(MetaKanbanTask)
class MetaKanbanTaskAdmin(admin.ModelAdmin):
    list_display = META_KANBAN_TASK_ADMIN_LIST
    list_filter = META_KANBAN_TASK_ADMIN_FILTER
    search_fields = META_KANBAN_TASK_ADMIN_SEARCH
    ordering = ['-created_at']
