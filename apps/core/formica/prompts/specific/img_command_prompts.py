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

def build_formica_action__img_prompt(user_query: str) -> str:
    return f"""
        ### **USER SELECTED ACTION:**

        '''
            //img
        '''

        **Tools & Data Sources:**

        '''
        - Data Sources Available: [IMAGE GENERATION TOOL]
        - Tools Available: [USE IMAGE GENERATION TOOL TO GENERATE IMAGES]
        '''

        ---

        **YOUR GOAL:** The user has selected the Image Generation Command action. Review the user’s query carefully
        to understand the type of image they need for the form. Generate a single image that aligns with the form’s
        purpose and meets the user's requirements. USE YOUR IMAGE GENERATION TOOL to create this image based on the
        user’s query. Do not directly provide a prompt; instead, format it as specified in the structured output.

        ---

        **USER QUERY:**

        '''
        {user_query}
        '''
    """
