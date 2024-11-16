#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: voidforger_leanmod_oracle_search_prompt.py
#  Last Modified: 2024-11-16 00:54:40
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-16 00:54:41
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


def build_structured_tool_prompt__leanmod_oracle_search_voidforger():
    response_prompt = f"""
        ### **TOOL: LeanMod Oracle Search Tool**

        - This tool allows you to search through the LeanMod oracle assistants you have access to. You can use this tool
        to find out which LeanMod oracle can be the best fit for the actions you want to perform. This way, you can also
        discover the IDs of those relevant LeanMod oracles and therefore be able to order them commands by using these IDs.

        - To use this tool, you must provide a query to search with the LeanMod oracles. Your query will be searched
        within the fields of the LeanMod oracles, which contain:
            i. Assistant Name: The name of the LeanMod oracle assistant.
            ii. Assistant Description: The description of the LeanMod oracle assistant.
            iii. Data Sources: The data sources the LeanMod oracle assistant is connected to.
                a. Expert Networks: The expert networks the LeanMod oracle assistant is connected to, in other words
                the underlying complex assistants / teams the LeanMod oracle is capable of commanding.
                    1. Name of the Expert Network: The name of the expert network.
                    2. Description of the Expert Network: The description of the expert network.
                    3. Network Assistants: The references of underlying complex Assistants within that expert network.
                        x. Assistant Name: The name of the underlying complex assistant.
                        xx. Assistant Description: The description of the underlying complex assistant.

        -----

        - The format of dict to use for searching the LeanMod Oracles is as follows:

        '''
            {{
                "tool": "{ToolCallDescriptorNames.EXECUTE_VOIDFORGER_LEANMOD_ORACLE_SEARCH_QUERY}",
                "parameters": {{
                    "query": "<your search query here>"
                }}
            }}
        '''

        ---

        #### **INSTRUCTIONS**

        - "query" is the field where you will provide the search query to search within the LeanMod Oracles.

        The answer will be returned as a response, and it will be in the following format:

        [n] "tool_name": {ToolCallDescriptorNames.EXECUTE_VOIDFORGER_LEANMOD_ORACLE_SEARCH_QUERY},
            [na.] "tool_response": <sample response>,
            [ib.] "file_uris": ["...", "..."],
            [ic.] "image_uris": ["...", "..."]

        ---
    """
    return response_prompt
