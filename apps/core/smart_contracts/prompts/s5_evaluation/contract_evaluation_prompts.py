#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: contract_evaluation_prompts.py
#  Last Modified: 2024-10-21 13:50:32
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-21 13:50:33
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


def contract_final_evaluation_primary_instructions(contract_object: BlockchainSmartContract):
    return f"""
        ### **EVALUATION INSTRUCTIONS:**

        Perform an evaluation of the contract, ensuring that it is fully functional, secure, and ready for deployment
        on the blockchain.

        **INSTRUCTIONS:**
        - Perform a final review of the contract to ensure that all features requested by the user have been implemented
          correctly.
        - Ensure that the contract is secure, following Solidity best practices for security (such as reentrancy protection,
          proper access control, and integer safety).
        - Verify that the contract is optimized for gas efficiency without sacrificing functionality or security.
        - Confirm that all necessary Solidity `event` emitters are in place for key operations, such as transfers or
          ownership changes, to ensure transparency.
        - Check that the contract adheres to the specified Solidity version and follows proper coding standards.

        **IMPORTANT NOTES:**
        - The contract must be fully functional, secure, and optimized for gas usage.
        - **DO NOT** add or remove any features at this stage—focus solely on evaluating the existing functionality
          to ensure it meets all requirements.
        - **DO NOT** include any comments, explanations, or additional text in the Solidity code.
        - **DO NOT** include any placeholders or variables that require user input.

        Once the contract has passed the final evaluation, it is ready for deployment.

        -----
    """


def contract_natural_language_context_explanation_prompt(contract_object: BlockchainSmartContract):
    return f"""
        ### **NATURAL LANGUAGE CONTEXT EXPLANATION:**

        You are tasked with reviewing the content of the generated Solidity smart contract and providing a
        natural language explanation that identifies key details about the contract. Your response must be formatted
        as JSON, and should include the following sections:

        **TOPIC**:
        - Identify the primary purpose or topic of the contract (e.g., token creation, escrow, governance).

        **PROTOCOL DETAILS**:
        - Include any relevant blockchain or protocol-related details (e.g., ERC-20, ERC-721, staking).

        **SUMMARY:**
        - Provide a high-level summary of what the contract does.

        **PARTIES:**
        - Identify the involved parties (e.g., owner, participants, administrators).

        **CLAUSES:**
        - Identify key clauses or conditions within the contract, particularly those relevant to its functionality.

        **FUNCTIONS:**
        - For each function in the contract, capture the following details:

            1. Function name
            2. Description of the function’s purpose (in summary)
            3. Input parameters (name, type, and short explanation)
            4. Return types (if any)
            5. Visibility (public, private, internal, external)
            6. Modifiers (if any)
            7. Payable status (whether the function is `payable`)
            8. State mutability (view, pure, non-payable)

        **CONTRACT ARGUMENTS:**
        - List any arguments or parameters that the contract requires for its operation.
            - For example, for a lending-borrowing contract, this could include borrower address, loan amount, etc.
            - Or, for a token contract, this could include the token name, symbol, and decimals.
            - User is responsible for providing you these details of course, so if the prompt does not include
                these details, you can produce these YOURSELF. But NEVER use placeholders or variables that require
                user input. Also NEVER leave this section empty (if the contract requires arguments).

            - **IMPORTANT NOTE:** In order for the contract to be successfully deployed, YOU MUST provide the field
            names for the contract arguments "AND" the values for these fields. DO NOT leave any mandatory fields
            empty. This mostly depends on the contract type you are working on. For example, _borrower, _amount,
            _duration, _interestRate, etc. ARE MANDATORY most of the time, for most of the lending-borrowing contracts.
            **SO YOU DONT HAVE THE CHANCE** to leave these fields empty. You must provide the values for these fields.
            **REPEATING AGAIN:** DO NOT LEAVE MANDATORY FIELDS EMPTY.

            *Example of correct contract arguments (for a lender-borrower type of contract):*

                ```
                {{
                    "borrower": "0x1234567890abcdef",
                    "amount": 1000,
                    "duration": 30,
                    "interestRate": 5
                }}
                ```

            *Example of INCORRECT contract arguments (for a lender-borrower type of contract):*

                ```
                {{
                    "borrower": "0x123456"
                }}

                Reason of Incorrectness: -> MISSING FIELDS

            -

            *Example of INCORRECT contract arguments (for a lender-borrower type of contract):*

                ```
                {{
                    "borrower": "real address here",
                    "amount": "real value here",
                    "duration": "real value here",
                }}
                ```

                Reason of Incorrectness: -> DO NOT USE PLACEHOLDER VALUES, USE **REAL VALUES**

            -

            *Example of INCORRECT contract arguments (for a lender-borrower type of contract):*

                ```
                {{
                    "borrower": "borrower is the address of the borrower",
                    "amount": "amount is the amount of the loan",
                    "duration": "duration is the duration of the loan",
                    "interestRate": "interestRate is the interest rate of the loan"
                }}
                ```

                Reason of Incorrectness: -> THE GOAL "IS NOT TO EXPLAIN" WHAT THESE FIELDS ARE, BUT TO PROVIDE
                **REAL VALUES** FOR THESE FIELDS.

            -

        ---

        **STRICT OUTPUT FORMAT:**

        Your output MUST BE structured as follows:

        '''

        {{
            "topic": "<Topic of the contract>",
            "protocol_details": "<Protocol information related to the contract>",
            "summary": "<High-level summary of the contract's purpose and functionality>",
            "parties": [
                "<Party 1>",
                "<Party 2>",
                ...
            ],
            "clauses": [
                "<Key clause 1>",
                "<Key clause 2>",
                ...
            ],
            "functions": [
                {{
                    "function_name": "<Name of the function>",
                    "description": "<Purpose of the function>",
                    "input_parameters": [
                        {{
                            "name": "<Parameter name>",
                            "type": "<Parameter type>",
                            "description": "<Description of the parameter>"
                        }},
                        ...
                    ],
                    "return_types": [
                        "<Return type 1>",
                        "<Return type 2>"
                    ],
                    "visibility": "<Visibility (public/private/external/internal)>",
                    "modifiers": [
                        "<Modifier name 1>",
                        "<Modifier name 2>"
                    ],
                    "payable": "<true/false>",
                    "state_mutability": "<view/pure/non-payable>"
                }},
                ...
            ],
            "contract_args": {{
                "<Argument 1 Name>": "<Value for Argument 1>",
                "<Argument 2 Name>": "<Value for Argument 2>",
                ...
            }}
        }}

        '''

        **IMPORTANT NOTES:**

        - Ensure that your explanation is clear, concise, and reflects the content of the Solidity smart contract.
        - You must **ONLY** output the JSON object without any additional text, explanations, or confirmations.
        - **DO NOT** include characters such as `'''` or `"'"`, or any other specifiers that can break the JSON.
        - **DO NOT** output text in the following formats:

            **Invalid Example 1 (with specifiers -> DO NOT USE '```' or "'''" EVER)):**

            '''

            ```
            {{
              "key": "value"
            }}
            ```

            '''

            **Invalid Example 2 (extraneous text):**

            '''

            Here is your JSON:

            ```
            {{
              "key": "value"
            }}
            ```

            '''

            **Invalid Example 3 (invalid character usage -> DO NOT USE '```' or "'''" EVER):**

            '''

            Here is your JSON:

            ```json
            {{
              "key": "value"
            }}
            ```

            '''

            **SAMPLE CORRECT OUTPUT:**

            '''

            {{
                "topic": "Token Creation",
                "protocol_details": "ERC-20",
                ...
            }}

            '''

        - **ONLY** output the raw JSON object in the correct format. **No other text or characters** are allowed.
        - **IF YOU FAIL TO FOLLOW THE STRICT OUTPUT FORMAT, YOUR SUBMISSION WILL FAIL SINCE THE SYSTEM WILL NOT BE ABLE TO PARSE THE OUTPUT.**

        -----

        **THE CONTRACT CODE IS PROVIDED BELOW FOR REFERENCE:**

        '''
        {contract_object.generated_solidity_code}
        '''

        -----

        **THE WALLET INFORMATION FOR YOU TO USE IN YOUR EVALUATION:**

        '''
        [1] Blockchain Type: {contract_object.wallet.blockchain_type}
        [2] Wallet Address: {contract_object.wallet.wallet_address}
        [3] Wallet Private Key: {contract_object.wallet.wallet_private_key}
        [4] Wallet Balance: {contract_object.wallet.wallet_balance}
        [5] Balance Last Synced At: {contract_object.wallet.balance_last_synced_at}
        '''

        -----

        **SMART CONTRACT METADATA:**

        '''
        [1] Nickname: {contract_object.nickname}
        [2] Description: {contract_object.description}
        [3] Category: {contract_object.category}
        [4] Type of Contract Template: {contract_object.contract_template}
        '''

        -----
    """
