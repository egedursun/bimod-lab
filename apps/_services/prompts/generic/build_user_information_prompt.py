#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: build_user_information_prompt.py
#  Last Modified: 2024-08-01 13:09:54
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:10:41
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib.auth.models import User


def build_structured_user_information_prompt(user: User):
    return f"""
        **USER INFORMATION:**

        '''
        User's Full Name: {user.profile.first_name} {user.profile.last_name}
        User's Email: {user.email}
        User's City: {user.profile.city}
        User's Country: {user.profile.country}
        User's Birthday: {user.profile.birthdate}
        '''

        **NOTE**: This is the information about the user you are currently chatting with. Make sure to keep
        this information in mind while responding to the user's messages. If this part is EMPTY, you can
        respond to the user's messages without any specific considerations.
    """
