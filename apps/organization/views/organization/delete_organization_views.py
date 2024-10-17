#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_organization_views.py
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
import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import DeleteView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.llm_transaction.models import TransactionInvoice
from apps.llm_transaction.utils import InvoiceTypesNames, AcceptedMethodsOfPaymentNames
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


logger = logging.getLogger(__name__)


class OrganizationView_OrganizationDelete(DeleteView, LoginRequiredMixin):
    model = Organization
    context_object_name = 'organization'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user_orgs = Organization.objects.filter(users__in=[self.request.user])
        context['user_organizations'] = user_orgs
        context['user_organizations_count'] = user_orgs.count()
        return context

    def post(self, request, *args, **kwargs):
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - DELETE_ORGANIZATIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_ORGANIZATIONS):
            messages.error(self.request, "You do not have permission to delete organizations.")
            return redirect('organization:list')
        ##############################

        org = self.get_object()
        transfer_org_id = request.POST.get('transfer_organization_id')

        transfer_org = get_object_or_404(Organization, id=transfer_org_id, users__in=[context_user])
        src_org_balance = org.balance
        transfer_org.balance += org.balance
        transfer_org.save()

        TransactionInvoice.objects.create(
            organization=org, responsible_user=context_user, transaction_type=InvoiceTypesNames.TRANSFERRED_CREDITS,
            amount_added=src_org_balance, payment_method=AcceptedMethodsOfPaymentNames.INTERNAL_TRANSFER)
        org.delete()
        logger.info(f"Organization: {org.id} was deleted by User: {context_user.id}.")
        messages.success(request,
                         f'Organization "{org.name}" has been deleted and the balance has been transferred to "{transfer_org.name}".')
        return redirect('organization:list')

    def get_queryset(self):
        context_user = self.request.user
        return Organization.objects.filter(users__in=[context_user])
