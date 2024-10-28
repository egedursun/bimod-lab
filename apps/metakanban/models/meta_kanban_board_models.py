#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: meta_kanban_board_models.py
#  Last Modified: 2024-10-26 21:02:20
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-26 21:02:21
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
import secrets

from django.db import models

from apps.metakanban.utils import META_KANBAN_BOARD_API_KEY_DEFAULT_LENGTH


class MetaKanbanBoard(models.Model):
    project = models.ForeignKey('projects.ProjectItem', on_delete=models.CASCADE)
    llm_model = models.ForeignKey('llm_core.LLMCore', on_delete=models.CASCADE)
    title = models.CharField(max_length=10000)
    description = models.TextField()
    connection_api_key = models.CharField(max_length=1000,
                                          default=secrets.token_urlsafe(META_KANBAN_BOARD_API_KEY_DEFAULT_LENGTH))

    created_by_user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + ' - ' + self.created_at.strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        verbose_name = 'Meta Kanban Board'
        verbose_name_plural = 'Meta Kanban Boards'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
            models.Index(fields=['project']),
            models.Index(fields=['llm_model']),
            models.Index(fields=['created_by_user']),
            models.Index(fields=['title']),
            models.Index(fields=['created_at', 'updated_at']),
            models.Index(fields=['created_at', 'updated_at', 'project']),
            models.Index(fields=['created_at', 'updated_at', 'llm_model']),
            models.Index(fields=['created_at', 'updated_at', 'created_by_user']),
            models.Index(fields=['created_at', 'updated_at', 'title']),
            models.Index(fields=['created_at', 'updated_at', 'project', 'llm_model']),
            models.Index(fields=['created_at', 'updated_at', 'project', 'created_by_user']),
            models.Index(fields=['created_at', 'updated_at', 'project', 'title']),
            models.Index(fields=['created_at', 'updated_at', 'llm_model', 'created_by_user']),
            models.Index(fields=['created_at', 'updated_at', 'llm_model', 'title']),
            models.Index(fields=['created_at', 'updated_at', 'created_by_user', 'title']),
            models.Index(fields=['created_at', 'updated_at', 'project', 'llm_model', 'created_by_user']),
            models.Index(fields=['created_at', 'updated_at', 'project', 'llm_model', 'title']),
            models.Index(fields=['created_at', 'updated_at', 'project', 'created_by_user', 'title']),
            models.Index(fields=['created_at', 'updated_at', 'llm_model', 'created_by_user', 'title']),
        ]
