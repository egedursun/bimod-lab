#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: leanmod_semantor_execution_prompt.py
#  Last Modified: 2024-11-10 17:06:53
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-10 17:06:53
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


def build_structured_tool_prompt__semantor_consultation_execution_leanmod():
    response_prompt = f"""
                ### **TOOL: Semantor Consultation Query Execution Tool**

                - This allows consulting to local and global assistants within the Semantor network. Local assistants
                are assistants that are within the organization of the user and might have broader set of data sources
                that are internal and specific to the organization, while global assistants might have a broader set
                of specialities and can be helpful although they might not have access to internal data sources.

                - [1] While using these consultations, if there is a local assistant that can be capable of doing the task
                prompted by the user, you must always prioritize local assistants over global assistants.

                - [2] However, if the capabilities or specialties of the local assistants are not sufficient for the task,
                you can consult to global assistants.

                -----

                - The format of dict to use for consulting Semantor Network Assistants:

                '''
                    {{
                        "tool": "{ToolCallDescriptorNames.EXECUTE_SEMANTOR_CONSULTATION_QUERY}",
                        "parameters": {{
                            "object_id": <id of the target assistant>,
                            "is_local": <boolean value>,
                            "query": "<your request from the target assistant>",
                            "image_urls": ["..."],
                            "file_urls": ["..."]
                        }}
                    }}
                '''

                ---

                #### **INSTRUCTIONS**

                - "object_id" is the ID of the assistant you want to consult, either in local or global network.
                - "is_local" is a boolean value that indicates whether the assistant is local or global, depending
                    on which one you have chosen to consult.
                - "query" is question/request you want to perform.
                - "image_urls" is list of URLs of images to provide to expert.
                - "file_urls" is list of URLs of files to provide to expert.

                The answer will be returned as a response, and it will be in the following format:

                [n] "tool_name": {ToolCallDescriptorNames.EXECUTE_SEMANTOR_CONSULTATION_QUERY},
                    [na.] "tool_response": <sample response>,
                    [ib.] "file_uris": ["...", "..."],
                    [ic.] "image_uris": ["...", "..."]

                #### **Important Note**
                    - If you retrieve the response, stop calling the tool again, and instead provide the response to
                        user in natural language, using data you received.

                ---
            """
    return response_prompt
