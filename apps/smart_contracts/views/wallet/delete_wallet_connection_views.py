#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_wallet_connection_views.py
#  Last Modified: 2024-10-19 22:33:50
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-19 22:33:51
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
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.smart_contracts.models import BlockchainWalletConnection
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class SmartContractView_WalletConnectionDelete(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        wallet_connection_id = self.kwargs.get('pk')
        wallet_connection = get_object_or_404(BlockchainWalletConnection, pk=wallet_connection_id)
        context['wallet_connection'] = wallet_connection
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - DELETE_BLOCKCHAIN_WALLET_CONNECTIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_BLOCKCHAIN_WALLET_CONNECTIONS):
            messages.error(self.request, "You do not have permission to delete Blockchain Wallet Connections.")
            return redirect('smart_contracts:wallet_connection_list')
        ##############################

        wallet_connection_id = self.kwargs.get('pk')
        wallet_connection = get_object_or_404(BlockchainWalletConnection, pk=wallet_connection_id)
        wallet_connection.delete()
        logger.info(f'Wallet connection deleted. Wallet_connection_id: {wallet_connection_id}')
        messages.success(request, 'Wallet connection deleted successfully.')
        return redirect('smart_contracts:wallet_connection_list')
