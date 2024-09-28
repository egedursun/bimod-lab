from apps._services.storages.storage_executor import StorageExecutor
from apps._services.tools.utils import ExecutionTypesNames
from apps.datasource_media_storages.models import DataSourceMediaStorageConnection
from apps.multimodal_chat.models import MultimodalChat


def execute_storage_query(connection_id, chat_id, execution_type, file_paths, query, without_chat=False):
    connection = DataSourceMediaStorageConnection.objects.get(id=connection_id)
    chat = None
    if without_chat is False:
        chat = MultimodalChat.objects.get(id=chat_id)
    try:
        executor = StorageExecutor(connection=connection, chat=chat)
        print(f"[storage_query_execution_handler.execute_storage_query] Executing the storage query with the "
              f"execution type: {execution_type}.")
        response, file_uris, image_uris = "", [], []
        if execution_type == ExecutionTypesNames.FILE_INTERPRETATION:
            response = executor.interpret_file(full_file_paths=file_paths, query_string=query)
            file_uris = response.get("file_uris")
            image_uris = response.get("image_uris")
        elif execution_type == ExecutionTypesNames.IMAGE_INTERPRETATION:
            response = executor.interpret_image(full_image_paths=file_paths, query_string=query)
    except Exception as e:
        error = (f"[storage_query_execution_handler.execute_storage_query] Error occurred while executing the storage "
                 f"query: {str(e)}")
        return error, [], []
    print(f"[storage_query_execution_handler.execute_storage_query] Storage query executed successfully.")
    return response, file_uris, image_uris
