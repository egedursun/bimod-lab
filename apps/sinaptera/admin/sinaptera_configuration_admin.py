#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: sinaptera_configuration_admin.py
#  Last Modified: 2024-12-14 17:22:58
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-14 17:22:59
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

from apps.sinaptera.models import (
    SinapteraConfiguration
)

from apps.sinaptera.utils import (
    SINAPTERA_CONFIGURATION_ADMIN_LIST,
    SINAPTERA_CONFIGURATION_ADMIN_FILTER,
    SINAPTERA_CONFIGURATION_ADMIN_SEARCH
)


@admin.register(SinapteraConfiguration)
class SinapteraConfigurationAdmin(admin.ModelAdmin):
    list_display = SINAPTERA_CONFIGURATION_ADMIN_LIST
    list_filter = SINAPTERA_CONFIGURATION_ADMIN_FILTER
    search_fields = SINAPTERA_CONFIGURATION_ADMIN_SEARCH

    ordering = ['-created_at']
