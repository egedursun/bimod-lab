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
    ("gpt-3.5-turbo-16k", "gpt-3.5-turbo-16k"),
    ("gpt-3.5-turbo", "gpt-3.5-turbo"),
]


class LLMCore(models.Model):
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

    organization = models.ForeignKey("organization.Organization", on_delete=models.CASCADE)

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = "LLM Core"
        verbose_name_plural = "LLM Cores"

    def get_provider_name(self):
        return dict(LLM_CORE_PROVIDERS)[self.provider]

