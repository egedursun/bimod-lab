#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: llm_core_models.py
#  Last Modified: 2024-09-27 17:27:16
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:56:05
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.db import models

from apps.finetuning.models import FineTunedModelConnection
from apps.llm_core.utils import LLM_CORE_PROVIDERS, OPENAI_GPT_MODEL_NAMES


class LLMCore(models.Model):
    """
    LLMCore Model:
    - Purpose: Represents a configuration for a Language Model (LLM) core, storing details such as the provider, API key, model name, and various model-specific parameters.
    - Key Fields:
        - `nickname`: A user-defined nickname for the LLM core.
        - `description`: An optional description of the LLM core.
        - `provider`: The provider of the LLM core (e.g., OpenAI-GPT).
        - `api_key`: The API key used to access the LLM core.
        - `model_name`: The name of the model used within the LLM core (e.g., gpt-4o, gpt-4-turbo).
        - `temperature`, `maximum_tokens`, `stop_sequences`, `top_p`, `frequency_penalty`, `presence_penalty`: Model-specific parameters that control the behavior of the LLM core.
        - `created_at`, `updated_at`: Timestamps for creation and last update.
        - `created_by_user`, `last_updated_by_user`: ForeignKey fields linking to the user who created or last updated the LLM core.
        - `organization`: ForeignKey linking to the organization associated with the LLM core.
    - Methods:
        - `__str__()`: Returns the nickname of the LLM core.
        - `get_provider_name()`: Returns the full name of the provider based on the `provider` field.
    - Meta:
        - `verbose_name`: "LLM Core"
        - `verbose_name_plural`: "LLM Cores"
        - `ordering`: Orders LLM cores by creation date in descending order.
        - `indexes`: Indexes on various fields such as `nickname`, `provider`, `model_name`, `organization`, and related user fields for optimized queries.
    """

    nickname = models.CharField(max_length=255)
    description = models.TextField(default="", blank=True)
    provider = models.CharField(max_length=2, choices=LLM_CORE_PROVIDERS)
    api_key = models.CharField(max_length=8192)
    model_name = models.CharField(max_length=1000)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, default=0.50)
    maximum_tokens = models.IntegerField(default=4094)
    stop_sequences = models.TextField(default="", blank=True)
    top_p = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)
    frequency_penalty = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    presence_penalty = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by_user = models.ForeignKey("auth.User", on_delete=models.CASCADE,
                                        related_name="llm_core_created_by_users")
    last_updated_by_user = models.ForeignKey("auth.User", on_delete=models.CASCADE,
                                             related_name="llm_core_last_updated_by_users")

    organization = models.ForeignKey("organization.Organization", on_delete=models.CASCADE,
                                     related_name="llm_cores", null=True)

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = "LLM Core"
        verbose_name_plural = "LLM Cores"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["nickname"]),
            models.Index(fields=["provider"]),
            models.Index(fields=["model_name"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),
            models.Index(fields=["organization"]),
            models.Index(fields=["created_by_user"]),
            models.Index(fields=["last_updated_by_user"]),
            models.Index(fields=["organization", "nickname"]),
            models.Index(fields=["organization", "provider"]),
            models.Index(fields=["organization", "model_name"]),
            models.Index(fields=["organization", "created_at"]),
            models.Index(fields=["organization", "updated_at"]),
            models.Index(fields=["organization", "created_by_user"]),
            models.Index(fields=["organization", "last_updated_by_user"]),
        ]

    def get_provider_name(self):
        return dict(LLM_CORE_PROVIDERS)[self.provider]

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # add the fine-tuned instances
        fine_tuned_models = FineTunedModelConnection.objects.filter(
            organization__in=[self.organization]
        ).all()
        for model in fine_tuned_models:
            if model.model_name not in [m[0] for m in OPENAI_GPT_MODEL_NAMES]:
                OPENAI_GPT_MODEL_NAMES.append((model.model_name, model.nickname))
        for model in OPENAI_GPT_MODEL_NAMES:
            if (model[0] not in [m[0] for m in OPENAI_GPT_MODEL_NAMES] and model[0] not in [m[0] for m in
                                                                                            fine_tuned_models]):
                OPENAI_GPT_MODEL_NAMES.remove(model)

        super().save(force_insert, force_update, using, update_fields)
