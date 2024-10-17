#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: auto_topup_models.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:43
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
#
#
#

from django.db import models


class AutoBalanceTopUpModel(models.Model):
    organization = models.ForeignKey('organization.Organization', on_delete=models.SET_NULL,
                                     related_name='auto_balance_top_ups',
                                     null=True)
    on_balance_threshold_trigger = models.BooleanField(default=False)
    on_interval_by_days_trigger = models.BooleanField(default=False)
    balance_lower_trigger_threshold_value = models.DecimalField(max_digits=12, decimal_places=6, null=True, blank=True)
    addition_on_balance_threshold_trigger = models.DecimalField(max_digits=12, decimal_places=6, null=True, blank=True)
    regular_by_days_interval = models.IntegerField(null=True, blank=True)
    addition_on_interval_by_days_trigger = models.DecimalField(max_digits=12, decimal_places=6, null=True, blank=True)
    date_of_last_auto_top_up = models.DateTimeField(null=True, blank=True)
    calendar_month_total_auto_addition_value = models.DecimalField(max_digits=12, decimal_places=6, null=True,
                                                                   blank=True)
    monthly_hard_limit_auto_addition_amount = models.DecimalField(max_digits=12, decimal_places=6, null=True,
                                                                  blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.organization} - {self.created_at}"

    class Meta:
        verbose_name = "Auto Balance Top Up"
        verbose_name_plural = "Auto Balance Top Ups"
        ordering = ["-created_at"]
