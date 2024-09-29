#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: transfer_balance_views.py
#  Last Modified: 2024-09-28 15:44:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:08:01
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

import decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views import View

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.llm_transaction.models import TransactionInvoice
from apps.llm_transaction.utils import InvoiceTypesNames, PaymentMethodsNames
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames


class OrganizationBalanceTransferView(LoginRequiredMixin, View):
    """
    Handles the transfer of balance between two organizations.

    This view allows users to transfer a specified amount of balance from one of their organizations to another. It ensures that the transfer amount is valid and that the user has sufficient balance in the source organization.

    Methods:
        post(self, request, *args, **kwargs): Handles the balance transfer process, including validation and updating the balances of the source and destination organizations.
    """

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - TRANSFER_BALANCE_BETWEEN_ORGANIZATIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.TRANSFER_BALANCE_BETWEEN_ORGANIZATIONS):
            messages.error(self.request, "You do not have permission to transfer balance between organizations.")
            return redirect('llm_transaction:list')
        ##############################

        source_org_id = request.POST.get('source_org')
        destination_org_id = request.POST.get('destination_org')
        transfer_amount = request.POST.get('transfer_amount')
        if transfer_amount is None:
            messages.error(request, "Invalid transfer amount.")
            return redirect('llm_transaction:list')
        try:
            transfer_amount = decimal.Decimal(transfer_amount)
        except decimal.InvalidOperation:
            messages.error(request, "Invalid transfer amount.")
            return redirect('llm_transaction:list')
        if transfer_amount <= 0:
            messages.error(request, "Transfer amount must be greater than zero.")
            return redirect('llm_transaction:list')
        if source_org_id == destination_org_id:
            messages.error(request, "Source and destination organizations cannot be the same.")
            return redirect('llm_transaction:list')

        source_org = get_object_or_404(Organization, id=source_org_id, users__in=[request.user])
        destination_org = get_object_or_404(Organization, id=destination_org_id, users__in=[request.user])
        if source_org.balance < transfer_amount:
            messages.error(request, "Insufficient balance in the source organization.")
            return redirect('llm_transaction:list')

        source_org.balance -= transfer_amount
        destination_org.balance += transfer_amount
        source_org.save()
        destination_org.save()

        ############################################
        # Create the invoice for the transaction
        TransactionInvoice.objects.create(
            organization=destination_org,
            responsible_user=request.user,
            transaction_type=InvoiceTypesNames.TRANSFERRED_CREDITS,
            amount_added=transfer_amount,
            payment_method=PaymentMethodsNames.INTERNAL_TRANSFER,
        )
        ############################################

        messages.success(request,
                         f"${transfer_amount} successfully transferred from {source_org.name} to {destination_org.name}.")
        return redirect('llm_transaction:list')
