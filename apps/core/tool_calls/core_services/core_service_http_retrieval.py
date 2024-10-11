#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: core_service_http_retrieval.py
#  Last Modified: 2024-10-05 02:31:01
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:35
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#


from apps.core.http_client.http_client_download_manager import HTTPClientDownloadExecutor
from config.settings import MEDIA_URL


def run_http_retrieval(connection_id: int, url: str):
    xc = HTTPClientDownloadExecutor(storage_id=connection_id)
    try:
        if not url.startswith("http"):
            url = f"{MEDIA_URL}{url}"
        output = xc.retrieve(url=url)
    except Exception as e:
        error = f"Error occurred while downloading the file from the URL: {str(e)}"
        return error
    return output
