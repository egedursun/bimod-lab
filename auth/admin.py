#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: admin.py
#  Last Modified: 2024-09-15 15:15:41
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:13:59
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib import admin
from .models import Profile, UserCreditCard, PromoCode


# Register your models here.
class Member(admin.ModelAdmin):
    list_display = (
        "user", "email", "is_verified", "is_accredited_by_staff", "created_at",
    )


@admin.register(UserCreditCard)
class UserCreditCardAdmin(admin.ModelAdmin):
    list_display = (
        "name_on_card", "card_number", "card_expiration_month", "card_expiration_year", "card_cvc", "created_at",
    )


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = (
        "user", "code", "bonus_percentage_referrer", "bonus_percentage_referee", "is_active", "current_referrals",
        "max_referral_limit", "datetime_limit", "created_at",
    )


admin.site.register(Profile, Member)
