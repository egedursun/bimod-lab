#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: voidforger_agent_personality_prompt.py
#  Last Modified: 2024-11-16 00:49:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-16 00:49:48
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


def build_agent_personality_prompt_voidforger(tone):
    return f"""
        ### **YOUR TONE:**

        '''
        {tone}
        '''

        **NOTE**: This is the tone that you have as the assistant. The way you use language, respond, and perform
        interactions must be based on this tone. Make sure to keep this in mind while performing your tasks. If this
        part is EMPTY, assume a standard tone.
    """
