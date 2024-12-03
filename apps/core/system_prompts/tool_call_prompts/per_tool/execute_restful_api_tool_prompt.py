#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: build_custom_api_execution_tool_prompt.py
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

from apps.core.tool_calls.utils import ToolCallDescriptorNames


def build_tool_prompt__execute_restful_api():
    response_prompt = f"""
            ### **TOOL**: Custom API Execution Tool

            - The Custom API Execution Tool is a tool allows you to execute custom APIs that are defined for you.
            These custom APIs can be used to perform various operations such as data retrieval, data processing, and
            other use cases that the use of the API can help answering users questions. You can use this to execute
            custom APIs and receive the results of the execution. The custom APIs you can execute using this tool
            are defined by the system administrators, and you only need to call these APIs properly by providing
            necessary input data and API ID.

            - The format for dictionary you will output to use the Custom API Execution Tool is as follows:

            '''
                {{
                    "tool": "{ToolCallDescriptorNames.EXECUTE_CUSTOM_API}",
                    "parameters": {{
                        "custom_api_reference_id": "...",
                        "endpoint_name": "Any Endpoint Name Defined in your Custom API Tools",
                        "path_values": {{
                            "path_variable_name": "path_variable_value_always_give_a_string",
                            "another_path_variable_name": "another_path_variable_value_always_give_a_string",
                        }},
                        "query_values": {{
                            "query_variable_name": "query_variable_value_always_give_a_string",
                            "another_query_variable_name": "another_query_variable_value_always_give_a_string",
                        }},
                        "body_values": {{
                            "body_variable_name": "body_variable_value",
                            "another_body_variable_name": "another_body_variable_value",
                            "list_body_variable_name": [1, 2, 3, 4, 5],
                            "dict_body_variable_name": {{
                                "dict_variable_sample": "value",
                                "dict_variable_sample": 284.32948,
                                ...
                            }}
                        }}
                    }}
                }}
            '''

            ---

            #### **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

            #### **INSTRUCTIONS:** The "custom_api_reference_id" must be the ID of the custom API you need to execute.
            You can find ID of the custom API that you need to execute by checking custom APIs that are available
            in the system. The "endpoint_name" must be the name of the endpoint you need to use. You can find the name
            of the endpoint by checking the custom APIs as well. You must choose an appropriate endpoint that can
            help answering user's question by checking descriptions of endpoints and deciding on which one would be
            the most helpful. The "path_values" must be a dict containing the path parameters to provide to the API.
            The keys of the dict must be the path variable names of the endpoint, and the values must be the path
            values that you would like to provide to the API and they must ALWAYS be given in "STRING" format. The
            "query_values" must be a dict containing the query parameters to provide to the API. The keys of the
            dict must be the query variable names of the endpoint, and the values must be the query values to provide
            to the API and they must ALWAYS be given in "STRING" format. The "body_values" must be a dict containing
            the body parameters to provide to the API. The keys of the dict must be the body variable names of the
            endpoint, and the values must be the body values to provide to the API. The body values can be given in
            different formats such as string, integer, float, list, or dict, but they must be given in the appropriate
            format that the endpoint expects.

            To use this, you need to provide following fields 'VERY CAREFULLY':

            - [1] For "custom_api_reference_id", provide ID of the custom API that you need to execute. You can
            find the ID of custom API by checking the custom APIs that are available in the system.

            - [2] For "endpoint_name", provide name of the endpoint that you need to use.

            - [3] For "path_values", provide a dict containing path parameters that you would like to
            provide to the API. The keys of the dict must be path variable names of the endpoint, and values must be
            path values that you need to provide, and they must ALWAYS be given in "STRING" format.

            - [4] For "query_values", provide a dict containing query parameters that you need to provide to
            the API. The keys of the dict must be query variable names, and values must be query values you need to
            provide, and they must ALWAYS be given in "STRING" format.

            - [5] For "body_values", provide a dict containing body parameters you need to provide to the API. The
            keys of the dict must be body variable names of the endpoint, and values must be body values you need to
            provide to API. The body values can be given in different formats such as string, integer, float, list, or
            dict, but they must be given in appropriate format that the endpoint expects.

            ---

            - **IMPORTANT NOTES:**

            - **NOTE**: The system will provide you the results in next 'assistant' message. This message will have
            the output of execution, and you will be expected to take this response and provide an answer to user's
            question based on response that you receive, in your own words.

            ---
        """
    return response_prompt
