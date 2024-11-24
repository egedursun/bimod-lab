#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: export_voidforger_models.py
#  Last Modified: 2024-10-17 16:15:05
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-24 20:18:04
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
from django.utils import timezone

from apps.export_voidforger.utils import generate_voidforger_custom_api_key, generate_voidforger_endpoint
from config.settings import BASE_URL, EXPORT_VOIDFORGER_API_BASE_URL


class ExportVoidForgerAPI(models.Model):
    organization = models.ForeignKey("organization.Organization", on_delete=models.CASCADE,
                                     related_name='exported_voidforgers', null=True, blank=True)
    voidforger = models.ForeignKey('voidforger.VoidForger', on_delete=models.CASCADE,
                                   related_name='exported_voidforgers')
    is_public = models.BooleanField(default=False)
    request_limit_per_hour = models.IntegerField(default=1000)
    is_online = models.BooleanField(default=True)
    custom_api_key = models.CharField(max_length=1000, blank=True, null=True, unique=True)
    endpoint = models.CharField(max_length=1000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by_user = models.ForeignKey("auth.User", on_delete=models.CASCADE,
                                        related_name='export_voidforgers_created_by_user')

    def __str__(self):
        return str(self.voidforger.id) + " - " + self.created_at.strftime(
            "%Y-%m-%d %H:%M:%S") if self.created_at else ""

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.endpoint:
            self.endpoint = BASE_URL + "/" + EXPORT_VOIDFORGER_API_BASE_URL + "/" + generate_voidforger_endpoint(
                self.voidforger)
        if not self.custom_api_key and (not self.is_public):
            self.custom_api_key = generate_voidforger_custom_api_key(self.voidforger)
        super().save(force_insert, force_update, using, update_fields)

    def requests_in_last_hour(self):
        from apps.export_voidforger.models import VoidForgerRequestLog
        one_hour_ago = timezone.now() - timezone.timedelta(hours=1)
        return VoidForgerRequestLog.objects.filter(export_voidforger=self, timestamp__gte=one_hour_ago).count()

    def requests_limit_reached(self):
        return self.requests_in_last_hour() >= self.request_limit_per_hour

    class Meta:
        verbose_name = "Export VoidForger API"
        verbose_name_plural = "Export VoidForger APIs"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['voidforger']),
            models.Index(fields=['created_by_user']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
            models.Index(fields=['voidforger', 'created_at']),
            models.Index(fields=['voidforger', 'updated_at']),
            models.Index(fields=['voidforger', 'created_by_user']),
        ]
