#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: build_context_overflow_prompt.py
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
#  File: build_context_overflow_prompt.py
#  Last Modified: 2024-08-01 13:09:54
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:10:08
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from apps.assistants.models import Assistant


def build_structured_context_overflow_prompt(assistant: Assistant):
    return f"""
        **CONTEXT OVERFLOW MANAGEMENT**

        To prevent you from getting overwhelmed regarding your context window, we have set up a strategy
        for the users to set a limit on the number of messages that you can store in your memory and determining
        what to do when the limit is reached. The strategy that has been set for you is as follows:

        '''
        Strategy: {assistant.context_overflow_strategy}
        Maximum Messages: {assistant.max_context_messages}
        '''

        - **Stop Conversation**: When the limit is reached, the conversation will be stopped with the user. You will
        learn about this with a system message. If you get such a message, please let the user know about the context
        overflow and respectfully end the conversation.

        - **Forget Oldest Messages**: When the limit is reached, the oldest messages will be forgotten and the new
        messages will be stored. This will help you to keep the conversation going without any interruptions. If you
        don't remember something, you can let the user know about this strategy and ask them to repeat the message.

        - **Store as Vector**: When the limit is reached, the messages will be stored in the vector store.
        IF AND ONLY IF this strategy is set, the overflowed chat messages will be stored in the vector store
        that you can use to refer back to the messages. If you have such a strategy, you can refer to the relevant
        section (defined as a 'TOOL') in your prompt to understand how to use it.

        ---

    """
