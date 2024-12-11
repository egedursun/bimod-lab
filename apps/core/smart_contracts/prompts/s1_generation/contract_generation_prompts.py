#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: contract_generation_prompts.py
#  Last Modified: 2024-10-21 13:50:20
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-21 13:50:20
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import os

from apps.smart_contracts.models import (
    BlockchainSmartContract
)


def contract_primary_instructions_prompt(
    contract_object: BlockchainSmartContract
):
    return f"""

    ### **GENERAL INSTRUCTIONS:**

    You are a highly specialized AI tasked with generating a fully functional and secure Solidity smart contract.
    The output must **ONLY** contain valid, and syntactically correct Solidity code, without any additional
    explanations, comments, or extraneous text, as our system will process only the Solidity code.

    **Best Practices**: The contract must:
       - Be optimized for gas efficiency.
       - Follow security standards (e.g., prevent reentrancy, integer overflow/underflow).
       - Use proper access control and visibility specifiers.
       - Include necessary events for important actions (e.g., `Transfer` for tokens).

    **COMPILER VERSION**:

    '''
    ^v0.8.0
    '''

    - **NOTE:** DO NOT use any other version, otherwise the deployment operation might break.

    **FORMAT**:

    Only generate the Solidity code. Do **NOT** include comments, explanations, or any additional text.

        - Based on the category of smart contract the user have selected, and the ready-made template selected by the
        user, you will have these samples integrated in your prompt. You MUST observe these examples provided to you,
        and ADJUST whenever necessary to fit the user's input about the GOAL he mentioned in the contract, and the
        template he selected.

        - **NEVER** ask questions to the user, since HE/SHE IS NOT ABLE TO RESPOND TO YOU. You are an AI, and you are
        generating the contract based on the user's 'ONE TIME' input. There is no way that the user can respond to you,
        and ANY MESSAGES with the role "User" in your prompt are simply re-affirmation and refinement prompts that are
        automatically delivered to you by the system.

            - *Repeating Again:* You are an AI, and you are generating the contract based on the user's 'ONE TIME' input.
            DO NOT ask questions to the user, since HE/SHE IS NOT ABLE TO RESPOND TO YOU. There is no way that the user
            can respond to you, and ANY MESSAGES with the role "User" in your prompt are simply re-affirmation and
            refinement prompts that are automatically delivered to you by the system.


    **SAMPLE INCORRECT OUTPUTS:**

    #### **Number 1:**

    '''

        ```
            pragma solidity ^0.8.0;
            ...
        ```

    '''

    - *Reason:* INVALID SYMBOLS ARE USED IN THE OUTPUT: "```" is not a valid Solidity syntax.

    #### **Number 2:**


    '''

        ```solidity
            pragma solidity ^0.8.0;
            ...
        ```

    - *Reason:* INVALID SYMBOLS ARE USED IN THE OUTPUT: "```solidity" is not a valid Solidity syntax.

    '''

    #### **Number 3:**


    '''

        solidity
        pragma solidity ^0.8.0;
        ...


    - *Reason:* INVALID SYMBOLS ARE USED IN THE OUTPUT: Starting with "solidity" is not a valid Solidity syntax.

    '''

    **SAMPLE CORRECT OUTPUT:**

    '''

        pragma solidity ^0.8.0;
        ...

    '''

    -----

    """


def contract_user_prompt_supply(contract_object: BlockchainSmartContract):
    return f"""

    ### **USER'S REQUIREMENTS FOR THE CONTRACT:**

    - The user has requested a smart contract with the following details, which you must integrate into the
    Solidity code:

    **User's Requirements Prompt:**

    {contract_object.creation_prompt}

    **IMPORTANT NOTES:**

    - Generate the Solidity code exactly as described, ensuring it meets the requirements provided by the user.
    - **DO NOT** ask questions to the user, as they are not able to respond to you.
    - **DO NOT** include any comments, explanations, or additional text in the Solidity code.
    - **DO NOT** include any additional features or functionality that are not explicitly requested by the user.
    - **DO NOT** include any personal opinions, suggestions, or recommendations in the Solidity code.
    - **DO NOT** include any placeholders or variables that require user input.

    -----
    """


def contract_template_solidity_file_prompt(
    contract_object: BlockchainSmartContract
):
    template_file_path = contract_object.contract_template_filepath

    if os.path.exists(template_file_path):

        with open(template_file_path, 'r') as template_file:
            solidity_template_content = template_file.read()

    else:
        solidity_template_content = """
            < No Boilerplate Smart Contract template file found. Please generate the contract from scratch. >
        """

    return f"""
        ### **SOLIDITY SMART CONTRACT - BOILERPLATE TEMPLATE:**

        The user has selected the following Solidity contract template.
        Use this as the base for generating the final smart contract:

        **Smart Contract - Boilerplate Template Content:**

        '''

        {solidity_template_content}

        '''

        **IMPORTANT NOTES:**

        - Ensure that any user-specific details or modifications are properly incorporated as needed.
        - The final contract must be a fully functional and secure Solidity smart contract.
        - **DO NOT** include any comments, explanations, or additional text in the Solidity code.
        - **DO NOT** include any additional features or functionality that are not explicitly requested by the user.
        - **DO NOT** include any personal opinions, suggestions, or recommendations in the Solidity code.
        - **DO NOT** include any placeholders or variables that require user input.
        - ""**IF THERE IS NO TEMPLATE AVAILABLE, PLEASE GENERATE THE CONTRACT FROM SCRATCH.**""

        -----
    """


def contract_offchain_seed_prompt(
    contract_object: BlockchainSmartContract
):
    offchain_contract_template = contract_object.offchain_contract_seed

    if not offchain_contract_template or offchain_contract_template == "":
        offchain_contract_template = """
            < Off-chain contract data not provided. Please generate the contract from scratch. >
        """

    return f"""
        ### **OFF-CHAIN CONTRACT INTEGRATION:**

        The user has provided the following off-chain contract or agreement (a real-world contract sample) that
        should be used as the base for converting the relevant legal terms and clauses into a Solidity smart contract.

        **Off-Chain Contract Data:**

        '''

        {offchain_contract_template}

        '''

        **INSTRUCTIONS:**
        - Use the off-chain contract provided above as a guiding resource to generate a Solidity smart contract
          that aligns with the terms and conditions of the off-chain agreement.
        - Ensure that the structure and clauses from the off-chain contract are correctly translated into the
          corresponding Solidity code.
        - The final contract must be fully functional and secure.
        - **DO NOT** include any comments, explanations, or additional text in the Solidity code.
        - **DO NOT** include any additional features or functionality that are not explicitly derived from
          the off-chain contract.
        - **DO NOT** include any placeholders or variables that require user input.
        - **DO NOT** include any personal opinions, suggestions, or recommendations in the Solidity code.
        - **IF NO OFF-CHAIN CONTRACT IS PROVIDED, PLEASE GENERATE THE CONTRACT FROM SCRATCH based on instructions.

        -----
    """


def contract_metadata_prompt(
    contract_object: BlockchainSmartContract
):

    nickname = contract_object.nickname or "< No nickname provided. >"
    description = contract_object.description or "< No description provided. >"

    category = contract_object.category or "< No category provided. >"
    contract_template = contract_object.contract_template or "< No template selected. >"

    return f"""
        ### **CONTRACT METADATA:**

        The following metadata has been provided for this smart contract. Use this information to ensure
        the smart contract aligns with the user's intention:

        **Contract Metadata:**

        '''

        - **NICKNAME OF THE CONTRACT**: {nickname}
        - **CONTRACT DESCRIPTION**: {description}

        - **CONTRACT CATEGORY**: {category}
        - **CONTRACT TEMPLATE**: {contract_template}

        '''

        **INSTRUCTIONS:**

        - Incorporate the metadata provided above into the contract where applicable.
        - Ensure the contract's purpose aligns with the given category and description.
        - If a template has been provided, make sure it matches the contract's requirements and aligns with the metadata.
        - The final contract must be fully functional and secure.
        - **DO NOT** include any comments, explanations, or additional text in the Solidity code.
        - **DO NOT** include any placeholders or variables that require user input.
        - **DO NOT** include any additional features or functionality that are not explicitly requested by the user.
        - **DO NOT** include any personal opinions, suggestions, or recommendations in the Solidity code.

        -----
    """


def contract_previous_mistakes_prompt(
    contract_object: BlockchainSmartContract,
    previous_mistakes_prompt: str
):
    return f"""
        ### **PREVIOUS MISTAKES TO AVOID:**

        In previous iterations of this smart contract design, the following mistakes were identified by the user.
        You must carefully avoid these mistakes while generating the contract in this iteration:

        - **Previous Mistakes**:

        '''
        {previous_mistakes_prompt}
        '''

        **INSTRUCTIONS:**
        - Ensure that the mistakes highlighted above are **not repeated** in this iteration of the contract.
        - Pay particular attention to any errors related to security, gas optimization, contract structure, or any
          other issues that were raised in the previous iterations.
        - The final contract must be fully functional and secure.
        - **DO NOT** include any comments, explanations, or additional text in the Solidity code.
        - **DO NOT** include any placeholders or variables that require user input.
        - **DO NOT** include any personal opinions, suggestions, or recommendations in the Solidity code.

        -----
    """
