from apps._services.downloader.download_executor import DownloadExecutor
from config.settings import MEDIA_URL


def execute_url_file_downloader(connection_id: int, url: str):
    download_executor = DownloadExecutor(storage_id=connection_id)

    try:
        if not url.startswith("http"):
            url = f"{MEDIA_URL}{url}"
        url_file_path_response = download_executor.retrieve(url=url)
    except Exception as e:
        error = f"[url_file_downloader_execution_handler.execute_url_file_downloader] Error occurred while downloading the file from the URL: {str(e)}"
        return error
    print(f"[url_file_downloader_execution_handler.execute_url_file_downloader] File downloaded successfully.")
    return url_file_path_response
