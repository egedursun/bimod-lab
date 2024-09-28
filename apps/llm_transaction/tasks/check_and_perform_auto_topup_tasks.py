from celery import shared_task
from django.utils import timezone

from apps.llm_transaction.models import AutoBalanceTopUpModel, TransactionInvoice
from apps.llm_transaction.utils import InvoiceTypesNames, PaymentMethodsNames


@shared_task
def check_and_perform_auto_top_up():
    now = timezone.now()
    auto_top_up_plans = AutoBalanceTopUpModel.objects.filter(on_interval_by_days_trigger=True)
    # check if the start of the month, if so reset the calendar month total for all plans
    if now.day == 20:
        for plan in auto_top_up_plans:
            plan.calendar_month_total_auto_addition_value = 0
            plan.save()
        print("Calendar month totals reset for all auto top-up plans")

    for plan in auto_top_up_plans:
        days_since_last_top_up = (now - plan.date_of_last_auto_top_up).days
        if days_since_last_top_up >= plan.regular_by_days_interval:
            if plan.calendar_month_total_auto_addition_value + plan.addition_on_interval_by_days_trigger <= plan.monthly_hard_limit_auto_addition_amount:
                # Perform the top-up
                plan.organization.balance += plan.addition_on_interval_by_days_trigger
                plan.organization.save()

                ############################################
                # Create the invoice for the transaction
                TransactionInvoice.objects.create(
                    organization=plan.organization,
                    responsible_user=plan.organization.created_by_user,
                    transaction_type=InvoiceTypesNames.AUTO_TOP_UP,
                    amount_added=plan.addition_on_interval_by_days_trigger,
                    payment_method=PaymentMethodsNames.CREDIT_CARD,
                )
                ############################################

                # Update the last top-up time and calendar month total
                plan.date_of_last_auto_top_up = now
                plan.calendar_month_total_auto_addition_value += plan.addition_on_interval_by_days_trigger
                plan.save()
            else:
                # If the hard limit is reached, subtract the excess from the total
                reduced_addition_amount = (
                    plan.monthly_hard_limit_auto_addition_amount - plan.calendar_month_total_auto_addition_value)
                # Perform the top-up if there is still a balance that can be added
                if reduced_addition_amount > 0:
                    # Perform the top-up
                    plan.organization.balance += reduced_addition_amount
                    plan.organization.save()

                    ############################################
                    # Create the invoice for the transaction
                    TransactionInvoice.objects.create(
                        organization=plan.organization,
                        responsible_user=plan.organization.created_by_user,
                        transaction_type=InvoiceTypesNames.AUTO_TOP_UP,
                        amount_added=reduced_addition_amount,
                        payment_method=PaymentMethodsNames.CREDIT_CARD,
                    )
                    ############################################

                    # Update the last top-up time and calendar month total
                    plan.date_of_last_auto_top_up = now
                    plan.calendar_month_total_auto_addition_value += reduced_addition_amount
                    plan.save()
                else:
                    # If the reduced addition amount is 0, do nothing
                    print("Hard limit reached, no top-up performed for organization: ", plan.organization)
                    continue
        else:
            print("Days since last top-up is less than the interval for organization: ", plan.organization)
            continue
    return True
