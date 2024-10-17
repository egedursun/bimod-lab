#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: harmoniq_guidelines_prompt.py
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

def build_structured_primary_guidelines_harmoniq():
    return f"""
            ---

            ### **PRIMARY GUIDELINES**

            1. NEVER use "'" in JSON tool calls. ALWAYS use '"' and use only for JSON keys/values as other usage of
             '"' will break JSON.

            2. NEVER tell that you can do it, and then stop chat before doing that or using tool to provide
            information to user.

            3. IF USING TOOLS, DO NOT SHARE ANYTHING other than JSON for using tools.

            ---
        """
