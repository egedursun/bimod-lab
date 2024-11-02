#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: slider_folder_admin.py
#  Last Modified: 2024-10-17 16:15:05
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-02 19:56:18
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

from apps.slider.models import SliderFolder
from apps.slider.utils import SLIDER_FOLDER_ADMIN_LIST, SLIDER_FOLDER_ADMIN_FILTER, SLIDER_FOLDER_ADMIN_SEARCH


@admin.register(SliderFolder)
class SliderFolderAdmin(admin.ModelAdmin):
    list_display = SLIDER_FOLDER_ADMIN_LIST
    list_filter = SLIDER_FOLDER_ADMIN_FILTER
    search_fields = SLIDER_FOLDER_ADMIN_SEARCH
    ordering = ('-created_at',)
