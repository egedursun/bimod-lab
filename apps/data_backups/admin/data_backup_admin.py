#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
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
#   For permission inquiries, please contact: admin@Bimod.io.
#


from django.contrib import admin

from apps.data_backups.models import DataBackup
from apps.data_backups.utils import DATA_BACKUP_ADMIN_LIST, DATA_BACKUP_ADMIN_SEARCH, DATA_BACKUP_ADMIN_FILTER


@admin.register(DataBackup)
class DataBackupAdmin(admin.ModelAdmin):
    list_display = DATA_BACKUP_ADMIN_LIST
    list_filter = DATA_BACKUP_ADMIN_FILTER
    search_fields = DATA_BACKUP_ADMIN_SEARCH
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    actions = ['delete_selected']
