#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: voidforger_user_information_prompt.py
#  Last Modified: 2024-11-16 00:49:17
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-16 00:49:18
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


def build_structured_user_information_prompt_voidforger(user):
    return f"""
        ### **ADDITIONAL USER INFORMATION:**

        '''
        Name: {user.profile.first_name} {user.profile.last_name}
            Mail: {user.email}
            Birthday: {user.profile.birthdate}
        '''

        *NOTE:*
            - These are additional information about the user (if you are in a chat, otherwise neglect).

        ---
    """
