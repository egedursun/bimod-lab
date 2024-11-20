#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: actions_018_credit_card_create.py
#  Last Modified: 2024-11-18 22:25:51
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-18 22:25:51
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

from django.contrib.auth.models import User

from auth.models import UserCreditCard

logger = logging.getLogger(__name__)


def action__018_credit_card_create(
    metadata__user,
    response__payment_method_credit_card_name,
    response__payment_method_credit_card_number,
    response__payment_method_credit_card_expiration_month,
    response__payment_method_credit_card_expiration_year,
    response__payment_method_credit_card_cvc
):
    metadata__user: User
    try:
        new_payment_method = UserCreditCard.objects.create(
            user=metadata__user,
            profile=metadata__user.profile,
            name_on_card=response__payment_method_credit_card_name,
            card_number=response__payment_method_credit_card_number,
            card_expiration_month=response__payment_method_credit_card_expiration_month,
            card_expiration_year=response__payment_method_credit_card_expiration_year,
            card_cvc=response__payment_method_credit_card_cvc
        )

    except Exception as e:
        logger.error(f"Error on action__018_credit_card_create: {e}")
        return False, None

    logger.info(f"New credit card created for user: {metadata__user.username}")
    return True, new_payment_method
