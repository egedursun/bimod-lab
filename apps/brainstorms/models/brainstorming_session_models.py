#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: brainstorming_session_models.py
#  Last Modified: 2024-10-05 01:39:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:39
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


class BrainstormingSession(models.Model):
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE)
    llm_model = models.ForeignKey('llm_core.LLMCore', on_delete=models.CASCADE)
    created_by_user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    session_name = models.CharField(max_length=1000)
    topic_definition = models.TextField()
    constraints = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.session_name + ' - ' + self.organization.name + ' - ' + self.llm_model.nickname

    class Meta:
        verbose_name = 'Brainstorming Session'
        verbose_name_plural = 'Brainstorming Sessions'
        ordering = ['-created_at']
        unique_together = ['organization', 'llm_model', 'session_name']
        indexes = [
            models.Index(fields=['organization']),
            models.Index(fields=['llm_model']),
            models.Index(fields=['created_by_user']),
            models.Index(fields=['session_name']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
            models.Index(fields=['organization', 'llm_model']),
            models.Index(fields=['organization', 'session_name']),
            models.Index(fields=['llm_model', 'session_name']),
            models.Index(fields=['organization', 'llm_model', 'created_by_user']),
            models.Index(fields=['organization', 'llm_model', 'created_at']),
            models.Index(fields=['organization', 'llm_model', 'updated_at']),
            models.Index(fields=['organization', 'llm_model', 'session_name']),
            models.Index(fields=['organization', 'llm_model', 'created_by_user', 'session_name']),
            models.Index(fields=['organization', 'llm_model', 'created_by_user', 'created_at']),
            models.Index(fields=['organization', 'llm_model', 'created_by_user', 'updated_at']),
        ]


