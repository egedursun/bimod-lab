#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: contract_refinement_prompts.py
#  Last Modified: 2024-10-21 13:50:55
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-21 13:50:55
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from apps.smart_contracts.models import (
    BlockchainSmartContract
)


def contract_refinement_primary_instructions(
    contract_object: BlockchainSmartContract
):
    return f"""
        ### **CONTRACT REFINEMENT INSTRUCTIONS:**

        You have already created the first draft of the Solidity smart contract based on the user's input. Now,
        it is time to refine the contract. Your task is to enhance the contract by optimizing its structure, improving
        code clarity, and ensuring adherence to Solidity best practices.

        **INSTRUCTIONS:**

        - Ensure that the contract is as efficient as possible in terms of gas usage.
        - Refactor the code for clarity and modularity, ensuring that the contract is easy to maintain and extend.
        - Review the contract for potential security vulnerabilities, making sure that it adheres to security best
          practices (such as preventing reentrancy and ensuring proper access control).
        - Ensure the use of appropriate visibility specifiers (`public`, `private`, `internal`, `external`) for functions.
        - Verify that all key operations, especially token transfers or other critical operations, have corresponding
          Solidity `event` emitters to improve contract transparency.

        **IMPORTANT NOTES:**

        - The final contract must be fully functional, optimized, and secure.
        - **DO NOT** remove any features or functionality that were requested by the user in the initial draft.
        - **DO NOT** include any comments, explanations, or additional text in the Solidity code.
        - **DO NOT** include any placeholders or variables that require user input.
        - **IF EVERYTHING IS CORRECT**, output the contract as is without any modifications.
        - **IF SOMETHING NEEDS MODIFICATION**, make the necessary changes to enhance the contract and DO NOT share anything else OTHER THAN the updated contract code.

        -----
    """
