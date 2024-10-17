#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: audit_log_models.py
#  Last Modified: 2024-10-11 05:22:34
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-11 05:22:35
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
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.audit_logs.utils import AUDIT_LOG_ACTION_CHOICES


class AuditLog(models.Model):
    action = models.CharField(max_length=6, choices=AUDIT_LOG_ACTION_CHOICES)
    model_name = models.CharField(max_length=10000)
    object_id = models.PositiveIntegerField()
    timestamp = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL)
    changes = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = "Audit Log"
        verbose_name_plural = "Audit Logs"
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["object_id"]),
            models.Index(fields=["model_name"]),
            models.Index(fields=["timestamp"]),
            models.Index(fields=["user"]),
            models.Index(fields=["action"]),
            models.Index(fields=["model_name", "object_id"]),
            models.Index(fields=["model_name", "object_id", "action"]),
            models.Index(fields=["model_name", "object_id", "timestamp"]),
            models.Index(fields=["model_name", "object_id", "user"]),
            models.Index(fields=["model_name", "object_id", "action", "timestamp"]),
            models.Index(fields=["model_name", "object_id", "action", "user"]),
            models.Index(fields=["model_name", "object_id", "action", "timestamp", "user"]),
        ]

    def __str__(self):
        return f"AuditLog - {self.model_name} - {self.object_id} - {self.action}"

    def save_changes(self, old_instance, new_instance):
        old_values = old_instance.__dict__
        new_values = new_instance.__dict__
        changes = {field: {"old": old_values[field], "new": new_values[field]}
                   for field in new_values if old_values.get(field) != new_values.get(field)}
        self.changes = changes
