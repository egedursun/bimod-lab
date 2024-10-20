#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: wallet_connection_models.py
#  Last Modified: 2024-10-19 22:28:53
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-19 22:28:54
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

from django.db import models
from django.utils import timezone
from web3 import Web3

from apps.smart_contracts.utils import BLOCKCHAIN_TYPE, DEFAULT_WEI_UNIT
from config import settings

logger = logging.getLogger(__name__)


class BlockchainWalletConnection(models.Model):
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE)
    blockchain_type = models.CharField(max_length=100, choices=BLOCKCHAIN_TYPE)
    nickname = models.CharField(max_length=1000)
    description = models.TextField()

    wallet_address = models.CharField(max_length=16000)
    wallet_private_key = models.CharField(max_length=16000)
    wallet_balance = models.DecimalField(max_digits=20, decimal_places=10, default=0)
    balance_last_synced_at = models.DateTimeField(null=True, blank=True)

    created_by_user = models.ForeignKey('auth.User', on_delete=models.CASCADE,
                                        related_name='blockchain_wallet_connections_created_by_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.organization.name + " - " + self.nickname + ' (' + self.blockchain_type + ')' + ' - ' + self.wallet_address

    class Meta:
        verbose_name = 'Blockchain Wallet Connection'
        verbose_name_plural = 'Blockchain Wallet Connections'
        indexes = [
            models.Index(fields=['organization', 'blockchain_type', 'nickname']),
            models.Index(fields=['wallet_address']),
            models.Index(fields=['created_by_user']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]

    def get_and_sync_wallet_balance(self):
        infura_url = settings.INFURA_URL
        web3 = Web3(Web3.HTTPProvider(infura_url))
        if not web3.is_connected():
            logger.error('Web3 connection failed.')
            return None

        try:
            wei_balance = web3.eth.get_balance(self.wallet_address)
            eth_balance = Web3.from_wei(wei_balance, DEFAULT_WEI_UNIT)
            self.wallet_balance = eth_balance
            self.balance_last_synced_at = timezone.now()
            self.save()
            return eth_balance
        except Exception as e:
            logger.error('Error while getting wallet balance: ' + str(e))
            return None

