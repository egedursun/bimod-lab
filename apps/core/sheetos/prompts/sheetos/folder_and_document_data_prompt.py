#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: folder_and_document_data_prompt.py
#  Last Modified: 2024-10-16 16:57:35
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-16 16:57:37
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from apps.sheetos.models import (
    SheetosFolder,
    SheetosDocument
)


def build_sheetos_folder_and_document_data_prompt(
    folder: SheetosFolder,
    doc: SheetosDocument
):
    return f"""
        ### **FOLDER INFORMATION:**

        '''
        Folder's Name: {folder.name}
        Folder's Description: {folder.description}
        Folder's Organization: {folder.organization}
        Folder's Creation Date: {folder.created_at}

        **General Instructions for the Document's within this Folder:**

        {folder.meta_context_instructions}

        '''

        **NOTE**: This is the information about the folder the document you are helping the user (a spreadsheet).
        You need to be aware of the general meta-context instructions the folder has in order to grasp the overall
        context of other documents belonging to this folder. This will be helpful for you to generate better data and
        manipulate the data in the spreadsheet by making you more aware.

        ---

        ### **DOCUMENT INFORMATION:**

        '''
        Document's Folder: {doc.document_folder.name}
        Document's Title: {doc.document_title}
        Document's Tone: {doc.tone}
        Document's Target Audience: {doc.target_audience}
        Document's Creation Date: {doc.created_at}

        **Instructions for the Document:**

        {doc.context_instructions}

        '''

        **NOTE**: This is the information about the spreadsheet document you are currently interacting on with the user.
        You must be careful about the tone and target audience specified for this document while creating generated spreadsheet
        data for this document. Additionally, beware of the instructions specified for this document to understand the overall
        context of the document.

        ---
    """
