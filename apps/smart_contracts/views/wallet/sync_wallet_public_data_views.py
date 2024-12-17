#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: sync_wallet_public_data_views.py
#  Last Modified: 2024-10-20 23:02:57
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-20 23:02:58
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

from django.shortcuts import redirect
from django.utils import timezone
from django.views import View
from web3 import Web3

from apps.smart_contracts.models import (
    BlockchainWalletConnection
)

from apps.smart_contracts.utils import (
    DEFAULT_WEI_UNIT
)

from config import settings

logger = logging.getLogger(__name__)


class SmartContractView_SyncWalletPublicData(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        wallet_id = kwargs.get('pk')

        wallet = BlockchainWalletConnection.objects.get(
            id=wallet_id
        )

        self.sync_wallet_public_data(
            wallet
        )

        return redirect('smart_contracts:wallet_connection_list')

    def sync_wallet_public_data(self, wallet):
        success = self.sync_wallet_balance(
            wallet_connection=wallet
        )

        if success:
            logger.info(f'Wallet public data synced successfully. Wallet_id: {wallet.id}')

        else:
            logger.error(f'Error while syncing wallet public data. Wallet_id: {wallet.id}')

    def sync_wallet_balance(
        self,
        wallet_connection
    ):
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

            return True

        except Exception as e:
            logger.error('Error while syncing wallet balance: ' + str(e))

            return False
