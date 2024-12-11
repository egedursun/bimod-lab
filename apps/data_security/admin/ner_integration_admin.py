#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
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
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.contrib import admin

from apps.data_security.models import (
    NERIntegration
)

from apps.data_security.utils import (
    NER_INTEGRATION_ADMIN_LIST,
    NER_INTEGRATION_ADMIN_SEARCH,
    NER_INTEGRATION_ADMIN_FILTER
)


@admin.register(NERIntegration)
class NERIntegrationAdmin(admin.ModelAdmin):
    list_display = NER_INTEGRATION_ADMIN_LIST
    list_filter = NER_INTEGRATION_ADMIN_FILTER
    search_fields = NER_INTEGRATION_ADMIN_SEARCH

    readonly_fields = (
        'created_at',
        'updated_at'
    )
