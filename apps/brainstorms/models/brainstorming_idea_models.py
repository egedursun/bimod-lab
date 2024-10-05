#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: brainstorming_idea_models.py
#  Last Modified: 2024-10-01 14:26:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:37
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: brainstorming_idea_models.py
#  Last Modified: 2024-10-01 00:22:37
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-10-01 00:22:38
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@bimod.io.
#


from django.db import models


class BrainstormingIdea(models.Model):
    brainstorming_session = models.ForeignKey('BrainstormingSession', on_delete=models.CASCADE)
    created_by_user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    idea_title = models.CharField(max_length=1000)
    idea_description = models.TextField()
    depth_level = models.IntegerField(default=1)
    is_bookmarked = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.idea_title + ' - ' + self.brainstorming_session.session_name

    class Meta:
        verbose_name = 'Brainstorming Idea'
        verbose_name_plural = 'Brainstorming Ideas'
        ordering = ['-created_at']
        unique_together = ['brainstorming_session', 'idea_description', 'depth_level']

        indexes = [
            models.Index(fields=['brainstorming_session']),
            models.Index(fields=['created_by_user']),
            models.Index(fields=['idea_title']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
            models.Index(fields=['brainstorming_session', 'idea_title']),
            models.Index(fields=['brainstorming_session', 'created_by_user']),
            models.Index(fields=['brainstorming_session', 'created_at']),
            models.Index(fields=['brainstorming_session', 'updated_at']),
            models.Index(fields=['brainstorming_session', 'idea_title', 'created_by_user']),
            models.Index(fields=['brainstorming_session', 'idea_title', 'created_at']),
            models.Index(fields=['brainstorming_session', 'idea_title', 'updated_at']),
        ]
