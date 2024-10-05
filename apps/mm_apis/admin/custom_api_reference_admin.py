#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: custom_api_reference_admin.py
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
#   For permission inquiries, please contact: admin@br6.in.
#

from django.contrib import admin

from apps.mm_apis.models import CustomAPIReference


@admin.register(CustomAPIReference)
class CustomAPIReferenceAdmin(admin.ModelAdmin):
    list_display = ["custom_api", "assistant", "api_source", "created_by_user", "created_at", "updated_at"]
    search_fields = ["custom_api__name", "assistant__name", "api_source", "created_by_user__username"]
    list_filter = ["api_source", "created_at", "updated_at"]
    list_per_page = 20
