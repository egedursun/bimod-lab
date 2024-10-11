#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from celery import shared_task

from apps.datasource_codebase.tasks.create_repository_upload_log_tasks import add_repository_upload_log
from apps.datasource_codebase.utils import RepositoryUploadStatusNames


@shared_task
def index_repository_helper(connection_id, document_paths):
    from apps.datasource_codebase.models import CodeRepositoryStorageConnection
    from apps.core.codebase.codebase_decoder import CodeBaseDecoder

    conn = CodeRepositoryStorageConnection.objects.get(id=connection_id)
    xc = CodeBaseDecoder.get(connection=conn)
    if isinstance(document_paths, str):
        document_paths = [document_paths]

    for i, path in enumerate(document_paths):
        try:
            acc_doc = xc.repository_loader(file_path=path)
            if not acc_doc:
                add_repository_upload_log(document_full_uri=path, log_name=RepositoryUploadStatusNames.FAILED)
                continue
            add_repository_upload_log(document_full_uri=path, log_name=RepositoryUploadStatusNames.LOADED)

            chks = xc.chunk_repository(connection_id=xc.connection_object.id, document=acc_doc)
            if not chks:
                add_repository_upload_log(document_full_uri=path, log_name=RepositoryUploadStatusNames.FAILED)
                continue
            add_repository_upload_log(document_full_uri=path, log_name=RepositoryUploadStatusNames.CHUNKED)

            n_chks = len(chks) if chks else 0
            doc_id, doc_uuid, error = xc.embed_repository(
                document=acc_doc, path=path, number_of_chunks=n_chks
            )
            add_repository_upload_log(document_full_uri=path, log_name=RepositoryUploadStatusNames.PROCESSED_DOCUMENT)

            if error or not doc_id or not doc_uuid:
                add_repository_upload_log(document_full_uri=path, log_name=RepositoryUploadStatusNames.FAILED)
                continue

            errors = xc.embed_repository_chunks(chunks=chks, path=path, document_id=doc_id, document_uuid=doc_uuid)
            if errors:
                add_repository_upload_log(document_full_uri=path, log_name=RepositoryUploadStatusNames.PARTIALLY_FAILED)
                continue
            add_repository_upload_log(document_full_uri=path, log_name=RepositoryUploadStatusNames.PROCESSED_CHUNKS)
            add_repository_upload_log(document_full_uri=path, log_name=RepositoryUploadStatusNames.COMPLETED)

        except Exception as e:
            add_repository_upload_log(document_full_uri=path, log_name=RepositoryUploadStatusNames.FAILED)
            continue
    return
