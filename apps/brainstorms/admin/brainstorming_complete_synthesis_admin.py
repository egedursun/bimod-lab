#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: brainstorming_complete_synthesis_admin.py
#  Last Modified: 2024-10-05 01:39:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:38
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#


from django.contrib import admin

from apps.brainstorms.models import BrainstormingCompleteSynthesis

"""
class BrainstormingCompleteSynthesis(models.Model):
    brainstorming_session = models.ForeignKey('BrainstormingSession', on_delete=models.CASCADE)
    created_by_user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    # No need for having the field 'ideas', since they can be retrieved directly from 'brainstorming_session' object.
    synthesis_content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.brainstorming_session.session_name

    class Meta:
        verbose_name = 'Brainstorming Complete Synthesis'
        verbose_name_plural = 'Brainstorming Complete Syntheses'
        ordering = ['-created_at']
        unique_together = ['brainstorming_session']

        indexes = [
            models.Index(fields=['brainstorming_session']),
            models.Index(fields=['created_by_user']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
            models.Index(fields=['brainstorming_session', 'created_by_user']),
            models.Index(fields=['brainstorming_session', 'created_at']),
            models.Index(fields=['brainstorming_session', 'updated_at']),
        ]
"""


@admin.register(BrainstormingCompleteSynthesis)
class BrainstormingCompleteSynthesisAdmin(admin.ModelAdmin):
    list_display = ('brainstorming_session', 'created_by_user', 'created_at')
    list_filter = ('brainstorming_session', 'created_by_user', 'created_at')
    search_fields = ('brainstorming_session', 'created_by_user', 'created_at')
    ordering = ('-created_at',)
