#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: build_tone_prompt.py
#  Last Modified: 2024-09-28 00:42:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:10:39
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

def build_structured_tone_prompt(tone: str):
    return f"""
        **YOUR TONE:**

        '''
        {tone}
        '''

        **NOTE**: This is the tone that you will be using while responding to the user's messages. Your use
        of language, the way you respond, and the way you interact with the user will be based on this tone.
        Make sure to keep this in mind while responding to the user's messages. If this part is EMPTY, you can
        use a standard tone, without any specific considerations.
    """
