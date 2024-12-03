#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: build_metatempo_data_source_prompt.py
#  Last Modified: 2024-11-13 05:13:40
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-13 05:13:41
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
from apps.metatempo.models import MetaTempoAssistantConnection


def build_metatempo_to_assistant_data_source_prompt(assistant: Assistant):
    metatempo_to_assistant_data_sources = MetaTempoAssistantConnection.objects.filter(assistant=assistant)
    response_prompt = """
            ### **METATEMPO TRACKER CONNECTIONS:**

            '''
            """

    for i, info_feed in enumerate(metatempo_to_assistant_data_sources):
        conn: MetaTempoAssistantConnection = info_feed
        response_prompt += f"""
                [Connection ID: {conn.id}]
                    [MetaTempo Board Name: {conn.metatempo_instance.board.title}]
                    [MetaTempo Board Description: {conn.metatempo_instance.board.description or "N/A"}]
                    [Associated Project ID: {conn.metatempo_instance.board.project.id}]
                        [Associated Project Name: {conn.metatempo_instance.board.project.project_name}]
                ---
                """

    response_prompt += """
            '''

            ---

            #### **NOTE**: These are the MetaTempo Tracker <> Assistant Connections you have access. Keep these in mind
            while responding to the user's messages. If this part is EMPTY, it means that the user has
            not provided any MetaTempo Tracker <> Assistant Connections (yet), so neglect this part.

            ---
            """

    return response_prompt


def build_semantor_metatempo_to_assistant_data_source_prompt(temporary_sources: dict):
    metatempo_to_assistant_data_sources = temporary_sources.get("data_sources").get("metatempo_tracker_connections")

    response_prompt = """
            ### **METATEMPO TRACKER CONNECTIONS:**

            '''
            """

    for i, info_feed in enumerate(metatempo_to_assistant_data_sources):
        conn: MetaTempoAssistantConnection = info_feed
        response_prompt += f"""
                [Connection ID: {conn.id}]
                    [MetaTempo Board Name: {conn.metatempo_instance.board.title}]
                    [MetaTempo Board Description: {conn.metatempo_instance.board.description or "N/A"}]
                    [Associated Project ID: {conn.metatempo_instance.board.project.id}]
                        [Associated Project Name: {conn.metatempo_instance.board.project.project_name}]
                ---
                """

    response_prompt += """
            '''

            ---

            #### **NOTE**: These are the MetaTempo Tracker <> Assistant Connections you have access. Keep these in mind
            while responding to the user's messages. If this part is EMPTY, it means that the user has
            not provided any MetaTempo Tracker <> Assistant Connections (yet), so neglect this part.

            ---
            """

    return response_prompt


def build_lean_metatempo_to_assistant_data_source_prompt():
    response_prompt = """
            ### **METATEMPO TRACKER CONNECTIONS:**

            '''
            <This information is redacted because you won't need it to serve your instructions.>
            '''

            ---

            #### **NOTE**: These are the MetaTempo Tracker <> Assistant Connections you have access. Keep these in mind
            while responding to the user's messages. If this part is EMPTY, it means that the user has
            not provided any MetaTempo Tracker <> Assistant Connections (yet), so neglect this part.

            ---
            """
    return response_prompt
