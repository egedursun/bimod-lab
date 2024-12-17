#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: slider_google_apps_connection_models.py
#  Last Modified: 2024-10-31 05:36:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-02 19:56:26
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

from apps.slider.models import (
    SliderGoogleAppsConnection
)

from apps.slider.utils import (
    SLIDER_GOOGLE_APPS_CONNECTION_ADMIN_LIST,
    SLIDER_GOOGLE_APPS_CONNECTION_ADMIN_FILTER,
    SLIDER_GOOGLE_APPS_CONNECTION_ADMIN_SEARCH
)


@admin.register(SliderGoogleAppsConnection)
class SliderGoogleAppsConnectionAdmin(admin.ModelAdmin):
    list_display = SLIDER_GOOGLE_APPS_CONNECTION_ADMIN_LIST
    list_filter = SLIDER_GOOGLE_APPS_CONNECTION_ADMIN_FILTER
    search_fields = SLIDER_GOOGLE_APPS_CONNECTION_ADMIN_SEARCH

    ordering = ('-created_at', '-updated_at')
