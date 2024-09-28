from django.db import models


class LeanmodRequestLog(models.Model):
    export_lean_assistant = models.ForeignKey('ExportLeanmodAssistantAPI', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Request LeanMod Log"
        verbose_name_plural = "Request LeanMod Logs"
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['export_lean_assistant']),
            models.Index(fields=['timestamp']),
            models.Index(fields=['export_lean_assistant', 'timestamp']),
        ]
