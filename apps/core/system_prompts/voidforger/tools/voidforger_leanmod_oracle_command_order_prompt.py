#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: voidforger_leanmod_oracle_command_order_prompt.py
#  Last Modified: 2024-11-16 00:55:01
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-16 00:55:02
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


def build_structured_tool_prompt__leanmod_oracle_command_order_voidforger():
    response_prompt = f"""
        ### **TOOL: LeanMod Oracle Command Order**

        - This allows providing commands and orders to LeanMod oracles. You can use this tool to ask questions,
        request information, or provide commands to LeanMod oracles for them to perform the adequate actions or
        delegate those actions to their underlying assistants in their expert networks to let you go closer to
        the overall objectives you have in mind.

        - The format of dict to use:

        '''
            {{
                "tool": "{ToolCallDescriptorNames.EXECUTE_VOIDFORGER_LEANMOD_ORACLE_COMMAND_ORDER}",
                "parameters": {{
                    "object_id": "...",
                    "query": "...",
                    "image_urls": ["..."],
                    "file_urls": ["..."]
                }}
            }}
        '''

        ---

        #### **INSTRUCTIONS**

        - "object_id" is ID of the oracle search object you want to reach out. You can find IDs of LeanMod oracles by
        searching them within your LeanMod oracle network by using your search tool.
        - "query" is command, order or question you want to deliver to the LeanMod oracle in natural language.
        - "image_urls" is list of URLs of images to provide to the LeanMod oracle if you have any.
        - "file_urls" is list of URLs of files to provide to the LeanMod oracle if you have any.

        The answer will be returned as a response, and it will be in the following format:

        [n] "tool_name": {ToolCallDescriptorNames.EXECUTE_VOIDFORGER_LEANMOD_ORACLE_COMMAND_ORDER},
            [na.] "tool_response": <sample response>,
            [ib.] "file_uris": ["...", "..."],
            [ic.] "image_uris": ["...", "..."]

        ---
    """
    return response_prompt
