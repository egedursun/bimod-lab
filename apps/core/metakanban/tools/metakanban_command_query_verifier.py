#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: metakanban_command_query_verifier.py
#  Last Modified: 2024-10-27 20:11:42
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-27 20:11:43
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from apps.core.metakanban.utils import (
    MetaKanbanCommandTypes
)


def verify_metakanban_command_query_content(content: dict):
    if "parameters" not in content:
        return """
            The 'parameters' field is missing from the tool_usage_json. This field is mandatory for using the Meta Kanban
            Command Execution tool. Please make sure you are defining the 'parameters' field in the tool_usage_json.
        """

    ps = content.get("parameters")

    if "action_type" not in ps:
        return """
            The 'action_type' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory
            for using the Meta Kanban Command Execution tool. Please make sure you are defining the 'action_type' field in the
            parameters field of the tool_usage_json.
        """

    if ps.get("action_type") not in MetaKanbanCommandTypes.as_list():
        return f"""
            The 'action_type' field in the 'parameters' field of the tool_usage_json must be one of these values:
            {MetaKanbanCommandTypes.as_list()}. This field is mandatory for using the Meta Kanban Command Execution tool.
            Please make sure you are defining the 'action_type' field in the parameters field of the tool_usage_json.
        """

    if "action_content" not in ps:
        return """
            The 'action_content' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory
            for using the Meta Kanban Command Execution tool. Please make sure you are defining the 'action_content' field in the
            parameters field of the tool_usage_json.
        """

    if type(ps.get("action_content")) is not dict:
        return """
            The 'action_content' field in the 'parameters' field of the tool_usage_json must be a dictionary. This field is
            mandatory for using the Meta Kanban Command Execution tool. Please make sure you are defining the 'action_content' field in
            the parameters field of the tool_usage_json.
        """

    return None
