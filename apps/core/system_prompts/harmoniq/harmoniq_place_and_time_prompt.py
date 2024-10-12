#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: harmoniq_place_and_time_prompt.py
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
#   For permission inquiries, please contact: admin@br6.in.
#


from datetime import datetime


def build_structured_place_and_time_prompt_harmoniq(organization_data: dict, user_data: dict):
    response_prompt = f"""

            ### **YOUR ORGANIZATION:**

                - Organization Name {organization_data["org_name"]}
                - Organization Address: {organization_data["org_address"]}
                - Organization Phone: {organization_data["org_phone"]}
                - Organization City: {organization_data["org_city"]}
                - Organization Country: {organization_data["org_country"]}
                - Organization Postal Code: {organization_data["org_postal_code"]}
                - Organization Industry: {organization_data["org_industry"]}

            ---

            ### **USER YOU ARE INTERACTING:**

                - Username: {user_data["username"]}
                - Email: {user_data["email"]}
                - First Name: {user_data["first_name"]}
                - Last Name: {user_data["last_name"]}
                - Phone: {user_data["phone"]}
                - Address: {user_data["address"]}
                - City: {user_data["city"]}
                - Country: {user_data["country"]}
                - Postal Code: {user_data["postal_code"]}

            ---

            ### **PLACE AND TIME**

            '''
            """

    current_time = f"""
            ---

            - [UTC] Current Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                - Retrieved by datetime.datetime.now().

            - [Local] Current Time: [Infer on Country/City & Date]
            - [Infer the Timezone] Current Time: [Infer on Country/City & Date]

            '''

            ---
            """

    response_prompt += current_time
    return response_prompt
