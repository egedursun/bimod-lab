#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: export_assistant_models.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:42
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: export_assistant_models.py
#  Last Modified: 2024-09-27 19:45:58
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:50:16
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.db import models
from django.utils import timezone

from apps.export_assistants.models import RequestLog
from apps.export_assistants.utils import generate_assistant_custom_api_key, generate_endpoint
from config.settings import BASE_URL, EXPORT_API_BASE_URL


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
    organization = models.ForeignKey("organization.Organization", on_delete=models.CASCADE,
                                     related_name='exported_assistants',
                                     default=2, null=True, blank=True)
    assistant = models.ForeignKey('assistants.Assistant', on_delete=models.CASCADE, related_name='exported_assistants')
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
