#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: action_019_balance_top_up_plan_create.py
#  Last Modified: 2024-11-18 22:26:03
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-18 22:26:04
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

from apps.llm_transaction.models import (
    AutoBalanceTopUpModel
)

from apps.organization.models import Organization

logger = logging.getLogger(__name__)


def action__019_balance_top_up_plan_create(
    metadata__user,
    metadata__organization,
    option,
    response__balance_top_up_amount,
    response__balance_top_up_interval_days,
    response__balance_top_up_threshold_value,
    response__balance_top_up_hard_limit
):
    if option == 'regular_interval':

        try:
            new_top_up_instance = AutoBalanceTopUpModel.objects.create(
                organization=metadata__organization,
                on_balance_threshold_trigger=False,
                on_interval_by_days_trigger=True,
                regular_by_days_interval=response__balance_top_up_interval_days,
                addition_on_interval_by_days_trigger=response__balance_top_up_amount,
                monthly_hard_limit_auto_addition_amount=response__balance_top_up_hard_limit
            )

            metadata__organization: Organization
            metadata__organization.auto_balance_topup = new_top_up_instance

            metadata__organization.save()

        except Exception as e:
            logger.error(f"Error on action__019_balance_top_up_plan_create [regular_interval]: {e}")
            return False, None

    elif option == 'threshold_trigger':

        try:
            new_top_up_instance = AutoBalanceTopUpModel.objects.create(
                organization=metadata__organization,
                on_balance_threshold_trigger=True,
                on_interval_by_days_trigger=False,
                balance_lower_trigger_threshold_value=response__balance_top_up_threshold_value,
                addition_on_balance_threshold_trigger=response__balance_top_up_amount,
                monthly_hard_limit_auto_addition_amount=response__balance_top_up_hard_limit
            )

            metadata__organization: Organization
            metadata__organization.auto_balance_topup = new_top_up_instance

            metadata__organization.save()

        except Exception as e:
            logger.error(f"Error on action__019_balance_top_up_plan_create [threshold_trigger]: {e}")

            return False, None

    else:
        logger.error(f"Invalid balance top-up option: {option}")

        return False, None

    logger.info(f"New balance top-up plan created for user: {metadata__user.username}")

    return True, new_top_up_instance
