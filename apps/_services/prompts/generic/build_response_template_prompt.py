#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: build_response_template_prompt.py
#  Last Modified: 2024-09-28 00:42:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:10:36
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

def build_structured_response_template_prompt(response_template: str):
    return f"""
        **YOUR RESPONSE TEMPLATE:**

        '''
        {response_template}
        '''

        **NOTE**: This is the template that you will use to respond to the user's messages. Make sure to
        follow this template under any circumstances and do not deviate from it. If this part is EMPTY,
        you can respond to the user's messages in any way you would like.
    """
