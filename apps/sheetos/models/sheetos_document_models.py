#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: sheetos_document_models.py
#  Last Modified: 2024-10-31 18:34:36
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-31 18:34:37
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


class SheetosDocument(models.Model):
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE)
    copilot_assistant = models.ForeignKey('assistants.Assistant', on_delete=models.CASCADE, default=1)

    document_folder = models.ForeignKey('sheetos.SheetosFolder', on_delete=models.CASCADE)
    document_title = models.CharField(max_length=4000)
    document_content_json_quill = models.TextField(blank=True, null=True)
    context_instructions = models.TextField(blank=True, null=True)
    target_audience = models.TextField(blank=True, null=True)
    tone = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by_user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='sheetos_document_created_by_user')
    last_updated_by_user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='sheetos_document_last_updated_by_user')

    def __str__(self):
        return self.organization.name + ' - ' + self.document_folder.name + ' - ' + self.document_title

    class Meta:
        verbose_name = 'Sheetos Document'
        verbose_name_plural = 'Sheetos Documents'
        unique_together = [
            ["organization", "document_folder", "document_title"],
        ]
        indexes = [
            models.Index(fields=['organization']),
            models.Index(fields=['organization', 'document_folder']),
            models.Index(fields=['organization', 'copilot_assistant']),
            models.Index(fields=['organization', 'copilot_assistant', 'document_folder']),
            models.Index(fields=['organization', 'document_folder', 'document_title']),
            models.Index(fields=['organization', 'copilot_assistant', 'document_folder', 'document_title']),
        ]


