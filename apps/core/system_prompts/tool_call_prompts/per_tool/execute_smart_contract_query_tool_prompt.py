#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: execute_smart_contract_query_tool_prompt.py
#  Last Modified: 2024-11-13 05:16:50
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-13 05:16:50
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from apps.core.tool_calls.utils import ToolCallDescriptorNames

from apps.smart_contracts.utils import (
    SmartContractCategoriesNames,
    SmartContractTemplateNames
)


def build_tool_prompt__execute_smart_contract_generation_query():
    response_prompt = f"""

            ### **TOOL**: Smart Contract Generation Query Tool

            - The Smart Contract Generation Query Tool is a tool you can use to generate smart contracts based on the details
            provided by you along with statements, clauses and certain ingredients you prefer to have within the smart contract.
            The contract will be deployed locally after being generated and then will require the manual confirmation of the
            user to be deployed in the blockchain network. You can use this tool to help users create smart contracts and
            you must understand their requirements very well before attempting to generate the contracts for them. The
            requirements you deliver can be in natural language since the contract generation process will be handled by
            a distinct AI assistant and the only thing you must be very careful about is the format of your tool call since
            this will be critical for the receiver assistant to extract and understand the requirements. After you receive
            a successful response for the contract generation (or no errors have been delivered to you), you can let the
            user know about the success of the generation process and tell them to check their Smart Contracts folder in
            Bimod platform to access the generated contract, and if they like it, they can sign and deploy it to the
            blockchain network.

            - The format for the dictionary you will output to use Smart Contract Generation Query Tool is as follows:

            '''
                {{
                    "tool": "{ToolCallDescriptorNames.EXECUTE_SMART_CONTRACT_GENERATION_QUERY}",
                    "parameters": {{
                        "wallet_id": <integer>,
                        "nickname": "...",
                        "description": "...",
                        "category": "< One of these options: {SmartContractCategoriesNames.as_list()} >",
                        "contract_template": "< One of these options: {SmartContractTemplateNames.Custom.as_list()} >",
                        "creation_prompt": "...",
                        "maximum_gas_limit": 1000000,  #  can be higher or lower based on the contract or user's requests (don't include this comment in your tool call)
                        "gas_price_gwei": 20,  #  can be higher or lower based on the contract or user's requests (don't include this comment in your tool call)
                     }}
                }}
            '''

            ---

            #### **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

            To use this tool, you need to provide following fields 'VERY CAREFULLY':

            - [1] The "wallet_id" field must be the ID of the wallet you are using to deploy the smart contract. This ID will be
            used to identify the wallet you are using to deploy the contract and can be found in the Blockchain Wallet Connections
            folder in Bimod platform.

                **IMPORTANT NOTES:**

                - NEVER put in an invalid wallet ID since this will result in an error and the contract generation process will
                be halted.

                - NEVER put in placeholder values or anything other than an integer value in the wallet ID field.

                - NEVER omit the wallet ID field.

            - [2] The "nickname" field must be the nickname of the smart contract you are generating. This nickname will be used
            to identify the contract in the Smart Contracts folder in Bimod platform.

            - [3] The "description" field must be the description of the smart contract you are generating. This description will
            be used to describe the contract in the Smart Contracts folder in Bimod platform in natural language and can be a
            short explanation about what this contract aims to do.

            - [4] The "category" field must be the category of the smart contract you are generating. This category will be used
            to categorize the contract in the Smart Contracts folder in Bimod platform and can be one of the options provided to you
            without exceptions, so **be very careful** about the category you are selecting since any other category will not be
            accepted by the system.

            - [5] The "contract_template" field must be the contract template of the smart contract you are generating. This template
            will be used to generate the smart contract based on the template you are selecting and can be one of the options provided
            to you without exceptions, so **be very careful** about the template you are selecting since any other template will not be
            accepted by the system.

            - [6] The "creation_prompt" field must be the creation prompt of the smart contract you are generating. This creation prompt
            will be used to generate the smart contract based on the creation prompt you are providing and can be a detailed explanation
            about the contract you are generating, the clauses, the statements, the ingredients and the requirements you are expecting
            to have within the contract. This prompt will be used by a distinct AI assistant to generate and refine the contract
            and all these operations depend on the quality of the creation prompt you are providing.

            - [7] The "maximum_gas_limit" field must be the maximum gas limit of the smart contract you are generating. This gas limit
            will be used to set the maximum gas limit for the contract deployment and can be higher or lower based on the contract or
            user's requests. **Do not include the comment I have shared in the JSON dictionary in your tool call**.

            - [8] The "gas_price_gwei" field must be the gas price in Gwei of the smart contract you are generating. This gas price
            will be used to set the gas price for the contract deployment and can be higher or lower based on the contract or user's
            requests. **Do not include the comment I have shared in the JSON dictionary in your tool call**.

            #### **NOTE**: The system will provide you the information about the generated smart contract in the next 'assistant' message.
            This message will have the relevant data about the contract generation process and can provide you insights for you to
            understand what kind of contract you have recently generated and how it went. You are expected to take in this response,
            and use it to provide a final answer to the user. You can let the user know about the success of the generation process
            and tell them to check their Smart Contracts folder in Bimod platform to access the generated contract, and if they like it,
            they can sign and deploy it to the blockchain network.

            ---

        """
    return response_prompt
