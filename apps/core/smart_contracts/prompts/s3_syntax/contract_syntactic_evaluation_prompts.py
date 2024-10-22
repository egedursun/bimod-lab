#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: contract_syntactic_evaluation_prompts.py
#  Last Modified: 2024-10-21 13:51:09
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-21 13:51:09
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


def contract_syntactic_check_primary_instructions(contract_object: BlockchainSmartContract):
    return f"""
        ### **SYNTACTIC CHECK INSTRUCTIONS:**

        Perform a thorough syntactic check of the entire contract. Ensure that the code is free of any syntax errors
        and is fully compliant with the Solidity compiler requirements.

        **INSTRUCTIONS:**

        - Carefully review the contract for any syntax errors or issues that would prevent the contract from compiling.
        - Verify that all Solidity keywords, operators, and declarations are used correctly.
        - Ensure the contract adheres to the proper Solidity version, specifically using the version declared in the
          `pragma solidity` directive.
        - Ensure the correct use of data types, function declarations, modifiers, and state variables in the contract.
        - Confirm that all control structures (e.g., `if`, `else`, `for`, `while`) are used correctly.

        **IMPORTANT NOTES:**

        - The contract must be fully syntactically correct and free of errors.
        - **DO NOT** add or remove any features, logic, or functionality in this step—focus solely on the syntax.
        - **DO NOT** include any comments, explanations, or additional text in the Solidity code.
        - **DO NOT** include any placeholders or variables that require user input.
        - **IF EVERYTHING IS CORRECT**, output the contract as is without any modifications.
        - **IF SOMETHING NEEDS MODIFICATION**, make the necessary changes to enhance the contract and DO NOT share anything else OTHER THAN the updated contract code.

        -----
    """
