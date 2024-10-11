#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: add_gift_balance_views.py
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

import decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.views import View

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.llm_transaction.models import TransactionInvoice
from apps.llm_transaction.utils import InvoiceTypesNames, AcceptedMethodsOfPaymentNames
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames


class OrganizationView_AddGiftCredits(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - ADD_BALANCE_TO_ORGANIZATION
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_BALANCE_TO_ORGANIZATION):
            messages.error(self.request, "You do not have permission to add balance to organizations.")
            return redirect('llm_transaction:list')
        ##############################

        org_id = kwargs.get('pk')
        user = request.user
        org = get_object_or_404(Organization, id=org_id, users__in=[request.user])
        user = User.objects.get(id=user.id)
        try:
            if user.profile.free_credits != 0:
                free_credits = user.profile.free_credits
                user.profile.free_credits = 0
                user.profile.save()
                user.save()
                org.balance += decimal.Decimal.from_float(free_credits)
                org.save()

                TransactionInvoice.objects.create(
                    organization=org,
                    responsible_user=request.user,
                    transaction_type=InvoiceTypesNames.GIFT_CREDITS,
                    amount_added=decimal.Decimal.from_float(free_credits),
                    payment_method=AcceptedMethodsOfPaymentNames.INTERNAL_TRANSFER,
                )
                messages.success(request, f"Gift credits successfully added to {org.name}.")
            else:
                messages.error(request, "No gift credits available to add.")
        except Exception as e:
            messages.error(request, f"Error adding gift credits: {str(e)}")
        return redirect('llm_transaction:list')
