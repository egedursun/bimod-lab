#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: custom_function_reference_models.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:40
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
#
#
#

from django.db import models


class CustomFunctionReference(models.Model):
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
