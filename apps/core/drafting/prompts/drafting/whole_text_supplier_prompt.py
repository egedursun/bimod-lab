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
from apps.core.drafting.drafting_executor import DraftingExecutionManager


def build_whole_text_supply_prompt(xc: DraftingExecutionManager):
    return f"""
            ### **DOCUMENT TEXT CONTENT INFORMATION:**

            **Textual Content of the Document:**

            '''

            {xc.drafting_document.document_content_json_quill}

            '''

            **NOTE**: This is the entire textual content of the document. There can be a dictionary format in the
            content you receive, and this is because the user is interacting with the text with a Quill editor on
            front-end side. Therefore, you must neglect the Quill-related things, and just focus on the plain text.

                - **NEVER** include the Quill-related things in the text you generate for the drafting process,
                because the text you generate will be directly pasted to the editor user is interacting with, and
                it will be rendered as a plain text, so you MUST NOT provide your output in Quill JSON or anything
                like that. You must produce plain text (UNLESS YOU HAVE TOOLS TO RUN, AND YOU DECIDE TO RUN A TOOL).

            ---
        """


def build_whole_text_supply_prompt_public(content: str):
    return f"""
            ### **DOCUMENT TEXT CONTENT INFORMATION:**

            **Textual Content of the Document:**

            '''

            {str(content)}

            '''

            **NOTE**: This is the entire textual content of the document. There can be a dictionary format in the
            content you receive, and this is because the user is interacting with the text with a Quill editor on
            front-end side. Therefore, you must neglect the Quill-related things, and just focus on the plain text.

                - **NEVER** include the Quill-related things in the text you generate for the drafting process,
                because the text you generate will be directly pasted to the editor user is interacting with, and
                it will be rendered as a plain text, so you MUST NOT provide your output in Quill JSON or anything
                like that. You must produce plain text (UNLESS YOU HAVE TOOLS TO RUN, AND YOU DECIDE TO RUN A TOOL).

            ---
        """
