#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: build_audience_prompt.py
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


def build_target_audience_prompt(audience: str):
    return f"""
        ### **YOUR AUDIENCE:**

        '''
        {audience}
        '''

        **NOTE**: This is the audience that you will be targeting with your responses. Make sure to keep
        this in mind while responding for to the messages. If this part is EMPTY, you can target a general audience,
        without any specific target.
    """
