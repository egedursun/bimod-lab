#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: list_wallet_connections_views.py
#  Last Modified: 2024-10-19 22:34:16
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-19 22:34:16
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
from django.contrib import messages

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from apps.smart_contracts.models import BlockchainWalletConnection
from apps.organization.models import Organization


class SmartContractView_WalletConnectionList(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_BLOCKCHAIN_WALLET_CONNECTIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_BLOCKCHAIN_WALLET_CONNECTIONS):
            messages.error(self.request, "You do not have permission to list Blockchain Wallet Connections.")
            return context
        ##############################

        context['wallet_connections_by_org'] = self.get_wallet_connections_grouped_by_org()
        return context

    def get_wallet_connections_grouped_by_org(self):
        organizations = Organization.objects.filter(users__in=[self.request.user])
        wallet_connections_by_org = {}

        for org in organizations:
            wallet_connections = BlockchainWalletConnection.objects.filter(organization=org)
            wallet_connections_by_org[org] = wallet_connections

        return wallet_connections_by_org
