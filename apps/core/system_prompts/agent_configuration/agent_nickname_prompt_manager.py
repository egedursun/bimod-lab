#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: build_name_prompt.py
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
#   For permission inquiries, please contact: admin@br6.in.
#

def build_agent_nickname_prompt(name: str, chat_name: str):
    return f"""
        ### **YOUR NAME:**

        '''
        {name}
        '''

        **NAME OF THE CHAT YOU ARE INTERACTING WITH:**

        '''
        {chat_name}
        '''

        **NOTE**: This is your name as an Agent. The user can refer you by this name. Make sure to keep
        this name in mind while responding to the user's messages. If this part is EMPTY, your default name
        will be "Assistant".
    """
