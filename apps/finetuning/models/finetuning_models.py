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
