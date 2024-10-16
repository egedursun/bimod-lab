#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: sql_command_handler.py
#  Last Modified: 2024-10-15 23:33:07
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-15 23:33:08
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#


def handle_sql_command(command: str) -> str:
    # TODO-EGE: implement (6b)
    """
        This function does the following:
        - Takes the command.
        - Creates a lean AI assistant, with as few prompt tokens as possible to avoid costs.
        - Also adds a prompt for folder configurations, document configurations, and the current status of the text.
        - Also adds a prompt for available SQL Connections for the Co-Pilot assistant.
        - Also adds a prompt for the drafting operations
        - Also adds a prompt for the specific action performed by this function.
        - Performs an SQL search in the DBs according to the thing user requested.
        - Returns the output.

        :param command:
        :return:
    """
    return f"TODO: Not implemented yet. SQL command: {command}"


def _execute_tool_query_sql(query: str):
    pass
