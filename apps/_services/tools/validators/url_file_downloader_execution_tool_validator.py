#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: url_file_downloader_execution_tool_validator.py
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
#
#


def validate_url_file_downloader_execution_tool_json(tool_usage_json: dict):
    if "parameters" not in tool_usage_json:
        return """
            The 'parameters' field is missing from the tool_usage_json. This field is mandatory for using the URL File
            Downloader tool. Please make sure you are defining the 'parameters' field in the tool_usage_json.
        """
    parameters = tool_usage_json.get("parameters")

    if "media_storage_connection_id" not in parameters:
        return """
            The 'media_storage_connection_id' field is missing from the 'parameters' field in the tool_usage_json. This
            field is mandatory for using the URL File Downloader tool. Please make sure you are defining the
            'media_storage_connection_id' field in the parameters field of the tool_usage_json.
        """

    if "url" not in parameters:
        return """
            The 'download_url' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory
            for using the URL File Downloader tool. Please make sure you are defining the 'download_url' field in the
            parameters field of the tool_usage_json.
        """
    print(
        f"[url_file_downloader_execution_tool_validator.validate_url_file_downloader_execution_tool_json] Validation is successful.")
    return None
