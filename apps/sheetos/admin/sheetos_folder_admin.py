#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: sheetos_folder_admin.py
#  Last Modified: 2024-10-31 18:34:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-31 18:34:07
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

from apps.sheetos.models import SheetosFolder
from apps.sheetos.utils import SHEETOS_FOLDER_ADMIN_LIST, SHEETOS_FOLDER_ADMIN_FILTER, SHEETOS_FOLDER_ADMIN_SEARCH


@admin.register(SheetosFolder)
class SheetosFolderAdmin(admin.ModelAdmin):
    list_display = SHEETOS_FOLDER_ADMIN_LIST
    list_filter = SHEETOS_FOLDER_ADMIN_FILTER
    search_fields = SHEETOS_FOLDER_ADMIN_SEARCH
    ordering = ('-created_at',)
