#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: leanmod_user_information_prompt.py
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
#
#

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
