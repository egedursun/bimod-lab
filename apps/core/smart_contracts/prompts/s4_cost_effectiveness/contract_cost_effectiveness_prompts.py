#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: contract_cost_effectiveness_prompts.py
#  Last Modified: 2024-10-21 13:50:44
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-21 13:50:45
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
from apps.smart_contracts.models import BlockchainSmartContract


def contract_cost_effectiveness_primary_instructions(contract_object: BlockchainSmartContract):
    return f"""
        ### **COST EFFECTIVENESS INSTRUCTIONS:**

        Optimize the contract for cost-effectiveness. This involves minimizing gas consumption and improving the
        efficiency of the contract's operations, while maintaining all the required functionality.

        **INSTRUCTIONS:**

        - Identify and optimize any gas-intensive operations, such as loops, external calls, and storage access.
        - Use gas-efficient data types and structures (e.g., prefer `uint256` over smaller integer types to avoid implicit
          conversions that increase gas usage).
        - Minimize the use of storage variables where possible by using memory variables or recalculating values within the
          same transaction to reduce storage access costs.
        - Ensure that functions and modifiers are used efficiently, and remove any redundant operations or computations
          that can increase gas costs.
        - Check for opportunities to reduce the size of the contract by consolidating functionality or using libraries.

        **IMPORTANT NOTES:**

        - The contract must remain fully functional and maintain all the requested features.
        - **DO NOT** remove any critical functionality or features in the name of optimization—focus purely on improving
          gas efficiency without altering the contract's logic or purpose.
        - **DO NOT** include any comments, explanations, or additional text in the Solidity code.
        - **DO NOT** include any placeholders or variables that require user input.
        - **IF EVERYTHING IS CORRECT**, output the contract as is without any modifications.
        - **IF SOMETHING NEEDS MODIFICATION**, make the necessary changes to enhance the contract and DO NOT share anything else OTHER THAN the updated contract code.

        -----
    """
