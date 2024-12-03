#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: index_document_helper_tasks.py
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

from celery import shared_task

from apps.datasource_knowledge_base.utils import (
    document_loader
)


logger = logging.getLogger(__name__)


@shared_task
def index_document_helper(
    connection_id,
    document_paths
):

    from apps.datasource_knowledge_base.models import (
        DocumentKnowledgeBaseConnection
    )

    from apps.core.vector_operations.vector_document.vector_store_decoder import (
        KnowledgeBaseSystemDecoder
    )

    from apps.datasource_knowledge_base.utils import (
        VectorStoreDocProcessingStatusNames
    )

    from apps.datasource_knowledge_base.tasks import (
        add_vector_store_doc_loaded_log
    )

    conn = DocumentKnowledgeBaseConnection.objects.get(
        id=connection_id
    )

    xc = KnowledgeBaseSystemDecoder.get(
        connection=conn
    )

    if isinstance(document_paths, str):
        document_paths = [document_paths]

    for i, path in enumerate(document_paths):
        try:
            docc = _load_doc(path, xc)

            if not docc:
                add_vector_store_doc_loaded_log(
                    document_full_uri=path,
                    log_name=VectorStoreDocProcessingStatusNames.FAILED
                )

                logger.error(f"[index_document_helper] Document could not be loaded: {path}")
                continue

            add_vector_store_doc_loaded_log(
                document_full_uri=path,
                log_name=VectorStoreDocProcessingStatusNames.LOADED
            )

            logger.info(f"[index_document_helper] Document loaded: {path}")
            chks = _chunk_doc(docc, xc)

            if not chks:
                add_vector_store_doc_loaded_log(
                    document_full_uri=path,
                    log_name=VectorStoreDocProcessingStatusNames.FAILED
                )

                logger.error(f"[index_document_helper] Document could not be chunked: {path}")
                continue

            add_vector_store_doc_loaded_log(
                document_full_uri=path,
                log_name=VectorStoreDocProcessingStatusNames.CHUNKED
            )

            logger.info(f"[index_document_helper] Document chunked: {path}")
            doc_id, doc_uuid, error = _embed_doc(chks, docc, path, xc)

            add_vector_store_doc_loaded_log(
                document_full_uri=path,
                log_name=VectorStoreDocProcessingStatusNames.PROCESSED_DOCUMENT
            )

            logger.info(f"[index_document_helper] Document embedded: {path}")

            if error or not doc_id or not doc_uuid:

                add_vector_store_doc_loaded_log(
                    document_full_uri=path,
                    log_name=VectorStoreDocProcessingStatusNames.FAILED
                )

                continue

            logger.info(f"[index_document_helper] Document embedded successfully: {path}")
            errors = _chunk_doc_chks(chks, doc_id, doc_uuid, path, xc)

            if errors:
                add_vector_store_doc_loaded_log(
                    document_full_uri=path,
                    log_name=VectorStoreDocProcessingStatusNames.PARTIALLY_FAILED
                )

                logger.error(f"[index_document_helper] Document chunks could not be embedded: {path}")
                continue

            add_vector_store_doc_loaded_log(
                document_full_uri=path,
                log_name=VectorStoreDocProcessingStatusNames.PROCESSED_CHUNKS
            )

            add_vector_store_doc_loaded_log(
                document_full_uri=path,
                log_name=VectorStoreDocProcessingStatusNames.COMPLETED
            )

            logger.info(f"[index_document_helper] Document indexed successfully: {path}")

        except Exception as e:
            add_vector_store_doc_loaded_log(
                document_full_uri=path,
                log_name=VectorStoreDocProcessingStatusNames.FAILED
            )

            logger.error(f"[index_document_helper] Error processing the document: {e}")
            continue

    return


def _chunk_doc_chks(
    chks,
    doc_id,
    doc_uuid,
    path,
    xc
):
    errors = xc.embed_document_chunks(
        chunks=chks,
        path=path,
        document_id=doc_id,
        document_uuid=doc_uuid
    )

    return errors


def _chunk_doc(docc, xc):
    chks = xc.chunk_document(
        connection_id=xc.connection_object.id,
        document=docc
    )

    return chks


def _load_doc(path, xc):
    file_format = path.split(".")[-1]

    docc = document_loader(
        file_path=path,
        file_type=file_format
    )

    return docc


def _embed_doc(
    chks,
    docc,
    path,
    xc
):
    n_chks = len(chks) if chks else 0

    doc_id, doc_uuid, error = xc.embed_document(
        document=docc,
        path=path,
        number_of_chunks=n_chks
    )

    return doc_id, doc_uuid, error
