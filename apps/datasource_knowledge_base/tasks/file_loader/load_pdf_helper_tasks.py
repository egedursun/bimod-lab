#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: load_pdf_helper_tasks.py
#  Last Modified: 2024-09-28 22:44:38
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:44:38
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.
#
#  Project: Bimod.io
#  File: load_pdf_helper_tasks.py
#  Last Modified: 2024-09-26 22:02:31
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:44:13
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from langchain_community.document_loaders import PyPDFLoader


def load_pdf_helper(path: str):
    loader = PyPDFLoader(file_path=path)
    docs = loader.load()
    clean_doc = {"page_content": "", "metadata": {}}
    if docs:
        for doc in docs:
            try:
                page_content = doc.page_content
                metadata = doc.metadata
                clean_doc["page_content"] += page_content
                clean_doc["metadata"] = metadata
            except Exception as e:
                print(f"[tasks.load_pdf_helper] Error loading PDF: {e}")
                continue
    return clean_doc
