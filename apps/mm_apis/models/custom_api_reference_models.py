#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: custom_api_reference_models.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:33
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#

from django.db import models


class CustomAPIReference(models.Model):
    """
    CustomAPIReference Model:
    - Purpose: Represents a reference to a custom API associated with a specific assistant, storing information about the API source and the user who created the reference.
    - Key Fields:
        - `custom_api`: ForeignKey linking to the `CustomAPI` model.
        - `assistant`: ForeignKey linking to the `Assistant` model.
        - `api_source`: A field indicating whether the API is internal or external.
        - `created_by_user`: ForeignKey linking to the `User` who created the API reference.
        - `created_at`, `updated_at`: Timestamps for creation and last update.
    - Meta:
        - `verbose_name`: "Custom API Reference"
        - `verbose_name_plural`: "Custom API References"
        - `unique_together`: Ensures that each combination of `custom_api` and `assistant` is unique.
        - `indexes`: Indexes on various fields for optimized queries.
    """

    custom_api = models.ForeignKey("CustomAPI", on_delete=models.CASCADE, related_name="custom_api_references")
    assistant = models.ForeignKey("assistants.Assistant", on_delete=models.CASCADE)
    api_source = models.CharField(max_length=255, default="internal", blank=True)
    created_by_user = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.custom_api.name + " - " + self.assistant.name + " - " + self.created_at.strftime(
            "%Y-%m-%d %H:%M:%S")

    class Meta:
        verbose_name = "Custom API Reference"
        verbose_name_plural = "Custom API References"
        unique_together = [["custom_api", "assistant"]]
        indexes = [
            models.Index(fields=["custom_api", "assistant"]),
            models.Index(fields=["assistant", "custom_api", "created_by_user"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["assistant"]),
            models.Index(fields=["custom_api"]),
            models.Index(fields=["created_by_user"]),
        ]
