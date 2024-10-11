#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: download_executor.py
#  Last Modified: 2024-10-05 02:20:19
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:36
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#


import uuid

from apps.core.http_client.utils import get_url_could_not_resolved_error_message, \
    get_download_from_url_failed_error_message, get_downloaded_item_could_not_saved_error_message, \
    get_transaction_could_not_saved_error_message
from apps.core.internal_cost_manager.costs_map import InternalServiceCosts
from apps.datasource_media_storages.models import DataSourceMediaStorageConnection, DataSourceMediaStorageItem
import requests
import filetype

from apps.llm_transaction.models import LLMTransaction
from apps.llm_transaction.utils import LLMTransactionSourcesTypesNames


class HTTPClientDownloadExecutor:

    def __init__(self, storage_id: int):
        c = None
        try:
            c = DataSourceMediaStorageConnection.objects.get(id=storage_id)
            if not c:
                pass
        except Exception as e:
            pass
        self.storage = c

    def retrieve(self, url: str):
        from apps.core.generative_ai.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps.core.generative_ai.utils import ChatRoles
        try:
            http_response = requests.get(url)
            estimate_format = str(filetype.guess(http_response.content).extension)
            if not estimate_format:
                return get_url_could_not_resolved_error_message(url)
            http_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return get_download_from_url_failed_error_message(str(e))

        try:
            file_name = self.generate_name_http_download()
            item = DataSourceMediaStorageItem.objects.create(
                storage_base=self.storage, media_file_name=file_name, media_file_size=len(http_response.content),
                media_file_type=estimate_format, file_bytes=http_response.content)
            item.save()
        except Exception as e:
            return get_downloaded_item_could_not_saved_error_message(str(e))

        try:
            tx = LLMTransaction(
                organization=self.storage.assistant.organization, model=self.storage.assistant.llm_model,
                responsible_user=None, responsible_assistant=self.storage.assistant,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE, llm_cost=InternalServiceCosts.DownloadExecutor.COST,
                transaction_type=ChatRoles.SYSTEM, transaction_source=LLMTransactionSourcesTypesNames.DOWNLOAD_FILE,
                is_tool_cost=True)
            tx.save()
        except Exception as e:
            return get_transaction_could_not_saved_error_message(str(e))
        return item.full_file_path

    @staticmethod
    def generate_name_http_download():
        try:
            uuid_1 = str(uuid.uuid4())
            uuid_2 = str(uuid.uuid4())
            final_uuid = f"{uuid_1}_{uuid_2}"
        except Exception as e:
            return None
        return final_uuid
