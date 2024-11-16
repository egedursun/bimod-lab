#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: voidforger_old_message_search_prompt.py
#  Last Modified: 2024-11-16 00:53:18
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-16 00:53:18
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from apps.core.tool_calls.utils import VoidForgerModesNames, ToolCallDescriptorNames


def build_structured_tool_prompt__old_message_search_execution_voidforger():
    response_prompt = f"""
            ### **TOOL: Old Chat Message Search Tool**

            - This tool is only helpful if your current mode is '{VoidForgerModesNames.CHAT}'.

            - Please neglect this tool if your mode is '{VoidForgerModesNames.AUTOMATED}' or '{VoidForgerModesNames.MANUAL}'
            since it is irrelevant and unlikely to provide any helpful data for you.

            - This tool allows you to search for old messages in a chat environment with a user, so that you can remember
            important details if you think some of the context is missing. Your message memory is limited to 25 messages in
            total, so if the conversation is long, you can choose to search through older messages to understand the older
            topics.

            - To use this tool, you must provide a query to search with the old chat messages. Your query will be searched
            within the fields of the old chat messages, which contain:
                i. chat_id: The ID of the chat the message belongs to.
                i. sender_type: The type of the sender, which can be 'user' or 'assistant'.
                ii. message_text_content: The content of the message in text format.
                iii. message_image_content: The image URLs if the message has any.
                iv. message_file_content: The file URLs if the message has any.
                v. message_audio: The audio URLs if the message has been narrated.
                vi. sent_at: The timestamp of the message sent.

            -----

            - The format of dict to use for searching the old chat messages is as follows:

            '''
                {{
                    "tool": "{ToolCallDescriptorNames.EXECUTE_VOIDFORGER_OLD_MESSAGE_SEARCH_QUERY}",
                    "parameters": {{
                        "query": "<your search query here>"
                    }}
                }}
            '''

            ---

            #### **INSTRUCTIONS**

            - "query" is the field where you will provide the search query to search within the old chat messages.

            The answer will be returned as a response, and it will be in the following format:

            [n] "tool_name": {ToolCallDescriptorNames.EXECUTE_VOIDFORGER_OLD_MESSAGE_SEARCH_QUERY},
                [na.] "tool_response": <sample response>,
                [ib.] "file_uris": ["...", "..."],
                [ic.] "image_uris": ["...", "..."]

            ---
        """
    return response_prompt
