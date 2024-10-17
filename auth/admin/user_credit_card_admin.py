#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: user_credit_card_admin.py
#  Last Modified: 2024-10-09 19:13:19
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-09 19:14:56
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

from auth.models import UserCreditCard
from auth.utils import CREDIT_CARD_ADMIN_LIST


@admin.register(UserCreditCard)
class UserCreditCardAdmin(admin.ModelAdmin):
    list_display = CREDIT_CARD_ADMIN_LIST
