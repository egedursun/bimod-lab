#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: whole_text_supplier_prompt.py
#  Last Modified: 2025-01-24 18:52:46
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2025-01-24 18:54:06
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

def build_whole_text_supply_prompt_public(content: str):
    return f"""
            ### **DOCUMENT TEXT CONTENT INFORMATION:**

            **Textual Content of the Document:**

            '''

            {str(content)}

            '''

            **NOTE**: This is the entire textual content of the document. There can be a dictionary format in the
            content you receive. Therefore, you must neglect the UI things, and just focus on the plain text.

                - **NEVER** include the UI things in the text you generate and because the content you generate will
                be directly pasted to the editor user is interacting with, and it will be rendered as a plain text,
                so you MUST NOT provide your output in JSON or anything like that. You must produce plain text (UNLESS
                YOU HAVE TOOLS TO RUN, AND YOU DECIDE TO RUN A TOOL).

            ---
        """
