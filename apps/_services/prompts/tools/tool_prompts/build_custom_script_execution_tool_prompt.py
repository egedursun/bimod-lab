#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: build_custom_script_execution_tool_prompt.py
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


def build_structured_tool_prompt__custom_script_content_retrieval():
    response_prompt = f"""
            **TOOL**: Custom Script Content Retrieval Tool

            - The Custom Script Content Retrieval Tool is a tool that allows you to retrieve the content of custom scripts
            that are defined in the system. This tool will help you retrieve the content of the custom scripts that are
            available in the system and then you can utilize these scripts by yourself by putting them in a file within
            file systems, or by running them in the system, or by using them in any other way that you would like to use
            them. The custom scripts that you can retrieve using this tool are defined by the system administrators and
            are available for retrieval in the system, and you only need to call these scripts properly by providing
            the script ID.

            - The standardized format for the dictionary that you will output to use the Custom Script Content Retrieval
            Tool is as follows:

            '''
                {{
                    "tool": "{ToolTypeNames.CUSTOM_SCRIPT_CONTENT_RETRIEVAL}",
                    "parameters": {{
                        "custom_script_reference_id": "...",
                    }}
                }}
            '''

            **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

            **INSTRUCTIONS:** The "custom_script_reference_id" field should be the ID of the custom script that you would
            like to retrieve the content of. You can find the ID of the custom script that you would like to retrieve the
            content of by checking the custom scripts that are available in the system.

            To use this tool, you need to provide the following field 'VERY CAREFULLY':

            1. For "custom_script_reference_id", provide the ID of the custom script that you would like to retrieve the
            content of. You can find the ID of the custom script by checking the custom scripts that are available in the
            system.

            ---

            **IMPORTANT NOTES:**

            **NOTE**: The system will provide you with the results in the next 'assistant' message. This message will
            have the output of the query execution, and you will be expected to take this response and provide an answer
            to the user's question based on the response that you receive, in your own words.
        """
    return response_prompt
