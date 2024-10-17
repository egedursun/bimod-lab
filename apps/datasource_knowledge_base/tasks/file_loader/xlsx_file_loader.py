#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: load_xlsx_helper_tasks.py
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
#   For permission inquiries, please contact: admin@Bimod.io.
#
import logging

from langchain_community.document_loaders import UnstructuredExcelLoader

logger = logging.getLogger(__name__)


def load_xlsx_content(path: str):
    loader = UnstructuredExcelLoader(file_path=path)
    docs = loader.load()
    clean_doc = {
        "page_content": "",
        "metadata": {}
    }
    if docs:
        for doc in docs:
            try:
                pg_content = doc.page_content
                meta = doc.metadata
                clean_doc["page_content"] += pg_content
                clean_doc["metadata"] = meta
            except Exception as e:
                logger.error(f"[tasks.load_xlsx_content] Error loading the XLSX content: {e}")
                continue
    logger.info(f"[tasks.load_xlsx_content] XLSX content loaded successfully.")
    return clean_doc
