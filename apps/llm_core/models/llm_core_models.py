#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: llm_core_models.py
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

from apps.llm_core.utils import (
    LARGE_LANGUAGE_MODEL_PROVIDERS,
    GPT_MODEL_NAMES,
    GPTModelNamesNames
)


class LLMCore(models.Model):
    nickname = models.CharField(max_length=255)
    description = models.TextField(default="", blank=True)

    provider = models.CharField(
        max_length=2,
        choices=LARGE_LANGUAGE_MODEL_PROVIDERS
    )

    api_key = models.CharField(max_length=8192)

    model_name = models.CharField(
        max_length=1000,
        default=GPTModelNamesNames.O3_MINI,
        null=False,
        blank=False
    )

    temperature = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.50
    )

    maximum_tokens = models.IntegerField(default=4094)
    stop_sequences = models.TextField(default="", blank=True)

    top_p = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=1.0
    )

    frequency_penalty = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.0
    )

    presence_penalty = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.0
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by_user = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="llm_core_created_by_users"
    )

    last_updated_by_user = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="llm_core_last_updated_by_users"
    )

    organization = models.ForeignKey(
        "organization.Organization",
        on_delete=models.CASCADE,
        related_name="llm_cores", null=True
    )

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = "LLM Core"
        verbose_name_plural = "LLM Cores"

        ordering = ["-created_at"]

        unique_together = [
            [
                "organization",
                "nickname"
            ],
        ]

        indexes = [
            models.Index(fields=[
                "nickname"
            ]),
            models.Index(fields=[
                "provider"
            ]),
            models.Index(fields=[
                "model_name"
            ]),
            models.Index(fields=[
                "created_at"
            ]),
            models.Index(fields=[
                "updated_at"
            ]),
            models.Index(fields=[
                "organization"
            ]),
            models.Index(fields=[
                "created_by_user"
            ]),
            models.Index(fields=[
                "last_updated_by_user"
            ]),
            models.Index(fields=[
                "organization",
                "nickname"
            ]),
            models.Index(fields=[
                "organization",
                "provider"
            ]),
            models.Index(fields=[
                "organization",
                "model_name"
            ]),
            models.Index(fields=[
                "organization",
                "created_at"
            ]),
            models.Index(fields=[
                "organization",
                "updated_at"
            ]),
            models.Index(fields=[
                "organization",
                "created_by_user"
            ]),
            models.Index(fields=[
                "organization",
                "last_updated_by_user"
            ]),
        ]

    def get_provider_name(self):
        return dict(LARGE_LANGUAGE_MODEL_PROVIDERS)[self.provider]

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None
    ):

        for model in GPT_MODEL_NAMES:
            if (
                model[0] not in [m[0] for m in GPT_MODEL_NAMES]
            ):
                GPT_MODEL_NAMES.remove(model)

        super().save(
            force_insert,
            force_update,
            using,
            update_fields
        )
