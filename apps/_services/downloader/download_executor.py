import uuid

from apps._services.config.costs_map import ToolCostsMap
from apps.datasource_media_storages.models import DataSourceMediaStorageConnection, DataSourceMediaStorageItem
import requests
import filetype

from apps.llm_transaction.models import LLMTransaction, TransactionSourcesNames


class DownloadExecutor:

    def __init__(self, storage_id: int):
        storage_connection = None
        try:
            storage_connection = DataSourceMediaStorageConnection.objects.get(id=storage_id)
            if not storage_connection:
                print(f"Storage with ID: {storage_id} does not exist")
        except Exception as e:
            print(f"Error getting storage connection: {e}")
        self.storage = storage_connection

    def generate_downloaded_file_name(self, url: str):
        uuid_name = str(uuid.uuid4())
        uuid_name_2 = str(uuid.uuid4())
        merged_name = f"{uuid_name}_{uuid_name_2}"
        return merged_name

    def retrieve(self, url: str):
        # download file from url
        try:
            response = requests.get(url)
            guess_extension = str(filetype.guess(response.content).extension)
            if not guess_extension:
                print(f"Could not guess the file extension for the file from url: {url}")
                return None
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error downloading file from url: {e}")
            return None

        # save the file to the storage
        generated_file_name = self.generate_downloaded_file_name(url)
        media_storage_item = DataSourceMediaStorageItem.objects.create(
            storage_base=self.storage,
            media_file_name=generated_file_name,
            media_file_size=len(response.content),
            media_file_type=guess_extension,
            file_bytes=response.content
        )
        media_storage_item.save()

        transaction = LLMTransaction(
            organization=self.storage.assistant.organization,
            model=self.storage.assistant.llm_model,
            responsible_user=None,
            responsible_assistant=self.storage.assistant,
            encoding_engine="cl100k_base",
            llm_cost=ToolCostsMap.DownloadExecutor.COST,
            transaction_type="system",
            transaction_source=TransactionSourcesNames.DOWNLOAD_FILE,
            is_tool_cost=True
        )
        transaction.save()

        # return the file path
        return media_storage_item.full_file_path
