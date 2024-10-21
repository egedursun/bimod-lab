#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: notifications_admin.py
#  Last Modified: 2024-10-20 14:08:34
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-20 14:08:34
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
import logging

from django.contrib import admin
from django.contrib.auth.models import User

from apps.notifications.models import NotificationItem
from apps.notifications.utils import NOTIFICATION_ITEM_ADMIN_LIST, NOTIFICATION_ITEM_ADMIN_FILTER, \
    NOTIFICATION_ITEM_ADMIN_SEARCH, NotificationTitleCategoryChoicesNames
from apps.organization.models import Organization

logger = logging.getLogger(__name__)


@admin.register(NotificationItem)
class NotificationItemAdmin(admin.ModelAdmin):
    list_display = NOTIFICATION_ITEM_ADMIN_LIST
    list_filter = NOTIFICATION_ITEM_ADMIN_FILTER
    search_fields = NOTIFICATION_ITEM_ADMIN_SEARCH
    ordering = ('-created_at',)
