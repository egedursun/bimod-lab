#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: video_generator_connection_models.py
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
from apps.core.video_generation.utils import VIDEO_GENERATOR_PROVIDER_TYPES


class VideoGeneratorConnection(models.Model):
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE)
    assistant = models.ForeignKey('assistants.Assistant', on_delete=models.CASCADE)
    created_by_user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    description = models.TextField()
    provider = models.CharField(max_length=255, choices=VIDEO_GENERATOR_PROVIDER_TYPES)
    provider_api_key = models.CharField(max_length=100000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Video Generator Connection'
        verbose_name_plural = 'Video Generator Connections'
        unique_together = [
            ["assistant", "name"],
        ]
        indexes = [
            models.Index(fields=['organization']),
            models.Index(fields=['organization', 'assistant']),
            models.Index(fields=['organization', 'assistant', 'created_by_user']),
        ]

    def __str__(self):
        return self.name + ' - ' + self.provider + ' - ' + self.organization.name
