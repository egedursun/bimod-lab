#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: leanmod_user_information_prompt.py
#  Last Modified: 2024-09-23 12:33:07
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:11:07
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib.auth.models import User


def build_structured_user_information_prompt_leanmod(user: User):
    return f"""
            *USER*

            '''
            Name: {user.profile.first_name} {user.profile.last_name}
                Mail: {user.email}
                City: {user.profile.city}
                Country: {user.profile.country}
                B.Day: {user.profile.birthdate}
            '''

            NOTE: This is info about chatting user.
        """
