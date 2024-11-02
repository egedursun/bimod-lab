#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: whole_text_supplier_prompt.py
#  Last Modified: 2024-10-16 17:05:30
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-16 17:05:31
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


def build_whole_text_supply_prompt_public(content: str) -> str:
    return f"""
            ### **FORM TEXT CONTENT INFORMATION:**

            **Textual Content of the Form:**

            '''

            {str(content)}

            '''

            **NOTE**: This is the entire textual content of the form. The content may include dictionary formats or
            Quill editor-related formatting, as the user is working with a Quill editor on the front-end. Focus solely
            on the plain text and disregard any Quill-specific formatting.

                - **NEVER** include Quill-related formatting in the suggestions or content you provide for the form,
                as the text will be rendered as plain text. Your output should be in plain text only (UNLESS YOU NEED
                TO RUN A TOOL AND CHOOSE TO DO SO).

            ---
        """
