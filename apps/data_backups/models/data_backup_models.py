#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: data_backup_models.py
#  Last Modified: 2024-09-30 16:47:04
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
#  File: data_backup_log_models.py
#  Last Modified: 2024-09-30 01:29:27
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-30 01:29:28
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@bimod.io.
#


from django.db import models
from apps.data_backups.utils import BACKUP_TYPES


class DataBackup(models.Model):
    responsible_user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE, null=True, blank=True)
    backup_name = models.CharField(max_length=255)
    backup_type = models.CharField(max_length=255, choices=BACKUP_TYPES, null=True, blank=True)
    backup_uuid = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    serialized_data = models.TextField(null=True, blank=True)
    encryption_password = models.CharField(max_length=255)

    def __str__(self):
        return self.responsible_user.username + ' - ' + self.backup_name

    class Meta:
        verbose_name = 'Data Backup'
        verbose_name_plural = 'Data Backups'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['organization']),
            models.Index(fields=['responsible_user']),
            models.Index(fields=['backup_name']),
            models.Index(fields=['backup_type']),
            models.Index(fields=['created_at']),
            models.Index(fields=['responsible_user', 'created_at']),
            models.Index(fields=['backup_name', 'created_at']),
            models.Index(fields=['organization', 'responsible_user']),
            models.Index(fields=['organization', 'backup_name']),
            models.Index(fields=['organization', 'backup_type']),
            models.Index(fields=['organization', 'created_at']),
            models.Index(fields=['responsible_user', 'backup_name', 'created_at']),
            models.Index(fields=['responsible_user', 'backup_type', 'created_at']),
            models.Index(fields=['organization', 'responsible_user', 'created_at']),
            models.Index(fields=['organization', 'backup_name', 'created_at']),
            models.Index(fields=['organization', 'responsible_user', 'backup_name', 'created_at']),
            models.Index(fields=['organization', 'responsible_user', 'backup_type', 'created_at']),
            models.Index(fields=['organization', 'backup_name', 'backup_type', 'created_at']),
            models.Index(fields=['organization', 'responsible_user', 'backup_name', 'backup_type', 'created_at']),
        ]
