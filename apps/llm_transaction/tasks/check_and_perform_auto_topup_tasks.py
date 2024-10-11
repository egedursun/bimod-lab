#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from celery import shared_task
from django.utils import timezone

from apps.llm_transaction.models import AutoBalanceTopUpModel, TransactionInvoice
from apps.llm_transaction.utils import InvoiceTypesNames, AcceptedMethodsOfPaymentNames


@shared_task
def check_and_perform_auto_top_up():
    now = timezone.now()
    all_auto_plans = AutoBalanceTopUpModel.objects.filter(on_interval_by_days_trigger=True)
    if now.day == 20:
        for plan in all_auto_plans:
            plan.calendar_month_total_auto_addition_value = 0
            plan.save()

    for plan in all_auto_plans:
        days_since_last = (now - plan.date_of_last_auto_top_up).days
        if days_since_last >= plan.regular_by_days_interval:
            if plan.calendar_month_total_auto_addition_value + plan.addition_on_interval_by_days_trigger <= plan.monthly_hard_limit_auto_addition_amount:
                plan.organization.balance += plan.addition_on_interval_by_days_trigger
                plan.organization.save()

                TransactionInvoice.objects.create(
                    organization=plan.organization, responsible_user=plan.organization.created_by_user,
                    transaction_type=InvoiceTypesNames.AUTO_TOP_UP,
                    amount_added=plan.addition_on_interval_by_days_trigger,
                    payment_method=AcceptedMethodsOfPaymentNames.CREDIT_CARD,
                )

                plan.date_of_last_auto_top_up = now
                plan.calendar_month_total_auto_addition_value += plan.addition_on_interval_by_days_trigger
                plan.save()
            else:
                reduced_add_amount = (
                    plan.monthly_hard_limit_auto_addition_amount - plan.calendar_month_total_auto_addition_value)

                if reduced_add_amount > 0:
                    plan.organization.balance += reduced_add_amount
                    plan.organization.save()

                    TransactionInvoice.objects.create(
                        organization=plan.organization, responsible_user=plan.organization.created_by_user,
                        transaction_type=InvoiceTypesNames.AUTO_TOP_UP, amount_added=reduced_add_amount,
                        payment_method=AcceptedMethodsOfPaymentNames.CREDIT_CARD,
                    )
                    plan.date_of_last_auto_top_up = now
                    plan.calendar_month_total_auto_addition_value += reduced_add_amount
                    plan.save()
                else:
                    continue
        else:
            continue
    return True
