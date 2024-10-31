#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: ellma_script_models.py
#  Last Modified: 2024-10-30 17:40:54
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-30 17:40:54
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

from apps.ellma.utils import ELLMA_TRANSCRIPTION_LANGUAGES, EllmaTranscriptionLanguagesNames


class EllmaScript(models.Model):
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE,
                                     related_name='ellma_scripts')
    script_name = models.CharField(max_length=255, null=False, blank=False)
    llm_model = models.ForeignKey('llm_core.LLMCore', on_delete=models.CASCADE, related_name='ellma_scripts')

    ellma_script_content = models.TextField(null=True, blank=True)
    ellma_transcription_language = models.CharField(max_length=255, choices=ELLMA_TRANSCRIPTION_LANGUAGES,
                                                    default=EllmaTranscriptionLanguagesNames.PYTHON3)
    ellma_transcribed_file = models.FileField(upload_to='ellma_scripts/%Y/%m/%d/', null=True, blank=True)

    created_by_user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='ellma_scripts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.script_name} - {self.organization.name} - {self.llm_model.nickname} - {self.created_at.strftime("%Y-%m-%d %H:%M:%S")}'

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'eLLMa Script'
        verbose_name_plural = 'eLLMa Scripts'
        indexes = [
            models.Index(fields=['organization', 'llm_model', 'created_by_user']),
            models.Index(fields=['organization', 'llm_model']),
            models.Index(fields=['organization']),
            models.Index(fields=['llm_model']),
            models.Index(fields=['created_by_user']),
            models.Index(fields=['created_at']),
        ]
