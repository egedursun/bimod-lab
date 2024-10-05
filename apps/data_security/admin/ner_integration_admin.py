#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: ner_integration_admin.py
#  Last Modified: 2024-10-05 01:39:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:40
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

from apps.data_security.models import NERIntegration


@admin.register(NERIntegration)
class NERIntegrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'language', 'created_by_user', 'created_at', 'updated_at')
    list_filter = ('organization', 'language', 'created_by_user')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
