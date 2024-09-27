from django.db import models


class DocumentProcessingLog(models.Model):
    """
    DocumentProcessingLog Model:
    - Purpose: Logs the processing activities of a document, storing information about the document's URI and associated log messages.
    - Key Fields:
        - `document_full_uri`: The full URI of the document being processed.
        - `log_message`: A text field for storing log messages related to document processing.
        - `created_at`: Timestamp for when the log was created.
    """

    document_full_uri = models.CharField(max_length=1000)
    log_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.document_full_uri + " - " + self.created_at.strftime("%Y%m%d%H%M%S")

    class Meta:
        verbose_name = "Document Processing Log"
        verbose_name_plural = "Document Processing Logs"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["document_full_uri"]),
            models.Index(fields=["created_at"]),
        ]
