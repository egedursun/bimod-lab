#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: wallet_connection_admin.py
#  Last Modified: 2024-10-19 22:29:40
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-19 22:29:40
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.contrib import admin

from apps.smart_contracts.models import BlockchainWalletConnection
from apps.smart_contracts.utils import BLOCKCHAIN_WALLET_CONNECTION_ADMIN_LIST, \
    BLOCKCHAIN_WALLET_CONNECTION_ADMIN_FILTER, BLOCKCHAIN_WALLET_CONNECTION_ADMIN_SEARCH


@admin.register(BlockchainWalletConnection)
class BlockchainWalletConnectionAdmin(admin.ModelAdmin):
    list_display = BLOCKCHAIN_WALLET_CONNECTION_ADMIN_LIST
    list_filter = BLOCKCHAIN_WALLET_CONNECTION_ADMIN_FILTER
    search_fields = BLOCKCHAIN_WALLET_CONNECTION_ADMIN_SEARCH
    ordering = ('-created_at',)
