#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: custom_function_reference_models.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:37
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
#  File: custom_function_reference_models.py
#  Last Modified: 2024-09-28 16:27:57
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:01:07
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.db import models


class CustomFunctionReference(models.Model):
    """
    CustomFunctionReference Model:
    - Purpose: Represents a reference to a custom function associated with a specific assistant, storing information about the function source and the user who created the reference.
    - Key Fields:
        - `custom_function`: ForeignKey linking to the `CustomFunction` model.
        - `assistant`: ForeignKey linking to the `Assistant` model.
        - `function_source`: A field indicating whether the function is internal or external.
        - `created_by_user`: ForeignKey linking to the `User` who created the function reference.
        - `created_at`, `updated_at`: Timestamps for creation and last update.
    - Meta:
        - `verbose_name`: "Custom Function Reference"
        - `verbose_name_plural`: "Custom Function References"
        - `unique_together`: Ensures that each combination of `custom_function` and `assistant` is unique.
        - `indexes`: Indexes on various fields for optimized queries.
    """
    organization = models.ForeignKey("organization.Organization", on_delete=models.CASCADE, null=True, blank=True,
                                     related_name="custom_function_references")
    custom_function = models.ForeignKey("CustomFunction", on_delete=models.CASCADE,
                                        related_name="custom_function_references")
    assistant = models.ForeignKey("assistants.Assistant", on_delete=models.CASCADE)
    function_source = models.CharField(max_length=255, default="internal", blank=True)
    created_by_user = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.custom_function.name + " - " + self.assistant.name + " - " + self.created_at.strftime(
            "%Y-%m-%d %H:%M:%S")

    class Meta:
        verbose_name = "Custom Function Reference"
        verbose_name_plural = "Custom Function References"
        unique_together = [["custom_function", "assistant"]]
        indexes = [
            models.Index(fields=["custom_function", "assistant"]),
            models.Index(fields=["assistant", "custom_function", "created_by_user"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["assistant"]),
            models.Index(fields=["custom_function"]),
            models.Index(fields=["created_by_user"]),
        ]
