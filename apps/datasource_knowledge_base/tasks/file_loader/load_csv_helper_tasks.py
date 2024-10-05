#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: load_csv_helper_tasks.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:47
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#
#

from langchain_community.document_loaders import UnstructuredCSVLoader


def load_csv_helper(path: str):
    loader = UnstructuredCSVLoader(file_path=path, mode="single")
    docs = loader.load()
    clean_doc = {"page_content": "", "metadata": {}}
    if docs:
        for doc in docs:
            try:
                page_content = doc.page_content
                metadata = doc.metadata
                clean_doc["page_content"] += page_content
                clean_doc["metadata"] = metadata
                return clean_doc
            except Exception as e:
                print(f"[tasks.load_csv_helper] Error loading CSV: {e}")
                continue
    return clean_doc
