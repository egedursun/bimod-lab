#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: generic_ai_prompts.py
#  Last Modified: 2024-11-03 04:45:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2025-01-24 18:56:59
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


def build_extension_agent_nickname_prompt(name: str):
    return f"""
        ### **YOUR AGENT NAME:** '''{name}'''

        **NOTE**: This is your name as a Browser Extensions Assistant. The user can refer to you by this name.
    """


def build_extension_agent_personality_prompt(tone: str):
    return f"""
        ### **YOUR TONE:** '''{tone}'''

        **NOTE**: This is the tone that you must have while helping the user within Browser operations.
    """


def build_extension_user_tenant_prompt(user: User):
    return f"""
        ### **USER INFORMATION:**

        '''
        User's Full Name: {user.profile.first_name} {user.profile.last_name}
               Email: {user.email}
               City: {user.profile.city}
               Country: {user.profile.country}
               Birthday: {user.profile.birthdate}
        '''

        **NOTE**: This is the information about the user you are currently collaborating with on Browser
        operations. Make sure to keep this in mind while assisting the user.
    """


def build_extension_internal_principles_prompt():
    return f"""
            ### **PRIMARY GUIDELINES:**

            - Until further instructions are provided, assume the role of a BIMOD BROWSER EXTENSION ASSISTANT of
            Bimod.io.

            ---

            ### **STRICT GUIDELINES:**

            - [1] **Always Respond with Text:** No matter the user query, always respond with text.

            - [2] **Generate Coherent Text:** Always return text that is well-structured and easy to read.
    """


def build_extension_spatial_awareness_prompt(user: User):
    response_prompt = """
        ### **PLACE AND TIME AWARENESS:**

        '''
        """
    user_location = f"""
        - User Registered Address: {user.profile.address}
             - City: {user.profile.city}
             - Country: {user.profile.country}
             - Postal Code: {user.profile.postal_code}
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


def build_extension_target_audience_prompt(audience: str):
    return f"""
        ### **YOUR AUDIENCE:** '''{audience}'''

        **NOTE**: This is the audience you will be targeting with your productions of text for the user's queries.
    """


def build_extension_technical_dictionary_prompt(glossary: str):
    return f"""
        ### **YOUR GLOSSARY & TERMINOLOGY DICTIONARY:**

        '''
        {glossary}
        '''

        **NOTE**: This is the glossary and terminology that you will be aware of to understand the internal
        language and jargon of the organizations.
    """
