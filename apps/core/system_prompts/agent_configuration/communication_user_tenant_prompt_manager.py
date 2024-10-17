#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: build_user_information_prompt.py
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
#
#

from django.contrib.auth.models import User


def build_user_tenant_prompt(user: User):
    return f"""
        ### **USER INFORMATION:**

        '''
        User's Full Name: {user.profile.first_name} {user.profile.last_name}
               Email: {user.email}
               City: {user.profile.city}
               Country: {user.profile.country}
               Birthday: {user.profile.birthdate}
        '''

        **NOTE**: This is the information about the user you are currently chatting. Make sure to keep
        this data in mind while responding to messages. If this part is EMPTY, you can respond
        without any specific considerations.
    """
