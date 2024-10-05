#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: maestro_admin.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:41
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

from apps.orchestrations.models import Maestro


@admin.register(Maestro)
class MaestroAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization', 'llm_model', 'created_by_user', 'last_updated_by_user', 'created_at',
                    'updated_at']
    search_fields = ['name', 'organization', 'llm_model', 'created_by_user', 'last_updated_by_user']
    list_filter = ['organization', 'llm_model', 'created_by_user', 'last_updated_by_user', 'created_at', 'updated_at']
