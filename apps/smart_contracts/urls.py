#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-10-19 22:22:16
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-19 22:22:17
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
from django.urls import path

from apps.smart_contracts.views import (
    SmartContractView_ContractCreate, SmartContractView_WalletConnectionCreate,
    SmartContractView_WalletConnectionDelete, SmartContractView_WalletConnectionUpdate,
    SmartContractView_WalletConnectionList, SmartContractView_ContractList, SmartContractView_ContractSoftDelete)

app_name = "smart_contracts"

urlpatterns = [
    path('wallet_connection/create/', SmartContractView_WalletConnectionCreate.as_view(
        template_name='smart_contracts/wallet/create_wallet_connection.html'), name='wallet_connection_create'),
    path('wallet_connection/delete/', SmartContractView_WalletConnectionDelete.as_view(
        template_name='smart_contracts/wallet/delete_wallet_connection.html'), name='wallet_connection_delete'),
    path('wallet_connection/update/', SmartContractView_WalletConnectionUpdate.as_view(
        template_name='smart_contracts/wallet/update_wallet_connection.html'), name='wallet_connection_update'),
    path('wallet_connection/list/', SmartContractView_WalletConnectionList.as_view(
        template_name='smart_contracts/wallet/list_wallet_connections.html'), name='wallet_connection_list'),

    path('contract/create/', SmartContractView_ContractCreate.as_view(
        template_name='smart_contracts/contract/create_smart_contract.html'), name='contract_create'),
    path('contract/list/', SmartContractView_ContractList.as_view(
        template_name='smart_contracts/contract/list_smart_contracts.html'), name='contract_list'),
    path('contract/delete/', SmartContractView_ContractSoftDelete.as_view(
        template_name='smart_contracts/contract/soft_delete_smart_contract.html'), name='contract_soft_delete'),
]
