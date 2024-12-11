#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: index_repository_helper_tasks.py
#  Last Modified: 2024-10-05 01:39:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:46
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

from apps.datasource_codebase.tasks.create_repository_upload_log_tasks import (
    add_repository_upload_log
)

from apps.datasource_codebase.utils import (
    RepositoryUploadStatusNames
)

logger = logging.getLogger(__name__)


@shared_task
def index_repository_helper(
    connection_id,
    document_paths
):
    from apps.datasource_codebase.models import (
        CodeRepositoryStorageConnection
    )

    from apps.core.codebase.codebase_decoder import (
        CodeBaseDecoder
    )

    conn = CodeRepositoryStorageConnection.objects.get(
        id=connection_id
    )

    xc = CodeBaseDecoder.get(
        connection=conn
    )

    if isinstance(
        document_paths,
        str
    ):
        document_paths = [
            document_paths
        ]

    for i, path in enumerate(document_paths):

        try:

            acc_doc = xc.repository_loader(
                file_path=path
            )

            if not acc_doc:
                add_repository_upload_log(
                    document_full_uri=path,
                    log_name=RepositoryUploadStatusNames.FAILED
                )

                logger.error(f"Document could not be loaded: {path}")

                continue

            add_repository_upload_log(
                document_full_uri=path,
                log_name=RepositoryUploadStatusNames.LOADED
            )

            logger.info(f"Document Loaded: {path}")

            chks = xc.chunk_repository(
                connection_id=xc.connection_object.id,
                document=acc_doc
            )

            if not chks:
                add_repository_upload_log(
                    document_full_uri=path,
                    log_name=RepositoryUploadStatusNames.FAILED
                )

                logger.error(f"Document could not be chunked: {path}")

                continue

            add_repository_upload_log(
                document_full_uri=path,
                log_name=RepositoryUploadStatusNames.CHUNKED
            )

            logger.info(f"Document Chunked: {path}")

            n_chks = len(chks) if chks else 0

            doc_id, doc_uuid, error = xc.embed_repository(
                document=acc_doc,
                path=path,
                number_of_chunks=n_chks
            )

            add_repository_upload_log(
                document_full_uri=path,
                log_name=RepositoryUploadStatusNames.PROCESSED_DOCUMENT
            )

            logger.info(f"Document Processed: {path}")

            if error or not doc_id or not doc_uuid:
                add_repository_upload_log(
                    document_full_uri=path,
                    log_name=RepositoryUploadStatusNames.FAILED
                )

                logger.error(f"Document could not be embedded: {path}")

                continue

            errors = xc.embed_repository_chunks(
                chunks=chks,
                path=path,
                document_id=doc_id,
                document_uuid=doc_uuid
            )

            if errors:
                add_repository_upload_log(
                    document_full_uri=path,
                    log_name=RepositoryUploadStatusNames.PARTIALLY_FAILED
                )

                logger.error(f"Document chunks could not be embedded: {path}")

                continue

            add_repository_upload_log(
                document_full_uri=path,
                log_name=RepositoryUploadStatusNames.PROCESSED_CHUNKS
            )

            add_repository_upload_log(
                document_full_uri=path,
                log_name=RepositoryUploadStatusNames.COMPLETED
            )

            logger.info(f"Document Completed: {path}")

        except Exception as e:
            add_repository_upload_log(
                document_full_uri=path,
                log_name=RepositoryUploadStatusNames.FAILED
            )

            logger.error(f"Error processing the document: {e}")

            continue

    logger.info(f"Document Processing Completed successfully.")

    return
