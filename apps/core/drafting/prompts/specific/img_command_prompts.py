#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: img_command_prompts.py
#  Last Modified: 2024-10-16 01:34:51
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-16 01:35:43
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

def build_drafting_action__img_prompt(user_query: str):
    return f"""
        ### **SELECTED ACTION BY THE USER:**

        '''
            //img
        '''

        **Tools & Data Sources:**

        '''
        - Data Sources You Have: [IMAGE GENERATION TOOL]
        - Tools You Have: [USE IMAGE GENERATION TOOL TO GENERATE IMAGES]
        '''

        ---

        **YOUR GOAL:** The user picked the Image Generation Command action. You MUST check the user's query and
        understand what kind of image they want to generate. Then, you must generate an image that's fitting the
        overall status of the document, as well as the query of the user to satisfy his expectations and needs.
        You must only generate a single (1) image. You must USE YOUR IMAGE GENERATION TOOL to provide the user with
        a generated image, based on the query of the user. You must not directly write a prompt, you must provide
        the prompt in a structured format, as specified in your prompt.

        ---

        **QUERY OF THE USER:**

        '''
        {user_query}
        '''

    """
