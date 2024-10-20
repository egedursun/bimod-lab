#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_soft_all_smart_contracts_views.py
#  Last Modified: 2024-10-19 22:57:42
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-19 22:57:43
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
from django.shortcuts import redirect
from django.views import View

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.smart_contracts.models import BlockchainSmartContract
from apps.user_permissions.utils import PermissionNames

logger = logging.getLogger(__name__)


class SettingsView_DeleteSoftAllSmartContracts(View, LoginRequiredMixin):
    def post(self, request, *args, **kwargs):

        user = request.user
        smart_contracts = BlockchainSmartContract.objects.filter(assistant__organization__users__in=[user]).all()
        confirmation_field = request.POST.get('confirmation', None)
        if confirmation_field != 'CONFIRM SOFT DELETING ALL BLOCKCHAIN SMART CONTRACTS':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM SOFT DELETING ALL BLOCKCHAIN SMART CONTRACTS'.")
            logger.error(f"Invalid confirmation field: {confirmation_field}")
            return redirect('user_settings:settings')

        ##############################
        # PERMISSION CHECK FOR - SOFT_DELETE_SMART_CONTRACTS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.SOFT_DELETE_SMART_CONTRACTS):
            messages.error(self.request, "You do not have permission to soft delete smart contracts.")
            return redirect('user_settings:settings')
        ##############################

        try:
            for contract in smart_contracts:
                contract.delete()
            messages.success(request, "All blockchain smart contracts associated with your account have "
                                      "been deleted.")
            logger.info(f"All blockchain smart contracts associated with User: {user.id} have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting blockchain smart contracts: {e}")
            logger.error(f"Error deleting blockchain smart contracts: {e}")
        return redirect('user_settings:settings')
