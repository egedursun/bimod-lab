from django.db import models


class OrchestratorRequestLog(models.Model):
    export_orchestration = models.ForeignKey('ExportOrchestrationAPI', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Request Orchestration Log"
        verbose_name_plural = "Request Orchestration Logs"
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['export_orchestration']),
            models.Index(fields=['timestamp']),
            models.Index(fields=['export_orchestration', 'timestamp']),
        ]
