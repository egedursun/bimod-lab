#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: meta_kanban_meeting_transcription_models.py
#  Last Modified: 2024-10-28 03:39:52
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-28 03:39:53
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


class MetaKanbanMeetingTranscription(models.Model):
    board = models.ForeignKey(
        'MetaKanbanBoard',
        on_delete=models.CASCADE
    )

    meeting_transcription_text = models.TextField()

    is_processed_with_ai = models.BooleanField(default=False)

    meeting_transcription_key_takeaways = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.board} - {self.created_at}'

    class Meta:
        verbose_name = 'Meta Kanban Meeting Transcription'
        verbose_name_plural = 'Meta Kanban Meeting Transcriptions'

        ordering = ['-created_at']

        indexes = [
            models.Index(fields=[
                'board',
                'is_processed_with_ai'
            ]),
            models.Index(fields=[
                'board',
                'is_processed_with_ai',
                'created_at'
            ]),
            models.Index(fields=[
                'board',
                'created_at'
            ]),
            models.Index(fields=[
                'is_processed_with_ai'
            ]),
            models.Index(fields=[
                'is_processed_with_ai',
                'created_at'
            ]),
            models.Index(fields=[
                'created_at'
            ]),
        ]
