#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: message_template_models.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:44
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.db import models


class MessageTemplate(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    organization = models.ForeignKey("organization.Organization", on_delete=models.CASCADE)
    template_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Message Template"
        verbose_name_plural = "Message Templates"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["organization"]),
            models.Index(fields=["template_text"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),
            models.Index(fields=["user", "organization"]),
            models.Index(fields=["user", "template_text"]),
            models.Index(fields=["user", "created_at"]),
            models.Index(fields=["user", "updated_at"]),
            models.Index(fields=["organization", "template_text"]),
            models.Index(fields=["organization", "created_at"]),
            models.Index(fields=["organization", "updated_at"]),
            models.Index(fields=["template_text", "created_at"]),
            models.Index(fields=["template_text", "updated_at"]),
            models.Index(fields=["created_at", "updated_at"]),
            models.Index(fields=["user", "organization", "template_text"]),
            models.Index(fields=["user", "organization", "created_at"]),
            models.Index(fields=["user", "organization", "updated_at"]),
            models.Index(fields=["user", "template_text", "created_at"]),
            models.Index(fields=["user", "template_text", "updated_at"]),
            models.Index(fields=["organization", "template_text", "created_at"]),
            models.Index(fields=["organization", "template_text", "updated_at"]),
            models.Index(fields=["template_text", "created_at", "updated_at"]),
            models.Index(fields=["user", "organization", "template_text", "created_at"]),
            models.Index(fields=["user", "organization", "template_text", "updated_at"]),
            models.Index(fields=["user", "organization", "created_at", "updated_at"]),
            models.Index(fields=["user", "template_text", "created_at", "updated_at"]),
            models.Index(fields=["organization", "template_text", "created_at", "updated_at"]),
            models.Index(fields=["user", "organization", "template_text", "created_at", "updated_at"]),
        ]

    def __str__(self):
        return f"{self.user} - {self.organization} - {self.template_text}"
