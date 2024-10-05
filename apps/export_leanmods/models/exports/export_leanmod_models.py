#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: export_leanmod_models.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:39
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
#  File: export_leanmod_models.py
#  Last Modified: 2024-09-27 22:58:55
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:51:20
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.db import models
from django.utils import timezone

from apps.export_leanmods.utils import generate_leanmod_assistant_endpoint, generate_leanmod_assistant_custom_api_key
from config.settings import BASE_URL, EXPORT_LEANMOD_API_BASE_URL


class ExportLeanmodAssistantAPI(models.Model):
    organization = models.ForeignKey("organization.Organization", on_delete=models.CASCADE,
                                     related_name='exported_leanmods', null=True, blank=True)
    lean_assistant = models.ForeignKey('leanmod.LeanAssistant', on_delete=models.CASCADE,
                                       related_name='exported_leanmods')
    is_public = models.BooleanField(default=False)
    request_limit_per_hour = models.IntegerField(default=1000)
    is_online = models.BooleanField(default=True)

    custom_api_key = models.CharField(max_length=1000, blank=True, null=True, unique=True)
    endpoint = models.CharField(max_length=1000, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by_user = models.ForeignKey("auth.User", on_delete=models.CASCADE,
                                        related_name='export_lean_assistants_created_by_user')

    def __str__(self):
        return self.lean_assistant.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.endpoint:
            self.endpoint = BASE_URL + "/" + EXPORT_LEANMOD_API_BASE_URL + "/" + generate_leanmod_assistant_endpoint(
                self.lean_assistant)
        # generate the API key for non-public usage of the exported assistant
        if not self.custom_api_key and (not self.is_public):
            self.custom_api_key = generate_leanmod_assistant_custom_api_key(self.lean_assistant)
        super().save(force_insert, force_update, using, update_fields)

    def requests_in_last_hour(self):
        from apps.export_leanmods.models import LeanmodRequestLog

        one_hour_ago = timezone.now() - timezone.timedelta(hours=1)
        return LeanmodRequestLog.objects.filter(export_lean_assistant=self, timestamp__gte=one_hour_ago).count()

    def requests_limit_reached(self):
        return self.requests_in_last_hour() >= self.request_limit_per_hour

    class Meta:
        verbose_name = "Export LeanMod Assistant API"
        verbose_name_plural = "Export LeanMod Assistant APIs"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['lean_assistant']),
            models.Index(fields=['created_by_user']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
            models.Index(fields=['lean_assistant', 'created_at']),
            models.Index(fields=['lean_assistant', 'updated_at']),
            models.Index(fields=['lean_assistant', 'created_by_user']),
        ]
