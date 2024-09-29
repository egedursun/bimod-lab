#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: custom_function_reference_admin.py
#  Last Modified: 2024-09-28 16:27:57
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:00:57
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib import admin

from apps.mm_functions.models import CustomFunctionReference


@admin.register(CustomFunctionReference)
class CustomFunctionReferenceAdmin(admin.ModelAdmin):
    list_display = ("custom_function", "assistant", "created_by_user", "created_at", "updated_at")
    list_filter = ("assistant", "created_by_user")
    search_fields = ("custom_function__name", "assistant__name")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
