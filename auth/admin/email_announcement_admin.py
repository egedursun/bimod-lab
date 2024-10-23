#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: email_announcement_admin.py
#  Last Modified: 2024-10-23 18:10:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-23 18:10:08
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

from auth.models import BimodEmailAnnouncement
from auth.utils import BIMOID_EMAIL_ANNOUNCEMENT_ADMIN_LIST, BIMOID_EMAIL_ANNOUNCEMENT_ADMIN_SEARCH, \
    BIMOID_EMAIL_ANNOUNCEMENT_ADMIN_FILTER


@admin.register(BimodEmailAnnouncement)
class BimodEmailAnnouncementAdmin(admin.ModelAdmin):
    list_display = BIMOID_EMAIL_ANNOUNCEMENT_ADMIN_LIST
    search_fields = BIMOID_EMAIL_ANNOUNCEMENT_ADMIN_SEARCH
    list_filter = BIMOID_EMAIL_ANNOUNCEMENT_ADMIN_FILTER
    readonly_fields = ['created_at']
