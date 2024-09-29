#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: embed_document_data_tasks.py
#  Last Modified: 2024-09-26 22:02:31
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:43:04
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from apps._services.knowledge_base.document.helpers.document_embedder import embed_document_helper


def embed_document_data(executor_params, document, path, number_of_chunks):
    doc_id, doc_uuid = None, None
    try:
        doc_id, doc_uuid, error = embed_document_helper(
            executor_params=executor_params,
            document=document,
            path=path,
            number_of_chunks=number_of_chunks
        )
    except Exception as e:
        error = f"[tasks.embed_document_data] Error embedding the document: {e}"
    return doc_id, doc_uuid, error
