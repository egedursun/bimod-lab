#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: build_context_memory_instruction.py
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
#  File: build_context_memory_instruction.py
#  Last Modified: 2024-09-28 00:42:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:09:34
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

def build_context_memory_instructions_prompt():
    context_memory_instructions = f"""
        ---
        **SYSTEM MESSAGE:**

        - This conversation has more messages than you are actually able to see. Some of the
        messages has been deleted since the context window limit determined by the user has been reached.
        Therefore, please be aware of the fact that you might not be remembering some of the things the
        user has said. If you don't remember something, you can let the user know about this strategy and
        ask them to repeat the message.
        ---
    """
    return context_memory_instructions


def build_context_memory_stop_conversation_prompt():
    stop_conversation_prompt = f"""
        ---
        **SYSTEM MESSAGE:**

        - The conversation needs to be stopped. Please let the user know about the context
        overflow and respectfully end the conversation.
        ---
    """
    return stop_conversation_prompt
