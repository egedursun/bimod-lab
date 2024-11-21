#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: build_place_and_time_prompt.py
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
#   For permission inquiries, please contact: admin@Bimod.io.
#


import datetime

from django.contrib.auth.models import User


def build_spatial_awareness_prompt(user: User):
    response_prompt = """
        ### **PLACE AND TIME AWARENESS:**

        '''
        """
    user_location = f"""
        - Registered Address: {user.profile.address or "N/A"}
        - City: {user.profile.city or "N/A"}
        - Country: {user.profile.country or "N/A"}
        - Postal Code: {user.profile.postal_code or "N/A"}
        - Coordinates: [Infer approximate coordinates from address, city, and country.]
    """
    current_time = f"""
        ---
        [UTC] Current Time: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                - The date above has been retrieved with standard datetime.datetime.now() function.
        [Local Time] Current Time: [Infer from the User's Country & City. Do not forget considering the season.]
        '''
        **NOTE**: Make sure to keep the user's location and the current time in mind while responding to the
        user's messages. For the local time, you can infer from the user's country and city but make sure
        to consider the season (which might affect the Daylight Saving Time).
        """

    response_prompt += user_location + current_time
    return response_prompt
