#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: check_and_perform_auto_topup_tasks.py
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

import logging

from celery import shared_task
from django.utils import timezone

from apps.llm_transaction.models import (
    AutoBalanceTopUpModel,
    TransactionInvoice
)

from apps.llm_transaction.utils import (
    InvoiceTypesNames,
    AcceptedMethodsOfPaymentNames
)

logger = logging.getLogger(__name__)


@shared_task
def check_and_perform_auto_top_up():
    now = timezone.now()

    all_auto_plans = AutoBalanceTopUpModel.objects.filter(
        on_interval_by_days_trigger=True
    )

    if now.day == 20:
        for plan in all_auto_plans:
            plan.calendar_month_total_auto_addition_value = 0

            logger.info(f"Auto Top Up Plan {plan.id} was reset for the month.")

            plan.save()

    for plan in all_auto_plans:
        days_since_last = (now - plan.date_of_last_auto_top_up).days

        if days_since_last >= plan.regular_by_days_interval:

            if plan.calendar_month_total_auto_addition_value + plan.addition_on_interval_by_days_trigger <= plan.monthly_hard_limit_auto_addition_amount:

                plan.organization.balance += plan.addition_on_interval_by_days_trigger

                plan.organization.save()

                logger.info(f"Auto Top Up Plan {plan.id} was triggered.")

                TransactionInvoice.objects.create(
                    organization=plan.organization,
                    responsible_user=plan.organization.created_by_user,
                    transaction_type=InvoiceTypesNames.AUTO_TOP_UP,
                    amount_added=plan.addition_on_interval_by_days_trigger,
                    payment_method=AcceptedMethodsOfPaymentNames.CREDIT_CARD,
                )

                plan.date_of_last_auto_top_up = now
                plan.calendar_month_total_auto_addition_value += plan.addition_on_interval_by_days_trigger

                plan.save()

                logger.info(f"Auto Top Up Plan {plan.id} was updated.")

            else:
                reduced_add_amount = (
                    plan.monthly_hard_limit_auto_addition_amount - plan.calendar_month_total_auto_addition_value
                )

                if reduced_add_amount > 0:
                    plan.organization.balance += reduced_add_amount

                    plan.organization.save()

                    logger.info(f"Auto Top Up Plan {plan.id} was triggered.")

                    TransactionInvoice.objects.create(
                        organization=plan.organization,
                        responsible_user=plan.organization.created_by_user,
                        transaction_type=InvoiceTypesNames.AUTO_TOP_UP,
                        amount_added=reduced_add_amount,
                        payment_method=AcceptedMethodsOfPaymentNames.CREDIT_CARD,
                    )

                    plan.date_of_last_auto_top_up = now
                    plan.calendar_month_total_auto_addition_value += reduced_add_amount

                    plan.save()

                    logger.info(f"Auto Top Up Plan {plan.id} was updated.")

                else:
                    continue
        else:
            continue

    logger.info("Auto Top Up Plans were checked and performed.")

    return True
