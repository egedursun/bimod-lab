#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: add_balance_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:40
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import decimal
import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.llm_transaction.models import TransactionInvoice
from apps.llm_transaction.utils import InvoiceTypesNames, AcceptedMethodsOfPaymentNames
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from auth.models import PromoCode


logger = logging.getLogger(__name__)


class OrganizationView_AddBalanceCredits(TemplateView, LoginRequiredMixin):
    def post(self, request, *args, **kwargs):
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - ADD_BALANCE_TO_ORGANIZATION
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_BALANCE_TO_ORGANIZATION):
            messages.error(self.request, "You do not have permission to add balance to organizations.")
            return redirect('llm_transaction:list')
        ##############################

        org_id = request.POST.get('org_id')
        org = get_object_or_404(Organization, id=org_id, users__in=[context_user])
        topup_amount = request.POST.get('topup_amount')
        promo_code = request.POST.get('promo_code')
        if float(topup_amount) <= 0:
            logger.error(f"User: {context_user.id} tried to top up with an invalid amount: {topup_amount}")
            messages.error(request, 'Top up amount must be greater than zero.')
            return redirect('llm_transaction:list')

        bonus_pct_referrer, bonus_pct_referee = 0, 0
        promo_code = PromoCode.objects.filter(code=promo_code).first()
        if promo_code is None:
            bonus_pct_referee = 0
        else:
            referrer = promo_code.user
            if promo_code.current_referrals + 1 > promo_code.max_referral_limit:
                promo_code.is_active = False
                promo_code.save()
            else:
                promo_code.current_referrals += 1
                bonus_pct_referrer = promo_code.bonus_percentage_referrer
                bonus_pct_referee = promo_code.bonus_percentage_referee
                promo_code.save()
                referrer_organization = Organization.objects.filter(users__in=[referrer]).first()
                referrer_organization.balance += decimal.Decimal.from_float(
                    float(float(topup_amount) * ((bonus_pct_referrer) / 100)))
                referrer_organization.save()

                TransactionInvoice.objects.create(
                    organization=referrer_organization,
                    responsible_user=bonus_pct_referrer,
                    transaction_type=InvoiceTypesNames.GIFT_CREDITS,
                    amount_added=decimal.Decimal.from_float(
                        float(float(topup_amount) * ((bonus_pct_referrer) / 100))),
                    payment_method=AcceptedMethodsOfPaymentNames.INTERNAL_TRANSFER,
                )
        try:
            topup_amount = float(topup_amount)
            topup_amount_without_bonus = topup_amount
            topup_amount += float(float(topup_amount) * (bonus_pct_referee) / 100)
            org.balance += decimal.Decimal.from_float(topup_amount)
            org.save()

            TransactionInvoice.objects.create(
                organization=org, responsible_user=context_user, transaction_type=InvoiceTypesNames.TOP_UP,
                amount_added=topup_amount_without_bonus, payment_method=AcceptedMethodsOfPaymentNames.CREDIT_CARD)

            if topup_amount_without_bonus != topup_amount:
                TransactionInvoice.objects.create(
                    organization=org, responsible_user=context_user, transaction_type=InvoiceTypesNames.GIFT_CREDITS,
                    amount_added=decimal.Decimal.from_float(
                        float(float(topup_amount) * ((bonus_pct_referee) / 100)) - topup_amount_without_bonus),
                    payment_method=AcceptedMethodsOfPaymentNames.INTERNAL_TRANSFER,
                )
            logger.info(f"User: {context_user.id} added ${topup_amount} to Organization: {org.id}.")
            messages.success(request, f'Credits successfully added. New balance: ${org.balance}')
        except ValueError:
            logger.error(f"User: {context_user.id} tried to top up with an invalid amount: {topup_amount}")
            messages.error(request, 'Invalid amount entered. Please enter a valid number.')
        return redirect('llm_transaction:list')
