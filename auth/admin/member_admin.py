#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: member_admin.py
#  Last Modified: 2024-10-09 19:13:05
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-09 19:13:05
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

from auth.models import Profile

from auth.utils import (
    MEMBER_ADMIN_LIST
)


class Member(admin.ModelAdmin):
    list_display = MEMBER_ADMIN_LIST


admin.site.register(
    Profile,
    Member
)
