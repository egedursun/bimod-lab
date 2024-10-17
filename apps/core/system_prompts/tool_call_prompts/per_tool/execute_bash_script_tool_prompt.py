#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
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
#   For permission inquiries, please contact: admin@Bimod.io.
#


from apps.core.tool_calls.utils import ToolCallDescriptorNames


def build_tool_prompt__execute_bash_script():
    response_prompt = f"""
            ### **TOOL**: Custom Script Content Retrieval Tool

            - The Custom Script Content Retrieval Tool is a tool allows you to retrieve content of custom scripts
            that are defined. This tool helps you retrieve the content of the scripts that are available for you, and
            then, you can utilize these by putting them in a file within e.g. SSH file systems, or by running them
            in the sandbox, or by using them in other ways you need to use them. The scripts you can retrieve using
            this tool are defined by system administrators and are available for retrieval, and you only need to call
            these scripts properly by providing their unique script ID.

            - The format for the dictionary you will output to use Custom Script Content Retrieval Tool is as follows:

            '''
                {{
                    "tool": "{ToolCallDescriptorNames.EXECUTE_CUSTOM_SCRIPT}",
                    "parameters": {{
                        "custom_script_reference_id": "...",
                    }}
                }}
            '''

            #### **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

            #### **INSTRUCTIONS:** The "custom_script_reference_id" should be the ID of custom script you would
            like to retrieve the content. You can find the ID of the custom script by checking the custom scripts
            that are available in the system.

            To use this tool, you need to provide the following fields 'VERY CAREFULLY':

            - [1] For "custom_script_reference_id", provide the ID of custom script you would like to retrieve the
            content.

            ---

            #### **IMPORTANT NOTES:**

            #### **NOTE**: The system will provide you the results in the next 'assistant' message. This message will
            have the output of the execution, and you will be expected to take this response and provide an answer
            to user's question, in your own words.

            ---
        """
    return response_prompt
