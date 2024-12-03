#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: leanmod_semantor_query_search_prompt.py
#  Last Modified: 2024-11-10 17:06:15
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-10 17:06:16
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


def build_structured_tool_prompt__semantor_search_execution_leanmod():
    response_prompt = f"""
                ### **TOOL: Semantor Search Query Execution Tool**

                - This tool allows you to retrieve the list of assistants within the local and global Semantor network,
                for you to approach as a solution if you can't complete a task yourself, and none of the assistants in
                your connected expert networks can also fulfill the task. In that case, you can use this tool to retrieve
                the list of local and global assistants that can help you with the task.

                - Local assistants are assistants that are within the organization of the user and might have broader
                set of data sources (e.g. SQL/NoSQL databases, File Systems, Browsers, Knowledge Bases, etc.) that are
                internal and specific to the organization

                - Global assistants are public assistants that are not specific to the organization, but they might
                have a broader set of different specialties and professions, and can be very helpful in some cases.
                Although they don't have data sources or tools themselves, they might have temporary access to them
                via other assistants with data sources acting as a reference, and this process is automatically handled
                by the system.

                - After you learn about the assistants that can help you, you can consult to them using the Semantor
                Consultation Query Execution Tool, which is another tool that you can use to consult to local and global
                assistants within the Semantor network. This tool is similar to using Expert Network Query Execution Tool,
                but it must be used only if you can't find a solution from the assistants in your connected expert networks.

                -----

                - The format of dict to use for searching within Semantor Network Assistants:

                '''
                    {{
                        "tool": "{ToolCallDescriptorNames.EXECUTE_SEMANTOR_SEARCH_QUERY}",
                        "parameters": {{
                            "query": "<your request from the target assistant>"
                        }}
                    }}
                '''

                ---

                #### **INSTRUCTIONS**

                - "query" is question/request you want to perform. Please note that this tool won't directly consult to
                the assistant for you, but it will provide you with the list of assistants that can help you with the task.
                You will then have to choose one of the ID of the assistants to consult to, and then run the Semantor
                Consultation Query Execution Tool to consult to the assistant.

                The answer will be returned as a response, and it will be in the following format:

                [n] "tool_name": {ToolCallDescriptorNames.EXECUTE_SEMANTOR_SEARCH_QUERY},
                    [na.] "tool_response": <sample response>,
                    [ib.] "file_uris": ["...", "..."],
                    [ic.] "image_uris": ["...", "..."]

                #### **Important Note**
                    - If you managed to successfully retrieve the response from the tool, stop calling the same tool over
                     and over again, and instead provide the response to user in natural language, using data you
                     received; **OR** use another tool that will make you  closer to reaching the solution.

                ---
            """
    return response_prompt


