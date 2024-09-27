def add_document_upload_log(document_full_uri, log_name):
    from apps.datasource_knowledge_base.models import DocumentProcessingLog
    DocumentProcessingLog.objects.create(
        document_full_uri=document_full_uri,
        log_message=log_name
    )
