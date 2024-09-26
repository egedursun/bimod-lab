from django.db import models


class RepositoryProcessingLog(models.Model):
    repository_full_uri = models.CharField(max_length=1000)
    log_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.repository_full_uri + " - " + self.created_at.strftime("%Y%m%d%H%M%S")

    class Meta:
        verbose_name = "Repository Processing Log"
        verbose_name_plural = "Repository Processing Logs"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["repository_full_uri"]),
            models.Index(fields=["created_at"]),
        ]
