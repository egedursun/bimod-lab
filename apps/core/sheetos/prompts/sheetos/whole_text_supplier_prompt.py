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
from apps.core.sheetos.sheetos_executor import SheetosExecutionManager


def build_whole_text_supply_prompt(xc: SheetosExecutionManager):
    return f"""
        ### **SPREADSHEET DOCUMENT CONTENT INFORMATION:**

        **CSV-Converted Content of the Spreadsheet:**

        '''

        {xc.sheetos_document.document_content_json_quill}

        '''

        **NOTE**: This is the entire CSV-converted content of the spreadsheet document. There can be a dictionary
        format in the content you receive, and this is because the user is interacting with the text with a JS-based
        editor on our website. Therefore, you must neglect the Handsontable or whatever the JS technology used to
        show the user spreadsheet in the front-end, and just focus on the CSV-formatted part.

            - **NEVER** include the UI-related information in the data you generate for the drafting process,
            because the output you generate will be directly pasted to the spreadsheet editor user is interacting
            with, and it will be rendered by getting converted back from CSV format, so you MUST NOT provide your
            output in natural language or UI-related format. You must produce plain, CSV-formatted output.
            (UNLESS YOU HAVE TOOLS TO RUN, AND YOU DECIDE TO RUN A TOOL: OUTPUT A PLAIN JSON IN THAT CASE).

        ---
    """


def build_whole_text_supply_prompt_public(content: str):
    return f"""
            ### **SPREADSHEET DOCUMENT CONTENT INFORMATION:**

            **CSV-Converted Content of the Spreadsheet:**

            '''

            {str(content)}

            '''

            **NOTE**: This is the entire CSV-converted content of the spreadsheet document. There can be a dictionary
            format in the content you receive, and this is because the user is interacting with the text with a JS-based
            editor on our website. Therefore, you must neglect the Handsontable or whatever the JS technology used to
            show the user spreadsheet in the front-end, and just focus on the CSV-formatted part.

                - **NEVER** include the UI-related information in the data you generate for the drafting process,
                because the output you generate will be directly pasted to the spreadsheet editor user is interacting
                with, and it will be rendered by getting converted back from CSV format, so you MUST NOT provide your
                output in natural language or UI-related format. You must produce plain, CSV-formatted output.
                (UNLESS YOU HAVE TOOLS TO RUN, AND YOU DECIDE TO RUN A TOOL: OUTPUT A PLAIN JSON IN THAT CASE).

            ---
        """
