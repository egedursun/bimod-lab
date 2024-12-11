#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: build_custom_code_execution_tool_prompt.py
#  Last Modified: 2024-10-05 02:25:59
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:35
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from apps.core.tool_calls.utils import (
    ToolCallDescriptorNames
)


def build_tool_prompt__execute_code():
    response_prompt = f"""
            ### **TOOL**: Custom Function Execution Tool

            - The Custom Function Execution Tool is a tool allows you to execute custom functions that are
            defined in the system. These custom functions can be used to perform various operations such as
            data processing, data analysis, data transformation, and more. You can use this to execute custom
            functions and receive the results of the execution. The custom functions you can execute using this tool
            are defined by system administrators and are available for execution, and you only need to call these
            functions properly by providing the necessary input data and function ID.

            - The format for dictionary you will output to use Custom Function Execution Tool is as follows:

            '''
                {{
                    "tool": "{ToolCallDescriptorNames.EXECUTE_CUSTOM_FUNCTION}",
                    "parameters": {{
                        "custom_function_reference_id": "...",
                        "input_data": {{
                            "input_variable_name": "input_variable_value_string",
                            "input_variable_name": 284.32948,
                            "input_variable_name": [1, 2, 3, 4, 5],
                            "input_variable_name": {{
                                "dict_variable_sample": "value",
                                "dict_variable_sample": 284.32948,
                                ...
                            }}
                            ...
                        }}
                    }}
                }}
            '''

            ---

            #### **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

            #### **INSTRUCTIONS:** The "custom_function_reference_id" should be the ID of the custom function that you
            need to execute. You can find ID of the custom function by checking the custom functions that are available
            for you. The "input_data" should be a dict that contains input data to provide to custom function. The
            input data must be provided in dict format, where the keys are input variable names, and the values are the
            input values to provide to custom function.

            To use this tool, you need to provide the following fields 'VERY CAREFULLY':

            - [1] For "custom_function_reference_id", provide ID of the custom function you need to execute. You can
            find the ID of custom function by checking the custom functions that are available for you.

            - [2] For "input_data", provide a dict containing input data to provide to custom function. The keys of
            the dict must be the input variable names, and the values must be the input values to provide to the
            custom function.

            ---

            - **NOTE**: The system will provide you the results in the next 'assistant' message. This message will
            have the output of the execution, and you will be expected to take this response and provide an answer
            to user's question based on the response you receive, in your own words.

            ---
        """

    return response_prompt
