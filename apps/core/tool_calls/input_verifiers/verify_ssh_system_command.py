#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: verify_ssh_system_command.py
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
#   For permission inquiries, please contact: admin@Bimod.io.
#


def verify_ssh_system_command_content(content: dict):

    if "parameters" not in content:
        return """
            The 'parameters' field is missing from the tool_usage_json. This field is mandatory for using the File System
            Command Execution tool. Please make sure you are defining the 'parameters' field in the tool_usage_json.
        """

    ps = content.get("parameters")

    if "file_system_connection_id" not in ps:
        return """
            The 'file_system_connection_id' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the File System Command Execution tool. Please make sure you are defining the 'file_system_connection_id' field in the
            parameters field of the tool_usage_json.
        """

    if "commands" not in ps:
        return """
            The 'commands' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the File System Command Execution tool. Please make sure you are defining the 'commands' field in the
            parameters field of the tool_usage_json.
        """

    if not isinstance(ps.get("commands"), list):
        return """
            The 'commands' field in the 'parameters' field of the tool_usage_json is not a list. This field should be a list of strings
            that you would like to execute on the file system. Please make sure you are defining the 'commands' field as a list of strings
            in the parameters field of the tool_usage_json.
        """

    if not all(isinstance(command, str) for command in ps.get("commands")):
        return """
            The 'commands' field in the 'parameters' field of the tool_usage_json is not a list of strings. This field should be a list of strings
            that you would like to execute on the file system. Please make sure you are defining the 'commands' field as a list of strings
            in the parameters field of the tool_usage_json.
        """

    return None
