#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: semantor_configuration_admin.py
#  Last Modified: 2024-11-10 00:33:51
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-10 00:33:51
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

from apps.semantor.models import SemantorConfiguration
from apps.semantor.utils.constant_utils import SEMANTOR_CONFIGURATION_ADMIN_LIST, SEMANTOR_CONFIGURATION_ADMIN_FILTER, \
    SEMANTOR_CONFIGURATION_ADMIN_SEARCH


@admin.register(SemantorConfiguration)
class SemantorConfigurationAdmin(admin.ModelAdmin):
    list_display = SEMANTOR_CONFIGURATION_ADMIN_LIST
    list_filter = SEMANTOR_CONFIGURATION_ADMIN_FILTER
    search_fields = SEMANTOR_CONFIGURATION_ADMIN_SEARCH
    ordering = ['user', 'created_at', 'updated_at']
