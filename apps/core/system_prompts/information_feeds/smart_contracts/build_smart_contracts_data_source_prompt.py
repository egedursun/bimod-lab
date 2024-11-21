#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: build_smart_contracts_data_source_prompt.py
#  Last Modified: 2024-10-22 00:40:42
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-22 00:40:43
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from apps.assistants.models import Assistant
from apps.smart_contracts.models import BlockchainSmartContract, BlockchainWalletConnection


def build_smart_contracts_data_source_prompt(assistant: Assistant):
    agent_org = assistant.organization
    smart_contracts = BlockchainSmartContract.objects.filter(wallet__organization=agent_org)
    response_prompt = """
        ### **BLOCKCHAIN WALLET CONNECTIONS:**

        '''
    """

    blockchain_wallets = BlockchainWalletConnection.objects.filter(organization=agent_org)
    for i, wallet in enumerate(blockchain_wallets):
        wallet: BlockchainWalletConnection
        response_prompt += f"""
        [Wallet ID: {wallet.id}]
            Nickname: {wallet.nickname}
            Description: {wallet.description or "N/A"}
            Blockchain Type: {wallet.blockchain_type}
            Address: {wallet.wallet_address}
            Balance: {wallet.wallet_balance}
            Balance Last Synced At: {wallet.balance_last_synced_at}

        ---
    """

    response_prompt += """

        ================

        ### **BLOCKCHAIN SMART CONTRACT CONNECTIONS:**

        '''
        """

    for i, smart_contract in enumerate(smart_contracts):
        smart_contract: BlockchainSmartContract
        response_prompt += f"""
        [Smart Contract Data Source ID: {smart_contract.id}]
            Nickname: {smart_contract.nickname}
            Description: {smart_contract.description or "N/A"}
            Category: {smart_contract.category}
            Contract Template: {smart_contract.contract_template or "N/A"}
            Contract Address: {smart_contract.contract_address or "N/A"}
            Contract Summary JSON:
                '''
                {smart_contract.generated_solidity_code_natural_language or "N/A"}
                '''
            Contract ABI (Application Binary Interface):
                '''
                {smart_contract.contract_abi or "N/A"}
                '''
            Contract Args used on Deployment Transaction:
                '''
                {smart_contract.contract_args or "N/A"}
                '''
            Transaction Hash of Deployment: {smart_contract.tx_hash or "N/A"}
            Transaction Receipt: {smart_contract.tx_receipt_raw}

            ***

            Smart Contract's Wallet Information:

            [Wallet ID: {smart_contract.wallet.id}]
                [**More information can be found in the Wallets section above.**]

        ---

        """

    response_prompt += """
        '''

        ---

        #### **NOTE**: These are the Blockchain Smart Contract connections that you have access. Keep these in mind while
        responding to user. If this part is EMPTY, it means that the user has not provided any Smart Contract
        Connections (yet), so you can neglect this part.

        #### **NOTE about Smart Contract Data Source ID**: This is the unique identifier for each Smart Contract
        Connection. You can use this ID to refer to a specific Smart Contract Connection in your responses.

        #### **NOTE ABOUT WALLET**: Each Smart Contract Connection is associated with a Wallet. Wallets are used to
        deploy and interact with Smart Contracts. Wallets have their own unique identifiers, however, you won't need
        to interact with the wallets directly. You are only responsible for the Smart Contracts and you must use
        the Smart Contract Data Source ID to refer to a specific Smart Contract Connection, '''NOT''' the Wallet ID.

            - **REPEATING AGAIN:** You must use the Smart Contract Data Source ID to refer to a specific Smart
            Contract Connection, '''NOT''' the Wallet ID.

        ---

        """

    return response_prompt


def build_lean_smart_contracts_data_source_prompt():
    response_prompt = """
        ### **BLOCKCHAIN SMART CONTRACT CONNECTIONS:**

        '''
        <This data is redacted because you won't need it to serve your instructions.>
        '''

        ---

        #### **NOTE**: These are the Blockchain Smart Contract connections that you have access. Keep these in mind while
        responding to user. If this part is EMPTY, it means that the user has not provided any Smart Contract
        Connections (yet), so you can neglect this part.

        #### **NOTE about Smart Contract Data Source ID**: This is the unique identifier for each Smart Contract
        Connection. You can use this ID to refer to a specific Smart Contract Connection in your responses.

        #### **NOTE ABOUT WALLET**: Each Smart Contract Connection is associated with a Wallet. Wallets are used to
        deploy and interact with Smart Contracts. Wallets have their own unique identifiers, however, you won't need
        to interact with the wallets directly. You are only responsible for the Smart Contracts and you must use
        the Smart Contract Data Source ID to refer to a specific Smart Contract Connection, '''NOT''' the Wallet ID.

            - **REPEATING AGAIN:** You must use the Smart Contract Data Source ID to refer to a specific Smart
            Contract Connection, '''NOT''' the Wallet ID.

        ---

        """

    return response_prompt
