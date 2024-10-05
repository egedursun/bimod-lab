#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: leanmod_tools_expert_networks_query_prompt.py
#  Last Modified: 2024-09-28 22:17:13
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:34
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: leanmod_tools_expert_networks_query_prompt.py
#  Last Modified: 2024-09-28 00:42:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:10:51
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from apps._services.tools.utils import ToolTypeNames


def build_structured_tool_prompt__expert_network_query_execution_leanmod():
    response_prompt = f"""
                TOOL: Expert Network Query Call

                - This allows consulting to expert networks. If data is not enough to respond, you can check network
                descriptions + instructions of assistants to see if they can answer.

                - The format of dict to use:

                '''
                    {{
                        "tool": "{ToolTypeNames.EXPERT_NETWORK_QUERY_CALL}",
                        "parameters": {{
                            "assistant_id": "...",
                            "query": "...",
                            "image_urls": ["..."],
                            "file_urls": ["..."]
                        }}
                    }}
                '''

                *INSTRUCTIONS*

                - "assistant_id" is ID of assistant you want to consult. Find ID of assistant by checking
                 networks/assistants you have access.
                - "query" is question/request you want to ask.
                - "image_urls" is list of URLs of images to provide to expert.
                - "file_urls" is list of URLs of files to provide to expert.

                The answer will be returned as a response, and it will be in the following format:

                [n] "tool_name": {ToolTypeNames.EXPERT_NETWORK_QUERY_CALL},
                    [na.] "tool_response": <sample response>,
                    [ib.] "file_uris": ["...", "..."],
                    [ic.] "image_uris": ["...", "..."]

                *Important Note*
                - If you retrieve the response, stop calling the tool again, and instead provide the response to
                user in natural language, using data you received.

                ---
            """
    return response_prompt
