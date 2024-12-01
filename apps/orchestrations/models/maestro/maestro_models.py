#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: maestro_models.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:41
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

from apps.orchestrations.utils import ORCHESTRATION_RESPONSE_LANGUAGES


class Maestro(models.Model):
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE, related_name='maestros')
    llm_model = models.ForeignKey('llm_core.LLMCore', on_delete=models.CASCADE, related_name='maestros')
    name = models.CharField(max_length=255)
    description = models.TextField(default="", blank=True)
    instructions = models.TextField(default="", blank=True)
    workflow_step_guide = models.TextField(default="", blank=True)
    maximum_assistant_limits = models.IntegerField(default=10)
    response_template = models.TextField(default="", blank=True)
    audience = models.CharField(max_length=1000)
    tone = models.CharField(max_length=1000)
    response_language = models.CharField(max_length=10, choices=ORCHESTRATION_RESPONSE_LANGUAGES, default="auto")
    maestro_image_save_path = 'maestro_images/%Y/%m/%d/'
    maestro_image = models.ImageField(upload_to=maestro_image_save_path, blank=True, max_length=5000, null=True)
    created_by_user = models.ForeignKey("auth.User", on_delete=models.CASCADE,
                                        related_name='maestros_created_by_user')
    last_updated_by_user = models.ForeignKey("auth.User", on_delete=models.CASCADE,
                                             related_name='maestros_last_updated_by_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    workers = models.ManyToManyField('assistants.Assistant', related_name='maestros', blank=True)

    def __str__(self):
        return self.name + " - " + self.organization.name + " - " + self.llm_model.nickname

    class Meta:
        verbose_name = "Maestro"
        verbose_name_plural = "Maestros"
        unique_together = [
            ["organization", "name"],
        ]
        indexes = [
            models.Index(fields=["organization"]),
            models.Index(fields=["llm_model"]),
            models.Index(fields=["name"]),
            models.Index(fields=["response_language"]),
            models.Index(fields=["created_by_user"]),
            models.Index(fields=["last_updated_by_user"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),
            models.Index(fields=["organization", "llm_model"]),
            models.Index(fields=["organization", "name"]),
            models.Index(fields=["organization", "created_by_user"]),
            models.Index(fields=["organization", "last_updated_by_user"]),
            models.Index(fields=["organization", "created_at"]),
            models.Index(fields=["organization", "updated_at"]),
            models.Index(fields=["llm_model", "name"]),
            models.Index(fields=["llm_model", "created_by_user"]),
            models.Index(fields=["llm_model", "last_updated_by_user"]),
            models.Index(fields=["llm_model", "created_at"]),
            models.Index(fields=["llm_model", "updated_at"]),
            models.Index(fields=["created_by_user", "created_at"]),
            models.Index(fields=["created_by_user", "updated_at"]),
            models.Index(fields=["last_updated_by_user", "created_at"]),
            models.Index(fields=["last_updated_by_user", "updated_at"]),
            models.Index(fields=["organization", "llm_model", "name"]),
            models.Index(fields=["organization", "llm_model", "created_by_user"]),
            models.Index(fields=["organization", "llm_model", "last_updated_by_user"]),
            models.Index(fields=["organization", "llm_model", "created_at"]),
            models.Index(fields=["organization", "llm_model", "updated_at"]),
            models.Index(fields=["organization", "name", "created_at"]),
            models.Index(fields=["organization", "name", "updated_at"]),
            models.Index(fields=["organization", "created_by_user", "created_at"]),
            models.Index(fields=["organization", "created_by_user", "updated_at"]),
            models.Index(fields=["organization", "last_updated_by_user", "created_at"]),
            models.Index(fields=["organization", "last_updated_by_user", "updated_at"]),
            models.Index(fields=["llm_model", "name", "created_at"]),
            models.Index(fields=["llm_model", "name", "updated_at"]),
            models.Index(fields=["llm_model", "created_by_user", "created_at"]),
            models.Index(fields=["llm_model", "created_by_user", "updated_at"]),
            models.Index(fields=["llm_model", "last_updated_by_user", "created_at"]),
            models.Index(fields=["llm_model", "last_updated_by_user", "updated_at"]),
            models.Index(fields=["created_by_user", "created_at", "updated_at"]),
            models.Index(fields=["last_updated_by_user", "created_at", "updated_at"]),
            models.Index(fields=["organization", "llm_model", "name", "created_at"]),
            models.Index(fields=["organization", "llm_model", "name", "updated_at"]),
            models.Index(fields=["organization", "llm_model", "created_by_user", "created_at"]),
            models.Index(fields=["organization", "llm_model", "created_by_user", "updated_at"]),
            models.Index(fields=["organization", "llm_model", "last_updated_by_user", "created_at"]),
            models.Index(fields=["organization", "llm_model", "last_updated_by_user", "updated_at"]),
            models.Index(fields=["organization", "name", "created_at", "updated_at"]),
            models.Index(fields=["organization", "created_by_user", "created_at", "updated_at"]),
            models.Index(fields=["organization", "last_updated_by_user", "created_at", "updated_at"]),
            models.Index(fields=["llm_model", "name", "created_at", "updated_at"]),
            models.Index(fields=["llm_model", "created_by_user", "created_at", "updated_at"]),
            models.Index(fields=["llm_model", "last_updated_by_user", "created_at", "updated_at"]),
        ]
