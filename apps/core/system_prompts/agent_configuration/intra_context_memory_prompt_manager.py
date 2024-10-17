#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: build_context_overflow_prompt.py
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


from apps.assistants.models import Assistant


def build_intra_context_memory_prompt(assistant: Assistant):
    return f"""
        ### **CONTEXT OVERFLOW MANAGEMENT**

        To prevent overload in your context window, a strategy has been set for managing the number of messages
            you store and determining actions when the limit is reached. The current strategy is as follows:

        ---

        **Strategy**: `{assistant.context_overflow_strategy}`
        **Maximum Messages**: `{assistant.max_context_messages}`

        ---

        #### **Actions When Limit Is Reached:**

        1. **Stop Conversation**:
           - If the limit is reached, the conversation will stop, and you will receive a system message.
                Notify the user about the context overflow and politely end the conversation.

        2. **Forget Oldest Messages**:
           - Once the limit is hit, the oldest messages will be removed, allowing new messages to be stored.
                Continue the conversation uninterrupted. If you forget any details, inform the user of this strategy
                and ask them to repeat the message.

        3. **Store as Vector**:
           - If this strategy is set, overflowed messages will be stored in a vector store, enabling you to
                reference them later. Refer to the relevant section (defined as a 'TOOL') to understand how to
                retrieve those messages when needed.

        ---
    """
