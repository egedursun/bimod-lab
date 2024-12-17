#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: update_wallet_connection_views.py
#  Last Modified: 2024-10-19 22:33:59
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-19 22:33:59
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

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.smart_contracts.utils import (
    DEFAULT_WEI_UNIT
)

from apps.user_permissions.utils import (
    PermissionNames
)

from config import settings
from web_project import TemplateLayout

from django.shortcuts import (
    get_object_or_404,
    redirect
)

from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from web3 import Web3

from apps.smart_contracts.models import (
    BlockchainWalletConnection
)

from apps.organization.models import Organization
from django.views.generic import TemplateView

logger = logging.getLogger(__name__)


class SmartContractView_WalletConnectionUpdate(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        wallet_connection_id = self.kwargs.get('pk')

        wallet_connection = get_object_or_404(
            BlockchainWalletConnection,
            pk=wallet_connection_id
        )

        context['wallet_connection'] = wallet_connection

        context['organizations'] = Organization.objects.filter(
            users__in=[self.request.user]
        )

        context['blockchain_types'] = BlockchainWalletConnection._meta.get_field('blockchain_type').choices

        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - UPDATE_BLOCKCHAIN_WALLET_CONNECTIONS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.UPDATE_BLOCKCHAIN_WALLET_CONNECTIONS
        ):
            messages.error(self.request, "You do not have permission to update Blockchain Wallet Connections.")

            return redirect('smart_contracts:wallet_connection_list')
        ##############################

        wallet_connection_id = self.kwargs.get('pk')

        wallet_connection = get_object_or_404(
            BlockchainWalletConnection,
            pk=wallet_connection_id
        )

        organization_id = request.POST.get('organization')
        nickname = request.POST.get('nickname')
        blockchain_type = request.POST.get('blockchain_type')

        wallet_address = request.POST.get('wallet_address')
        wallet_private_key = request.POST.get('wallet_private_key')
        description = request.POST.get('description')

        if not all(
            [
                organization_id,
                nickname,
                blockchain_type,
                wallet_address,
                wallet_private_key
            ]
        ):
            messages.error(request, 'All fields are required.')

            return redirect(
                reverse(
                    'smart_contracts:wallet_connection_update',
                    kwargs={
                        'pk': wallet_connection_id
                    }
                )
            )

        organization = get_object_or_404(
            Organization,
            id=organization_id
        )

        try:
            wallet_connection.organization = organization
            wallet_connection.nickname = nickname
            wallet_connection.blockchain_type = blockchain_type

            wallet_connection.wallet_address = wallet_address
            wallet_connection.wallet_private_key = wallet_private_key
            wallet_connection.description = description
            wallet_connection.updated_at = timezone.now()

            wallet_connection.save()

            connection_response = self.attempt_wallet_connection(
                wallet_address=wallet_address
            )

            if not connection_response:
                logger.error('Error while connecting to wallet.')
                messages.error(request, 'Error while connecting to wallet, please check your credentials.')

                return redirect('smart_contracts:wallet_connection_create')

            if self.sync_wallet_balance(wallet_connection):
                logger.info('Wallet connection updated and balance synced successfully.')
                messages.success(request, 'Wallet connection updated and balance synced successfully.')

            else:
                logger.warning('Wallet connection updated, but balance sync failed.')
                messages.warning(request, 'Wallet connection updated, but balance sync failed.')

        except Exception as e:
            logger.error(f'An error occurred while updating the wallet connection: {str(e)}')
            messages.error(request, f'An error occurred while updating the wallet connection: {str(e)}')

            return redirect(
                reverse(
                    'smart_contracts:wallet_connection_update',
                    kwargs={
                        'pk': wallet_connection_id
                    }
                )
            )

        return redirect(
            reverse(
                'smart_contracts:wallet_connection_list'
            )
        )

    def attempt_wallet_connection(self, wallet_address: str):
        infura_url = settings.INFURA_URL

        web3 = Web3(
            Web3.HTTPProvider(
                infura_url
            )
        )

        if not web3.is_connected():
            logger.error('Web3 connection failed.')

            return False

        try:
            wei_balance = web3.eth.get_balance(
                wallet_address
            )

            _ = Web3.from_wei(
                wei_balance,
                DEFAULT_WEI_UNIT
            )

            logger.info('Successfully connected to wallet.')

            return True

        except Exception as e:
            logger.error('Error while connecting to wallet: ' + str(e))

            return False

    def sync_wallet_balance(self, wallet_connection):
        infura_url = settings.INFURA_URL

        web3 = Web3(
            Web3.HTTPProvider(
                infura_url
            )
        )

        if not web3.is_connected():
            logger.error('Web3 connection failed.')

            return False

        try:
            wei_balance = web3.eth.get_balance(
                wallet_connection.wallet_address
            )

            eth_balance = Web3.from_wei(
                wei_balance,
                DEFAULT_WEI_UNIT
            )

            wallet_connection.wallet_balance = eth_balance
            wallet_connection.balance_last_synced_at = timezone.now()

            wallet_connection.save()

            logger.info('Wallet balance synced successfully.')

            return True

        except Exception as e:
            logger.error('Error while syncing wallet balance: ' + str(e))

            return False
