#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: finetuning_models.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:35
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
#  File: finetuning_models.py
#  Last Modified: 2024-09-27 18:25:50
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:53:37
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.db import models

from apps.finetuning.utils import FINE_TUNING_MODEL_PROVIDERS, FineTuningModelProvidersNames, MODEL_TYPES


# Create your models here.

class FineTunedModelConnection(models.Model):
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE, blank=True, null=True)
    created_by_user = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True)

    provider = models.CharField(max_length=255, choices=FINE_TUNING_MODEL_PROVIDERS,
                                default=FineTuningModelProvidersNames.OPENAI)
    provider_api_key = models.CharField(max_length=5000, blank=True, null=True)
    model_name = models.CharField(max_length=255)

    nickname = models.CharField(max_length=255)
    model_type = models.CharField(max_length=255, choices=MODEL_TYPES)
    model_description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.nickname + ' - ' + self.model_name

    class Meta:
        verbose_name = 'Fine-Tuned Model Connection'
        verbose_name_plural = 'Fine-Tuned Model Connections'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['organization']),
            models.Index(fields=['nickname']),
            models.Index(fields=['model_name']),
            models.Index(fields=['created_at']),
            models.Index(fields=['organization', 'nickname']),
            models.Index(fields=['organization', 'model_name']),
            models.Index(fields=['organization', 'created_at']),
            models.Index(fields=['nickname', 'model_name']),
            models.Index(fields=['nickname', 'created_at']),
            models.Index(fields=['model_name', 'created_at']),
            models.Index(fields=['organization', 'nickname', 'model_name']),
            models.Index(fields=['organization', 'nickname', 'created_at']),
            models.Index(fields=['organization', 'model_name', 'created_at']),
            models.Index(fields=['nickname', 'model_name', 'created_at']),
            models.Index(fields=['organization', 'nickname', 'model_name', 'created_at']),
        ]
