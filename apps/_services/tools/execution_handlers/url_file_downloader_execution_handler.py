#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: url_file_downloader_execution_handler.py
#  Last Modified: 2024-09-28 00:42:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:14:46
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from apps._services.downloader.download_executor import DownloadExecutor
from config.settings import MEDIA_URL


def execute_url_file_downloader(connection_id: int, url: str):
    download_executor = DownloadExecutor(storage_id=connection_id)

    try:
        if not url.startswith("http"):
            url = f"{MEDIA_URL}{url}"
        url_file_path_response = download_executor.retrieve(url=url)
    except Exception as e:
        error = (f"[url_file_downloader_execution_handler.execute_url_file_downloader] Error occurred while "
                 f"downloading the file from the URL: {str(e)}")
        return error
    print(f"[url_file_downloader_execution_handler.execute_url_file_downloader] File downloaded successfully.")
    return url_file_path_response
