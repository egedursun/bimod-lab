#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: custom_api_admin.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:33
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

from apps.mm_apis.models import CustomAPI
from apps.mm_apis.utils import CUSTOM_API_ADMIN_LIST, CUSTOM_API_ADMIN_FILTER, CUSTOM_API_ADMIN_SEARCH


@admin.register(CustomAPI)
class CustomAPIAdmin(admin.ModelAdmin):
    list_display = CUSTOM_API_ADMIN_LIST
    search_fields = CUSTOM_API_ADMIN_SEARCH
    list_filter = CUSTOM_API_ADMIN_FILTER
