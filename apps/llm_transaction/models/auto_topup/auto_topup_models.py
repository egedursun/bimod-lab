#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: auto_topup_models.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:39
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: auto_topup_models.py
#  Last Modified: 2024-09-28 15:44:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:56:59
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.db import models


class AutoBalanceTopUpModel(models.Model):
    """
    AutoBalanceTopUpModel:
    - Purpose: Represents the configuration for automatically topping up an organization's balance, with triggers based on balance thresholds or regular intervals.
    - Key Fields:
        - `organization`: ForeignKey linking to the `Organization` that the top-up configuration applies to.
        - `on_balance_threshold_trigger`: Boolean flag indicating if the top-up is triggered by a balance threshold.
        - `on_interval_by_days_trigger`: Boolean flag indicating if the top-up is triggered by regular intervals.
        - `balance_lower_trigger_threshold_value`, `addition_on_balance_threshold_trigger`: Fields related to the balance threshold trigger.
        - `regular_by_days_interval`, `addition_on_interval_by_days_trigger`, `date_of_last_auto_top_up`: Fields related to the interval trigger.
        - `calendar_month_total_auto_addition_value`, `monthly_hard_limit_auto_addition_amount`: Fields for tracking and limiting the total auto-addition value within a month.
        - `created_at`, `updated_at`: Timestamps for creation and last update.
    - Meta:
        - `verbose_name`: "Auto Balance Top Up"
        - `verbose_name_plural`: "Auto Balance Top Ups"
        - `ordering`: Orders top-up configurations by creation date in descending order.
    """

    organization = models.ForeignKey('organization.Organization', on_delete=models.SET_NULL,
                                     related_name='auto_balance_top_ups',
                                     null=True)

    # trigger types
    on_balance_threshold_trigger = models.BooleanField(default=False)
    on_interval_by_days_trigger = models.BooleanField(default=False)

    # on balance threshold parameters
    balance_lower_trigger_threshold_value = models.DecimalField(max_digits=12, decimal_places=6, null=True, blank=True)
    addition_on_balance_threshold_trigger = models.DecimalField(max_digits=12, decimal_places=6, null=True, blank=True)

    # on interval by days parameters
    regular_by_days_interval = models.IntegerField(null=True, blank=True)
    addition_on_interval_by_days_trigger = models.DecimalField(max_digits=12, decimal_places=6, null=True, blank=True)
    date_of_last_auto_top_up = models.DateTimeField(null=True, blank=True)

    # common parameters
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
