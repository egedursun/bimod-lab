#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#

from apps._services.tools.utils import ToolTypeNames


def build_structured_tool_prompt__custom_api_execution():
    response_prompt = f"""
            **TOOL**: Custom API Execution Tool

            - The Custom API Execution Tool is a tool that allows you to execute custom APIs that are defined in the system.
            These custom APIs can be used to perform various operations such as data retrieval, data processing, and
            other use cases that the use of the API can help answering the users questions. You can use this tool to execute
            custom APIs that are defined in the system and receive the results of the execution. The custom APIs that you
            can execute using this tool are defined by the system administrators and are available for execution in the system,
            and you only need to call these APIs properly by providing the necessary input data and the API ID.

            - The standardized format for the dictionary that you will output to use the Custom API Execution
            Tool is as follows:

            '''
                {{
                    "tool": "{ToolTypeNames.CUSTOM_API_EXECUTOR}",
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

            **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

            **INSTRUCTIONS:** The "custom_api_reference_id" field should be the ID of the custom API that you would like
            to execute. You can find the ID of the custom API that you would like to execute by checking the custom
            APIs that are available in the system. The "endpoint_name" field should be the name of the endpoint that
            you would like to use for the API. You can find the name of the endpoint that you would like to use by
            checking the custom APIs that are available in the system. You must choose an appropriate endpoint that
            could help answering the users question by checking the descriptions of the endpoints and deciding on which
            one would be the most helpful. The "path_values" field should be a dictionary that contains the path
            parameters that you would like to provide to the API. The keys of the dictionary should be the path
            variable names of the endpoint, and the values should be the path values that you would like to provide
            to the API and they must ALWAYS be given in "STRING" format. The "query_values" field should be a
            dictionary that contains the query parameters that you would like to provide to the API. The keys of the
            dictionary should be the query variable names of the endpoint, and the values should be the query values
            that you would like to provide to the API and they must ALWAYS be given in "STRING" format. The
            "body_values" field should be a dictionary that contains the body parameters that you would like to
            provide to the API. The keys of the dictionary should be the body variable names of the endpoint, and the
            values should be the body values that you would like to provide to the API. The body values can be given
            in different formats such as string, integer, float, list, or dictionary, but they must be given in the
            appropriate format that the endpoint expects.

            To use this tool, you need to provide the following field 'VERY CAREFULLY':

            1. For "custom_api_reference_id", provide the ID of the custom API that you would like to execute. You can
            find the ID of the custom API by checking the custom APIs that are available in the system.

            2. For "endpoint_name", provide the name of the endpoint that you would like to use for the API. You can find
            the name of the endpoint by checking the custom APIs that are available in the system.

            3. For "path_values", provide a dictionary that contains the path parameters that you would like to provide to
            the API. The keys of the dictionary should be the path variable names of the endpoint, and the values should be
            the path values that you would like to provide to the API and they must ALWAYS be given in "STRING" format.

            4. For "query_values", provide a dictionary that contains the query parameters that you would like to provide to
            the API. The keys of the dictionary should be the query variable names of the endpoint, and the values should be
            the query values that you would like to provide to the API and they must ALWAYS be given in "STRING" format.

            5. For "body_values", provide a dictionary that contains the body parameters that you would like to provide to
            the API. The keys of the dictionary should be the body variable names of the endpoint, and the values should be
            the body values that you would like to provide to the API. The body values can be given in different formats
            such as string, integer, float, list, or dictionary, but they must be given in the appropriate format that the
            endpoint expects.

            ---

            **IMPORTANT NOTES:**

            **NOTE**: The system will provide you with the results in the next 'assistant' message. This message will
            have the output of the query execution, and you will be expected to take this response and provide an answer
            to the user's question based on the response that you receive, in your own words.
        """
    return response_prompt
