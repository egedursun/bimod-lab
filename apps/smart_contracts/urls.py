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
    SmartContractView_WalletConnectionList, SmartContractView_ContractList, SmartContractView_ContractSoftDelete,
    SmartContractView_SyncWalletPublicData, SmartContractView_ContractGenerate,
    SmartContractView_ContractUpdateDeployStatus, SmartContractView_ConnectAssistantToSmartContract,
    SmartContractView_AssistantConnectionDelete)

app_name = "smart_contracts"

urlpatterns = [
    path('wallet_connection/create/', SmartContractView_WalletConnectionCreate.as_view(
        template_name='smart_contracts/wallet/create_wallet_connection.html'), name='wallet_connection_create'),
    path('wallet_connection/delete/<int:pk>/', SmartContractView_WalletConnectionDelete.as_view(
        template_name='smart_contracts/wallet/delete_wallet_connection.html'), name='wallet_connection_delete'),
    path('wallet_connection/update/<int:pk>/', SmartContractView_WalletConnectionUpdate.as_view(
        template_name='smart_contracts/wallet/update_wallet_connection.html'), name='wallet_connection_update'),
    path('wallet_connection/list/', SmartContractView_WalletConnectionList.as_view(
        template_name='smart_contracts/wallet/list_wallet_connections.html'), name='wallet_connection_list'),
    path('wallet_connection/sync/<int:pk>/', SmartContractView_SyncWalletPublicData.as_view(),
         name='wallet_connection_sync'),

    path('contract/create/', SmartContractView_ContractCreate.as_view(
        template_name='smart_contracts/contract/create_smart_contract.html'), name='contract_create'),
    path('contract/list/', SmartContractView_ContractList.as_view(
        template_name='smart_contracts/contract/list_smart_contracts.html'), name='contract_list'),
    path('contract/delete/<int:pk>/', SmartContractView_ContractSoftDelete.as_view(
        template_name='smart_contracts/contract/soft_delete_smart_contract.html'), name='contract_soft_delete'),
    path('contract/generate/<int:pk>/', SmartContractView_ContractGenerate.as_view(
        template_name='smart_contracts/contract/generate_smart_contract.html'), name='contract_generate'),
    path('contract/update_deploy_status/<int:pk>/', SmartContractView_ContractUpdateDeployStatus.as_view(),
         name='contract_update_deploy_status'),

    # Connect Assistant to Smart Contract
    path("connect/assistant/", SmartContractView_ConnectAssistantToSmartContract.as_view(
        template_name="smart_contracts/connect_assistant/connect_assistant_to_contract.html",
    ), name="connect_assistant"),
    path("disconnect/assistant/<int:pk>/", SmartContractView_AssistantConnectionDelete.as_view(),
         name="disconnect_assistant"),
]
