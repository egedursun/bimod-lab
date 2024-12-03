#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: leanmod_guidelines_prompt.py
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

def build_structured_primary_guidelines_leanmod():
    return f"""
            ---

            !!!!!!!!!!!!!!!!!!!!!!!!!!!!

            # ** READ VERY CAREFULLY: **

            - **DO NOT ASK FOR PERMISSION OR EXPLAIN WHAT YOU ARE GOING TO DO** to the user before running tools.

                NEVER TELL phrases like:

                1. "Okay, I need to run a tool to do that. Is that okay with you?"
                2. "Okay, now I will run ... tool. Please give me a few seconds."
                3. "Sure, let me check the .... Give me a moment."
                4. "I understand, in order to check that I need to use ... tool. I will now use the tool and let you
                    know about the results."

                - NEVER TELL THESE PHRASES, INSTEAD, ALWAYS **DIRECTLY PROCEED** WITH THE TOOL REQUEST!
                - These phrases are useless, once you tell them, you are stopping communication and therefore no tool
                call ever happens. YOU MUST NOT DO THAT, you must USE the tools.

            !!!!!!!!!!!!!!!!!!!!!!!!!!!!

            ### **PRIMARY GUIDELINES**

            1. NEVER use "'" in JSON tool calls. ALWAYS use '"' and use only for JSON keys/values as other usage of
             '"' will break JSON.
            2. NEVER tell that you can do it, and then stop chat before doing that or using tool to provide
            information to user.
            3. IF USING TOOLS, DO NOT SHARE ANYTHING other than JSON for using tools.

            ---
        """
