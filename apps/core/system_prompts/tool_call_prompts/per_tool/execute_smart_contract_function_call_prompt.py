#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: execute_smart_contract_function_call_prompt.py
#  Last Modified: 2024-10-22 00:30:01
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-22 00:30:02
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
from config.settings import MEDIA_URL


def build_tool_prompt__smart_contract_function_call():
    response_prompt = f"""
            ### **TOOL**: Smart Contract Function Call Execution

            - The Smart Contract Function Call Execution is a tool allows you to execute a function call on a smart
            contract. You can use this tool to execute a function call on a smart contract and get the results of the
            function call. The tool will execute the function call on the smart contract and provide you the results
            of the function call, in the next assistant message.

            - The format for dictionary you will output to use the Smart Contract Function Call Execution tool is as follows:

            '''
                {{
                    "tool": "{ToolCallDescriptorNames.EXECUTE_SMART_CONTRACT_FUNCTION_CALL}",
                    "parameters": {{
                        "smart_contract_id": "...",
                        "function_name": "...",
                        "function_kwargs": {{
                            "some_arg_name": "some_arg_value",
                            "another_arg_name": "another_arg_value"
                        }}
                    }}
                }}
            '''

            #### **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

            #### **INSTRUCTIONS:** The "parameters" field in the dictionary should contain the following fields:

                1. "smart_contract_id": The ID of one of the smart contract connection you have, and more specifically,
                    the one that you would like to execute the function call on.

                2. "function_name": The name of the function you would like to execute on the smart contract. The
                    list of available functions for each of the smart contract connections you have are given to you
                    in your prompt, under Smart Contract Data Source section. You must pick the relevant function name
                    you would like to execute from the list of available functions.

                3. "function_kwargs": These are the arguments the function expects you to provide. These arguments are
                something you can infer from the information that is shared with you under the Smart Contract data
                sources section, such as ABI (Application Binary Interface) of the smart contract, as well as the
                Database fields that is shared with you about the contract detail, such as the function input types,
                return types, etc. **IF THE FUNCTION DOES NOT REQUIRE ANY ARGUMENTS, YOU CAN PUT AN EMPTY DICTIONARY
                INSTEAD OF PROVIDING ANY ARGUMENTS.**

            ---

            - [1] For "smart_contract_id", provide the ID of the smart contract connection you would like to execute
                the function call on. NEVER put a placeholder value here. Always provide the actual ID of the smart
                contract connection you would like to execute the function call on. If you do not have a smart contract
                connection, don't use this tool.

            - [2] For "function_name", provide the name of the function you would like to execute on the smart contract.
                NEVER put a placeholder value here. Always provide the actual name of the function you would like to
                execute on the smart contract. If your smart contract connection does not have any function that can
                be called, don't use this tool (for that smart contract connection).

            - [3] For "function_kwargs", provide the arguments the function expects you to provide. NEVER put a
                placeholder value here. Always provide the actual arguments the function expects you to provide. If the
                function does not require any arguments, you can put an empty dictionary ( {{}} ) instead of providing
                any arguments.

            ---

            - **IMPORTANT NOTES:**

            - **NOTE**: The system will provide you the results in the next 'assistant' message. This message will
            have output of the function call execution, and you will be expected to take this response and
            provide an answer to user's question based on the response you received, in your own words. Think of this
            as an employee of yours that you are instructing to execute a query on a file, and you are expected to take
            the response of this employee and provide an answer to the user's question.

            #### **ABOUT PROVIDING URLS & LINKS:**

                - If you need to provide a direct link to user for reaching files, here is the base
                    URL you need to 'DIRECTLY' append the file path to provide an absolute HTTP URL to file:
                    - {MEDIA_URL}

                - **NEVER, EVER:** provide a 'relative' path to files. Always provide 'absolute' path by appending the
                file path to the base URL.

            ---

        """
    return response_prompt
