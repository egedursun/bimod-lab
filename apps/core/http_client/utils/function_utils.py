#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: function_utils.py
#  Last Modified: 2024-10-08 21:36:13
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-08 21:36:14
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


def get_url_could_not_resolved_error_message(url: str) -> str:
    return (f"[function_utils.get_url_could_not_resolved_error_message] Could not guess the file extension for "
            f"the file from url: {url}")


def get_download_from_url_failed_error_message(error: str) -> str:
    return f"[DownloadExecutor.retrieve] Error downloading file from url: {error}"


def get_downloaded_item_could_not_saved_error_message(error: str) -> str:
    return f"[DownloadExecutor.retrieve] Error saving the file to the storage: {error}"


def get_transaction_could_not_saved_error_message(error: str) -> str:
    return f"[DownloadExecutor.retrieve] Error saving the transaction: {error}"

