#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: user_permission_models.py
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
#   For permission inquiries, please contact: admin@br6.in.
#

from django.db import models

from apps.user_permissions.utils import PERMISSION_TYPES


class ActiveUserPermissionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class UserPermission(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="permissions", null=True)
    permission_type = models.CharField(max_length=255, choices=PERMISSION_TYPES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()  # The default manager.
    active_permissions = ActiveUserPermissionManager()  # Custom manager for active permissions.

    class Meta:
        verbose_name = "User Permission"
        verbose_name_plural = "User Permissions"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=['user', 'permission_type'], name='unique_user_permission')
        ]
        indexes = [
            models.Index(fields=['user', 'permission_type']),
            models.Index(fields=['user', 'permission_type', 'is_active']),
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['permission_type', 'is_active']),
            models.Index(fields=['permission_type']),
            models.Index(fields=['is_active']),
            models.Index(fields=['created_at']),
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['permission_type', 'created_at']),
            models.Index(fields=['user', 'permission_type', 'created_at']),
            models.Index(fields=['user', 'permission_type', 'is_active', 'created_at']),
            models.Index(fields=['user', 'is_active', 'created_at']),
            models.Index(fields=['permission_type', 'is_active', 'created_at']),
        ]

    def get_permission_type_name(self):
        return dict(PERMISSION_TYPES)[self.permission_type]

    def get_permission_type_code(self):
        return self.permission_type
