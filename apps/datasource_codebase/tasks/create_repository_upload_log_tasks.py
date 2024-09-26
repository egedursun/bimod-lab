def add_repository_upload_log(document_full_uri, log_name):
    from apps.datasource_codebase.models import RepositoryProcessingLog
    RepositoryProcessingLog.objects.create(
        repository_full_uri=document_full_uri,
        log_message=log_name
    )
