#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: custom_api_admin.py
#  Last Modified: 2024-09-28 16:08:50
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:59:26
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib import admin

from apps.mm_apis.models import CustomAPI


@admin.register(CustomAPI)
class CustomAPIAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "categories", "created_by_user", "created_at", "updated_at"]
    search_fields = ["name", "description", "categories", "created_by_user__username"]
    list_filter = ["categories", "created_at", "updated_at"]
    list_per_page = 20
