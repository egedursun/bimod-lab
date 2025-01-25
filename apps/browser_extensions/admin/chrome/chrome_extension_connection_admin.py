#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: chrome_extension_connection_admin.py
#  Last Modified: 2024-12-23 09:37:17
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-23 09:37:17
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

from apps.browser_extensions.models import (
    ChromeExtensionConnection,
)

from apps.browser_extensions.utils import (
    CHROME_EXTENSION_CONNECTION_ADMIN_LIST,
    CHROME_EXTENSION_CONNECTION_ADMIN_FILTER,
    CHROME_EXTENSION_CONNECTION_ADMIN_SEARCH
)


@admin.register(ChromeExtensionConnection)
class DChromeExtensionConnectionAdmin(admin.ModelAdmin):
    list_display = CHROME_EXTENSION_CONNECTION_ADMIN_LIST
    list_filter = CHROME_EXTENSION_CONNECTION_ADMIN_FILTER
    search_fields = CHROME_EXTENSION_CONNECTION_ADMIN_SEARCH

    ordering = ('-created_at', '-updated_at')
