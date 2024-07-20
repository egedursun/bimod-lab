from apps._services.downloader.download_executor import DownloadExecutor
from apps.datasource_media_storages.models import DataSourceMediaStorageConnection


def execute_url_file_downloader(connection_id: int, url: str):
    download_executor = DownloadExecutor(storage_id=connection_id)
    url_file_path_response = download_executor.retrieve(url=url)
    return url_file_path_response
