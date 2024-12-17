#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: generated_video_models.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:45
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


class GeneratedVideo(models.Model):
    organization = models.ForeignKey(
        'organization.Organization',
        on_delete=models.CASCADE,
        related_name='generated_videos'
    )

    assistant = models.ForeignKey(
        'assistants.Assistant',
        on_delete=models.CASCADE,
        related_name='generated_videos'
    )

    multimodal_chat = models.ForeignKey(
        'multimodal_chat.MultimodalChat',
        on_delete=models.CASCADE,
        related_name='generated_videos'
    )

    created_by_user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='generated_videos'
    )

    video_url = models.URLField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Generated Video'
        verbose_name_plural = 'Generated Videos'

        unique_together = [
            [
                "organization",
                "assistant",
                "multimodal_chat",
                "video_url"
            ],
        ]

        indexes = [
            models.Index(fields=[
                'organization'
            ]),
            models.Index(fields=[
                'organization',
                'assistant'
            ]),
            models.Index(fields=[
                'organization',
                'assistant',
                'created_by_user'
            ]),
        ]

    def __str__(self):
        return self.video_url + ' - ' + self.organization.name + ' - ' + self.assistant.name
