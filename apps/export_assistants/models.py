"""
Module Overview: This module defines models for managing exported assistant APIs and their request logs within an assistant-based application. It includes functionality for generating API keys and endpoints, tracking API requests, and enforcing rate limits.

Dependencies:
- `django.db.models`: Django's ORM for defining database models.
- `django.utils.timezone`: Django utility for handling timezone-aware datetime objects.
- `apps.export_assistants.utils`: Custom utilities for generating API keys and endpoints.
- `config.settings`: Application settings, particularly for accessing base URLs for the API.
"""

from django.db import models
from django.utils import timezone

from apps.export_assistants.utils import generate_assistant_custom_api_key, generate_endpoint
from config.settings import EXPORT_API_BASE_URL, BASE_URL


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


class ExportAssistantAPI(models.Model):
    """
    ExportAssistantAPI Model:
    - Purpose: Represents an exported assistant API, storing metadata and settings such as API key, endpoint, rate limits, and status (public or online).
    - Key Fields:
        - `assistant`: ForeignKey linking to the `Assistant` model.
        - `is_public`: Boolean flag indicating whether the API is publicly accessible.
        - `request_limit_per_hour`: Integer field defining the maximum number of requests allowed per hour.
        - `is_online`: Boolean flag indicating whether the API is currently online.
        - `custom_api_key`: Optional API key for non-public usage.
        - `endpoint`: The endpoint URL for accessing the exported assistant API.
        - `created_at`, `updated_at`: Timestamps for creation and last update.
        - `created_by_user`: ForeignKey linking to the user who created the exported assistant API.
    - Methods:
        - `save()`: Overridden to generate the endpoint and API key if not provided, and then save the model.
        - `requests_in_last_hour()`: Returns the count of requests made in the last hour.
        - `requests_limit_reached()`: Checks if the request limit for the last hour has been reached.
    - Meta:
        - `verbose_name`: "Export Assistant API"
        - `verbose_name_plural`: "Export Assistant APIs"
        - `ordering`: Orders APIs by creation date in descending order.
        - `indexes`: Indexes on `assistant`, `created_by_user`, `created_at`, `updated_at`, and various combinations for optimized queries.
    """

    assistant = models.ForeignKey('assistants.Assistant', on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)
    request_limit_per_hour = models.IntegerField(default=1000)
    is_online = models.BooleanField(default=True)

    custom_api_key = models.CharField(max_length=1000, blank=True, null=True, unique=True)
    endpoint = models.CharField(max_length=1000, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by_user = models.ForeignKey("auth.User", on_delete=models.CASCADE,
                                        related_name='export_assistants_created_by_user')

    def __str__(self):
        return self.assistant.name

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        # generate the endpoint for the exported assistant
        if not self.endpoint:
            self.endpoint = BASE_URL + "/" + EXPORT_API_BASE_URL + "/" + generate_endpoint(self.assistant)
        # generate the API key for non-public usage of the exported assistant
        if not self.custom_api_key and (not self.is_public):
            self.custom_api_key = generate_assistant_custom_api_key(self.assistant)
        super().save(force_insert, force_update, using, update_fields)

    def requests_in_last_hour(self):
        one_hour_ago = timezone.now() - timezone.timedelta(hours=1)
        return RequestLog.objects.filter(export_assistant=self, timestamp__gte=one_hour_ago).count()

    def requests_limit_reached(self):
        return self.requests_in_last_hour() >= self.request_limit_per_hour

    class Meta:
        verbose_name = "Export Assistant API"
        verbose_name_plural = "Export Assistant APIs"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['assistant']),
            models.Index(fields=['created_by_user']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
            models.Index(fields=['assistant', 'created_at']),
            models.Index(fields=['assistant', 'updated_at']),
            models.Index(fields=['assistant', 'created_by_user']),
        ]
