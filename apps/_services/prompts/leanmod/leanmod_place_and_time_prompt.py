#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: leanmod_place_and_time_prompt.py
#  Last Modified: 2024-09-28 20:38:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:11:05
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from datetime import datetime

from django.contrib.auth.models import User


def build_structured_place_and_time_prompt_leanmod(user: User):
    # Build the prompt
    response_prompt = """
            *PLACE AND TIME*

            '''
            """
    # Get the location of the user
    user_location = f"""
            User Address: {user.profile.address}
                City: {user.profile.city}
                Country: {user.profile.country}
                Postal Code: {user.profile.postal_code}
                Coordinates: [Infer on Address]
        """

    # Get the current time
    current_time = f"""
            ---
            [UTC] Current Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                    - Retrieved by datetime.datetime.now().
            [Local] Current Time: [Infer on Country/City & Date]
            '''

            NOTE: For local time, infer it from user's country/city and don't forget the Daylight Saving Time.
            """

    response_prompt += user_location + current_time
    return response_prompt
