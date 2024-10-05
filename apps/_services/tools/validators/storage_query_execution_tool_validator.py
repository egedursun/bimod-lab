#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: storage_query_execution_tool_validator.py
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


def validate_media_storage_query_execution_tool_json(tool_usage_json: dict):
    if "parameters" not in tool_usage_json:
        return """
            The 'parameters' field is missing from the tool_usage_json. This field is mandatory for using the Media Storage
            Query Execution tool. Please make sure you are defining the 'parameters' field in the tool_usage_json.
        """
    parameters = tool_usage_json.get("parameters")

    if "media_storage_connection_id" not in parameters:
        return """
            The 'media_storage_connection_id' field is missing from the 'parameters' field in the tool_usage_json. This
            field is mandatory for using the Media Storage Query Execution tool. Please make sure you are defining the
            'media_storage_connection_id' field in the parameters field of the tool_usage_json.
        """

    if "query" not in parameters:
        return """
            The 'query' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the Media Storage Query Execution tool. Please make sure you are defining the 'query' field in the
            parameters field of the tool_usage_json.
        """

    if "type" not in parameters:
        return """
            The 'type' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the Media Storage Query Execution tool. Please make sure you are defining the 'type' field in the
            parameters field of the tool_usage_json. The available types are "file_interpretation" and
            "image_interpretation".
        """

    if parameters.get("type") not in ["file_interpretation", "image_interpretation"]:
        return """
            The 'type' field in the 'parameters' field of the tool_usage_json must either be 'file_interpretation' or
            'image_interpretation'. This field is mandatory for using the Media Storage Query Execution tool. Please make
            sure you are defining the 'type' field in the parameters field of the tool_usage_json.
        """

    if "file_paths" not in parameters:
        return """
            The 'file_paths' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory
            for using the Media Storage Query Execution tool. Please make sure you are defining the 'file_paths' field in
            the parameters field of the tool_usage_json.
        """

    if not isinstance(parameters.get("file_paths"), list):
        return """
            The 'file_paths' field in the 'parameters' field of the tool_usage_json must be a list. This field is
            mandatory for using the Media Storage Query Execution tool. Please make sure you are defining the 'file_paths'
            field in the parameters field of the tool_usage_json.
        """
    print(
        f"[media_storage_query_execution_tool_validator.validate_media_storage_query_execution_tool_json] Validation is successful.")
    return None
