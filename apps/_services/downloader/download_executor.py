import uuid

from apps._services.config.costs_map import ToolCostsMap
from apps.datasource_media_storages.models import DataSourceMediaStorageConnection, DataSourceMediaStorageItem
import requests
import filetype

from apps.llm_transaction.models import LLMTransaction
from apps.llm_transaction.utils import TransactionSourcesNames


class DownloadExecutor:

    def __init__(self, storage_id: int):
        storage_connection = None
        try:
            storage_connection = DataSourceMediaStorageConnection.objects.get(id=storage_id)
            if not storage_connection:
                print(f"Storage with ID: {storage_id} does not exist")
        except Exception as e:
            print(f"[DownloadExecutor.__init__] Error getting storage connection: {e}")
        self.storage = storage_connection

    @staticmethod
    def generate_downloaded_file_name():
        try:
            uuid_name = str(uuid.uuid4())
            uuid_name_2 = str(uuid.uuid4())
            merged_name = f"{uuid_name}_{uuid_name_2}"
            print(f"[DownloadExecutor.generate_downloaded_file_name] Generated file name: {merged_name}")
        except Exception as e:
            print(f"[DownloadExecutor.generate_downloaded_file_name] Error generating the file name: {e}")
            return None
        return merged_name

    def retrieve(self, url: str):
        from apps._services.llms.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps._services.llms.utils import ChatRoles
        # download file from URL
        try:
            response = requests.get(url)
            guess_extension = str(filetype.guess(response.content).extension)
            print(f"[DownloadExecutor.retrieve] Guessed extension: {guess_extension}")
            if not guess_extension:
                return f"[DownloadExecutor.retrieve] Could not guess the file extension for the file from url: {url}"
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return f"[DownloadExecutor.retrieve] Error downloading file from url: {e}"

        # save the file to the storage
        try:
            generated_file_name = self.generate_downloaded_file_name()
            media_storage_item = DataSourceMediaStorageItem.objects.create(
                storage_base=self.storage,
                media_file_name=generated_file_name,
                media_file_size=len(response.content),
                media_file_type=guess_extension,
                file_bytes=response.content
            )
            media_storage_item.save()
            print(f"[DownloadExecutor.retrieve] File saved to the storage successfully.")
        except Exception as e:
            return f"[DownloadExecutor.retrieve] Error saving the file to the storage: {e}"

        try:
            # create a transaction
            transaction = LLMTransaction(
                organization=self.storage.assistant.organization,
                model=self.storage.assistant.llm_model,
                responsible_user=None,
                responsible_assistant=self.storage.assistant,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                llm_cost=ToolCostsMap.DownloadExecutor.COST,
                transaction_type=ChatRoles.SYSTEM,
                transaction_source=TransactionSourcesNames.DOWNLOAD_FILE,
                is_tool_cost=True
            )
            transaction.save()
            print(f"[DownloadExecutor.retrieve] Transaction saved successfully.")
        except Exception as e:
            return f"[DownloadExecutor.retrieve] Error saving the transaction: {e}"
        return media_storage_item.full_file_path
