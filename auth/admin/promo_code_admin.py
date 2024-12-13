#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: promo_code_admin.py
#  Last Modified: 2024-10-09 19:13:29
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-09 19:13:30
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

from auth.models import PromoCode

from auth.utils import (
    PROMO_CODE_ADMIN_LIST
)


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = PROMO_CODE_ADMIN_LIST
