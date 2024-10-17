#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: promo_code_models.py
#  Last Modified: 2024-10-09 19:21:20
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-09 19:21:21
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


from django.db import models

from auth.utils import REFERRAL_DEFAULT_BONUS_PERCENTAGE


class PromoCode(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="promo_codes")
    code = models.CharField(max_length=255)
    bonus_percentage_referrer = models.IntegerField(default=REFERRAL_DEFAULT_BONUS_PERCENTAGE)
    bonus_percentage_referee = models.IntegerField(default=REFERRAL_DEFAULT_BONUS_PERCENTAGE)
    is_active = models.BooleanField(default=True)
    current_referrals = models.IntegerField(default=0)
    max_referral_limit = models.IntegerField(default=0)
    datetime_limit = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Promo Code"
        verbose_name_plural = "Promo Codes"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["created_at"]),
        ]
