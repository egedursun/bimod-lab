#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: function_utils.py
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

def get_no_knowledge_base_connection_error_log(assistant_name, chat_name):
    return f"""
        The Context History Knowledge Base Connection for the chat: {chat_name} and assistant: {assistant_name}
        does not exist in the system. Please make sure you have the connection setup in the system.
    """


def get_no_tool_found_error_log(query_name):
    return f"""
        There is no tool with the name: {query_name} in the system. Please make sure you are defining
        the correct tool name in the tool_usage_json.
    """
