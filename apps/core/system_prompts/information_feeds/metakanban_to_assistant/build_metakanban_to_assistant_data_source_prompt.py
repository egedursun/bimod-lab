#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: build_metakanban_data_source_prompt.py
#  Last Modified: 2024-11-13 05:13:27
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-13 05:13:27
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
from apps.assistants.models import Assistant
from apps.metakanban.models import MetaKanbanAssistantConnection


def build_metakanban_to_assistant_data_source_prompt(assistant: Assistant):
    metakanban_to_assistant_data_sources = MetaKanbanAssistantConnection.objects.filter(assistant=assistant)
    response_prompt = """
            ### **METAKANBAN BOARD CONNECTIONS:**

            '''
            """

    for i, info_feed in enumerate(metakanban_to_assistant_data_sources):
        conn: MetaKanbanAssistantConnection = info_feed
        response_prompt += f"""
                [Connection ID: {conn.id}]
                    [MetaKanban Board Name: {conn.metakanban_board.title}]
                    [MetaKanban Board Description: {conn.metakanban_board.description or "N/A"}]
                    [Associated Project ID: {conn.metakanban_board.project.id}]
                        [Associated Project Name: {conn.metakanban_board.project.project_name}]
                ---
                """

    response_prompt += """
            '''

            ---

            #### **NOTE**: These are the MetaKanban Board <> Assistant Connections you have access. Keep these in mind
            while responding to the user's messages. If this part is EMPTY, it means that the user has
            not provided any MetaKanban Board <> Assistant Connections (yet), so neglect this part.

            ---
            """

    return response_prompt


def build_semantor_metakanban_to_assistant_data_source_prompt(temporary_sources: dict):
    metakanban_to_assistant_data_sources = temporary_sources.get("data_sources").get("metakanban_board_connections")

    response_prompt = """
            ### **METAKANBAN BOARD CONNECTIONS:**

            '''
            """

    for i, info_feed in enumerate(metakanban_to_assistant_data_sources):
        conn: MetaKanbanAssistantConnection = info_feed
        response_prompt += f"""
                [Connection ID: {conn.id}]
                    [MetaKanban Board Name: {conn.metakanban_board.title}]
                    [MetaKanban Board Description: {conn.metakanban_board.description or "N/A"}]
                    [Associated Project ID: {conn.metakanban_board.project.id}]
                        [Associated Project Name: {conn.metakanban_board.project.project_name}]
                ---
                """

    response_prompt += """
            '''

            ---

            #### **NOTE**: These are the MetaKanban Board <> Assistant Connections you have access. Keep these in mind
            while responding to the user's messages. If this part is EMPTY, it means that the user has
            not provided any MetaKanban Board <> Assistant Connections (yet), so neglect this part.

            ---
            """

    return response_prompt


def build_lean_metakanban_to_assistant_data_source_prompt():
    response_prompt = """
            ### **METAKANBAN BOARD CONNECTIONS:**

            '''
            <This information is redacted because you won't need it to serve your instructions.>
            '''

            ---

            #### **NOTE**: These are the MetaKanban Board <> Assistant Connections you have access. Keep these in mind
            while responding to the user's messages. If this part is EMPTY, it means that the user has
            not provided any MetaKanban Board <> Assistant Connections (yet), so neglect this part.

            ---
            """
    return response_prompt
