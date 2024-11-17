#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: build_context_memory_instruction.py
#  Last Modified: 2024-10-05 02:26:00
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


def build_chat_history_memory_handling_prompt():
    context_memory_instructions = f"""
        ---
        ### **SYSTEM MESSAGE:**

        - This conversation might have MORE messages than you are able to see. Some of the messages might have been
        deleted from the history, as the context window limit is reached. If you don't remember something, you can either
        ask the user to repeat, or if you can use tools to search through older chat messages to find the information
        you need. However, don't assume you forgot something before you are sure about it. You don't need to let the
        user know that you forget something unless it is necessary.
        ---
    """
    return context_memory_instructions


def build_chat_history_memory_stop_communication_handler_prompt():
    stop_conversation_prompt = f"""
        ---
        ### **SYSTEM MESSAGE:**

        - The conversation needs to be stopped. Please let the user know about the overflow and respectfully
        end the conversation.
        ---
    """
    return stop_conversation_prompt
