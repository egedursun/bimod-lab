#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: custom_script_reference_admin.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:38
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from django.contrib import admin

from apps.mm_scripts.models import CustomScriptReference


@admin.register(CustomScriptReference)
class CustomScriptReferenceAdmin(admin.ModelAdmin):
    list_display = ("custom_script", "assistant", "created_by_user", "created_at", "updated_at")
    list_filter = ("assistant", "created_by_user")
    search_fields = ("custom_script__name", "assistant__name")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
