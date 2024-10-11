#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: brainstorming_level_synthesis_models.py
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
#   For permission inquiries, please contact: admin@br6.in.
#


from django.db import models


class BrainstormingLevelSynthesis(models.Model):
    brainstorming_session = models.ForeignKey('BrainstormingSession', on_delete=models.CASCADE)
    created_by_user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    depth_level = models.IntegerField()
    ideas = models.ManyToManyField('BrainstormingIdea')
    synthesis_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.brainstorming_session.session_name + ' - ' + str(self.depth_level)

    class Meta:
        verbose_name = 'Brainstorming Level Synthesis'
        verbose_name_plural = 'Brainstorming Level Syntheses'
        ordering = ['-created_at']
        unique_together = ['brainstorming_session', 'depth_level']
        indexes = [
            models.Index(fields=['brainstorming_session']),
            models.Index(fields=['created_by_user']),
            models.Index(fields=['depth_level']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
            models.Index(fields=['brainstorming_session', 'depth_level']),
            models.Index(fields=['brainstorming_session', 'created_by_user']),
            models.Index(fields=['brainstorming_session', 'created_at']),
            models.Index(fields=['brainstorming_session', 'updated_at']),
            models.Index(fields=['brainstorming_session', 'depth_level', 'created_by_user']),
            models.Index(fields=['brainstorming_session', 'depth_level', 'created_at']),
            models.Index(fields=['brainstorming_session', 'depth_level', 'updated_at']),
        ]
