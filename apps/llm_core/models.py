"""
Module Overview: This module defines the `LLMCore` model, which represents a configuration for a Language Model (LLM) core within an assistant-based application. The model includes settings for API keys, model parameters, and metadata such as provider type, model name, and organization association.

Dependencies:
- `django.db.models`: Django's ORM for defining database models.
"""

from django.db import models

# Define enumeration for the provider
LLM_CORE_PROVIDERS = [
    ("OA", "OpenAI-GPT"),
]

# OPENAI GPT model names
OPENAI_GPT_MODEL_NAMES = [
    ("gpt-4o", "gpt-4o"),
    ("gpt-4-turbo", "gpt-4-turbo"),
    ("gpt-4", "gpt-4"),
]


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
    model_name = models.CharField(max_length=255, choices=OPENAI_GPT_MODEL_NAMES)
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
                                     related_name="llm_cores_organization", default=6)

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
