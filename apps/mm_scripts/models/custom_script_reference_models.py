#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: custom_script_reference_models.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:38
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


class CustomScriptReference(models.Model):
    custom_script = models.ForeignKey("CustomScript", on_delete=models.CASCADE,
                                      related_name="custom_script_references")
    assistant = models.ForeignKey("assistants.Assistant", on_delete=models.CASCADE)
    script_source = models.CharField(max_length=255, default="internal", blank=True)
    created_by_user = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.custom_script.name + " - " + self.assistant.name + " - " + self.created_at.strftime(
            "%Y-%m-%d %H:%M:%S")

    class Meta:
        verbose_name = "Custom Script Reference"
        verbose_name_plural = "Custom Script References"
        unique_together = [["custom_script", "assistant"]]
        indexes = [
            models.Index(fields=["custom_script", "assistant"]),
            models.Index(fields=["assistant", "custom_script", "created_by_user"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["assistant"]),
            models.Index(fields=["custom_script"]),
            models.Index(fields=["created_by_user"]),
        ]
