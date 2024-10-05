#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: harmoniq_admin.py
#  Last Modified: 2024-10-02 20:03:45
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:32
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
#  File: harmoniq_admin.py
#  Last Modified: 2024-10-02 20:02:54
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-10-02 20:03:04
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@bimod.io.
#


from django.contrib import admin

from apps.harmoniq.models import Harmoniq

"""
class Harmoniq(models.Model):
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE)
    llm_model = models.ForeignKey('llm_core.LLMCore', on_delete=models.CASCADE)
    created_by_user = models.ForeignKey('user.User', on_delete=models.CASCADE)

    name = models.CharField(max_length=1000)
    description = models.TextField()
    optional_instructions = models.TextField()
    mode = models.CharField(max_length=100, choices=HARMONIQ_INPUT_MODES, default=HarmoniqInputModesTypes.AUDIO)

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
            models.Index(fields=['organization', 'llm_model', 'created_by_user', 'mode']),
        ]

"""


@admin.register(Harmoniq)
class HarmoniqAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization', 'llm_model', 'created_by_user', 'mode', 'created_at']
    list_filter = ['organization', 'llm_model', 'created_by_user', 'mode', 'created_at']
    search_fields = ['name', 'organization__name', 'llm_model__nickname', 'created_by_user__username', 'mode']
    ordering = ['-created_at']
