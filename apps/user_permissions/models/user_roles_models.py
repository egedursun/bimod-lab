#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: user_roles_models.py
#  Last Modified: 2024-09-29 16:38:53
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-29 16:39:00
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.db import models


class UserRole(models.Model):
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE)
    role_name = models.CharField(max_length=1000)
    role_description = models.TextField(null=True, blank=True)
    role_permissions = models.JSONField(default=list)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by_user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='created_roles')

    class Meta:
        verbose_name = 'User Role'
        verbose_name_plural = 'User Roles'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['organization']),
            models.Index(fields=['role_name']),
            models.Index(fields=['organization', 'role_name']),
            models.Index(fields=['organization', 'role_name', 'created_at']),
        ]

    def __str__(self):
        return self.organization.name + ' - ' + self.role_name + ' Role'
