from django.db import models


class RequestLog(models.Model):
    """
    RequestLog Model:
    - Purpose: Tracks individual API requests made to an exported assistant API, storing the timestamp and linking each request to the corresponding `ExportAssistantAPI`.
    - Key Fields:
        - `export_assistant`: ForeignKey linking to the `ExportAssistantAPI` model.
        - `timestamp`: The timestamp of when the API request was made.
    - Meta:
        - `verbose_name`: "Request Log"
        - `verbose_name_plural`: "Request Logs"
        - `ordering`: Orders logs by timestamp in descending order.
        - `indexes`: Indexes on `export_assistant`, `timestamp`, and their combination for optimized queries.
    """

    export_assistant = models.ForeignKey('ExportAssistantAPI', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Request Log"
        verbose_name_plural = "Request Logs"
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['export_assistant']),
            models.Index(fields=['timestamp']),
            models.Index(fields=['export_assistant', 'timestamp']),
        ]
