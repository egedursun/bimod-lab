#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: index_repository_helper_tasks.py
#  Last Modified: 2024-09-26 20:30:21
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:38:00
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from celery import shared_task

from apps.datasource_codebase.tasks.create_repository_upload_log_tasks import add_repository_upload_log
from apps.datasource_codebase.utils import RepositoryUploadStatusNames


@shared_task
def index_repository_helper(connection_id, document_paths):
    from apps.datasource_codebase.models import CodeRepositoryStorageConnection
    from apps._services.codebase.codebase_decoder import CodeBaseDecoder

    connection = CodeRepositoryStorageConnection.objects.get(id=connection_id)
    executor = CodeBaseDecoder.get(connection=connection)
    if isinstance(document_paths, str):
        document_paths = [document_paths]
    # Iterate through the repositories
    print(f"[tasks.index_repository_helper] Indexing {len(document_paths)} repository(s)...")
    print(document_paths)
    for i, path in enumerate(document_paths):
        try:
            # Load the repository
            accumulated_document = executor.repository_loader(file_path=path)
            if not accumulated_document:
                print(f"[tasks.index_repository_helper] Error loading the repository with path: {path}")
                add_repository_upload_log(document_full_uri=path, log_name=RepositoryUploadStatusNames.FAILED)
                continue
            add_repository_upload_log(document_full_uri=path, log_name=RepositoryUploadStatusNames.LOADED)

            # Chunk the document
            chunks = executor.chunk_repository(connection_id=executor.connection_object.id,
                                               document=accumulated_document)
            if not chunks:
                print(f"[tasks.index_repository_helper] Error chunking the repository with path: {path}")
                add_repository_upload_log(document_full_uri=path, log_name=RepositoryUploadStatusNames.FAILED)
                continue
            add_repository_upload_log(document_full_uri=path, log_name=RepositoryUploadStatusNames.CHUNKED)

            number_of_chunks = len(chunks) if chunks else 0
            print(f"[tasks.index_repository_helper] Identified number of chunks: {number_of_chunks}")

            # Embed the repository
            doc_id, doc_uuid, error = executor.embed_repository(
                document=accumulated_document, path=path, number_of_chunks=number_of_chunks
            )
            add_repository_upload_log(document_full_uri=path, log_name=RepositoryUploadStatusNames.PROCESSED_DOCUMENT)

            if error or not doc_id or not doc_uuid:
                print(
                    f"[tasks.index_repository_helper] Error embedding the repository with path: {path} - Error: {error}")
                add_repository_upload_log(document_full_uri=path, log_name=RepositoryUploadStatusNames.FAILED)
                continue

            # Embed the document chunks
            errors = executor.embed_repository_chunks(chunks=chunks, path=path, document_id=doc_id,
                                                      document_uuid=doc_uuid)
            if errors:
                print(
                    f"[tasks.index_repository_helper] Error embedding at least one of the repository chunks with the repository path: {path} -"
                    f" Error: {errors}")
                add_repository_upload_log(document_full_uri=path,
                                          log_name=RepositoryUploadStatusNames.PARTIALLY_FAILED)
                continue
            add_repository_upload_log(document_full_uri=path, log_name=RepositoryUploadStatusNames.PROCESSED_CHUNKS)

            print(f"[tasks.index_repository_helper] Repository with path: {path} successfully indexed.")
            add_repository_upload_log(document_full_uri=path, log_name=RepositoryUploadStatusNames.COMPLETED)

        except Exception as e:
            print(f"[tasks.index_repository_helper] Error indexing the repository with path: {path} - Error: {e}")
            add_repository_upload_log(document_full_uri=path, log_name=RepositoryUploadStatusNames.FAILED)
            continue
    # make sure that the return statement is outside the loop
    return
