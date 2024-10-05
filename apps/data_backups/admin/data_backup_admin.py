#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: data_backup_admin.py
#  Last Modified: 2024-10-05 01:39:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:39
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#


from django.contrib import admin

from apps.data_backups.models import DataBackup


@admin.register(DataBackup)
class DataBackupAdmin(admin.ModelAdmin):
    list_display = ['organization', 'responsible_user', 'backup_name', 'backup_type', 'created_at']
    list_filter = ['organization', 'responsible_user', 'backup_name', 'backup_type', 'created_at']
    search_fields = ['organization', 'responsible_user__username', 'backup_name', 'backup_type']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    actions = ['delete_selected']
