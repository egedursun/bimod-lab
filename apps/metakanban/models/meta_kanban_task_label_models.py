#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: meta_kanban_label_models.py
#  Last Modified: 2024-10-27 00:26:30
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-27 00:26:30
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

from apps.metakanban.utils import META_KANBAN_TASK_LABEL_COLOR_CHOICES, MetaKanbanTaskLabelColorChoiceNames


class MetaKanbanTaskLabel(models.Model):
    board = models.ForeignKey('MetaKanbanBoard', on_delete=models.CASCADE)
    label_name = models.CharField(max_length=10000)
    label_color = models.CharField(max_length=100, choices=META_KANBAN_TASK_LABEL_COLOR_CHOICES,
                                   default=MetaKanbanTaskLabelColorChoiceNames.NAVY)

    created_by_user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.label_name + ' - ' + self.created_at.strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        verbose_name = 'Meta Kanban Task Label'
        verbose_name_plural = 'Meta Kanban Task Labels'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
            models.Index(fields=['created_by_user']),
            models.Index(fields=['label_name']),
            models.Index(fields=['created_at', 'updated_at']),
            models.Index(fields=['created_at', 'updated_at', 'created_by_user']),
            models.Index(fields=['created_at', 'updated_at', 'label_name']),
            models.Index(fields=['created_at', 'updated_at', 'label_name', 'created_by_user']),
        ]
