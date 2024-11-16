#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: voidforger_place_and_time_prompt.py
#  Last Modified: 2024-11-16 00:49:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-16 00:49:09
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.contrib.auth.models import User
from datetime import datetime


def build_structured_place_and_time_prompt_voidforger(user):
    user: User
    response_prompt = """
            ### **PLACE AND TIME**

            '''
            """
    user_location = f"""
            User Address: {user.profile.address}
                City: {user.profile.city}
                Country: {user.profile.country}
                Postal Code: {user.profile.postal_code}
                Coordinates: [Infer on Address]
        """

    current_time = f"""
            ---

            - [UTC] Current Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

                - Retrieved by datetime.datetime.now().

            - [Local] Current Time: [Infer on Country/City & Date]

            '''

            - **NOTE:** For local time, infer it from user's location and don't forget considering Daylight Savings. If
            you are not in a chat and therefore if you are triggered automatically, please ignore this part.

            ---
            """

    response_prompt += user_location + current_time
    return response_prompt
