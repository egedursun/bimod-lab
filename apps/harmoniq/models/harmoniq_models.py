#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: harmoniq_models.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:34
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
from apps.harmoniq.utils.constant_utils import HARMONIQ_DEITIES


class Harmoniq(models.Model):
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE)
    llm_model = models.ForeignKey('llm_core.LLMCore', on_delete=models.CASCADE)
    created_by_user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    consultant_expert_networks = models.ManyToManyField("leanmod.ExpertNetwork", related_name='harmoniqs',
                                                        blank=True)
    name = models.CharField(max_length=1000)
    description = models.TextField()
    harmoniq_deity = models.CharField(max_length=100, choices=HARMONIQ_DEITIES, default=HARMONIQ_DEITIES[0][0])
    optional_instructions = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + ' - ' + self.organization.name + ' - ' + self.llm_model.nickname

    class Meta:
        verbose_name = 'Harmoniq Agent'
        verbose_name_plural = 'Harmoniq Agents'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['organization']),
            models.Index(fields=['organization', 'llm_model']),
            models.Index(fields=['organization', 'llm_model', 'created_by_user']),
        ]
