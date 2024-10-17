#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: user_credit_card_models.py
#  Last Modified: 2024-10-09 19:21:28
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-09 19:21:29
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


from django.contrib.auth.models import User
from django.db import models


class UserCreditCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='credit_cards', blank=True, null=True)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='credit_cards', blank=True,
                                null=True)
    name_on_card = models.CharField(max_length=255, null=False, blank=False)
    card_number = models.CharField(max_length=16, null=False, blank=False)
    card_expiration_month = models.CharField(max_length=2, null=False, blank=False)
    card_expiration_year = models.CharField(max_length=2, null=False, blank=False)
    card_cvc = models.CharField(max_length=4, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.name_on_card}"

    class Meta:
        verbose_name = "Credit Card"
        verbose_name_plural = "Credit Cards"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['user', 'name_on_card', 'card_number', 'created_at']),
            models.Index(
                fields=['user', 'name_on_card', 'card_number', 'card_expiration_month', 'card_expiration_year',
                        'card_cvc', 'created_at'])
        ]
    def save(self, *args, **kwargs):
        self.name_on_card = self.name_on_card.upper()
        super(UserCreditCard, self).save(*args, **kwargs)
        self.user.profile.credit_cards.add(self)
