#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: build_hadron_prime_node_data_source_prompt.py
#  Last Modified: 2024-11-13 05:13:11
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-13 05:13:11
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
from apps.hadron_prime.models import HadronNodeAssistantConnection


def build_hadron_prime_node_to_assistant_data_source_prompt(assistant: Assistant):
    node_to_assistant_data_sources = HadronNodeAssistantConnection.objects.filter(assistant=assistant)
    response_prompt = """
            ### **HADRON PRIME NODE CONNECTIONS:**

            '''
            """

    for i, node_info_feed in enumerate(node_to_assistant_data_sources):
        conn: HadronNodeAssistantConnection = node_info_feed
        response_prompt += f"""
                [Connection ID: {conn.id}]
                    [Hadron Node Name: {conn.hadron_prime_node.node_name}]
                    [Hadron Node Description: {conn.hadron_prime_node.node_description or "N/A"}]
                ---
                """

    response_prompt += """
            '''

            ---

            #### **NOTE**: These are the Hadron Prime Node <> Assistant Connections you have access. Keep these in mind
            while responding to the user's messages. If this part is EMPTY, it means that the user has
            not provided any Hadron Prime Node <> Assistant Connections (yet), so neglect this part.

            ---
            """

    return response_prompt


def build_semantor_hadron_prime_node_to_assistant_data_source_prompt(temporary_sources: dict):
    node_to_assistant_data_sources = temporary_sources.get("data_sources").get("hadron_node_connections")

    response_prompt = """
            ### **HADRON PRIME NODE CONNECTIONS:**

            '''
            """

    for i, node_info_feed in enumerate(node_to_assistant_data_sources):
        conn: HadronNodeAssistantConnection = node_info_feed
        response_prompt += f"""
                [Connection ID: {conn.id}]
                    [Hadron Node Name: {conn.hadron_prime_node.node_name}]
                    [Hadron Node Description: {conn.hadron_prime_node.node_description or "N/A"}]
                ---
                """

    response_prompt += """
            '''

            ---

            #### **NOTE**: These are the Hadron Prime Node <> Assistant Connections you have access. Keep these in mind
            while responding to the user's messages. If this part is EMPTY, it means that the user has
            not provided any Hadron Prime Node <> Assistant Connections (yet), so neglect this part.

            ---
            """

    return response_prompt


def build_lean_hadron_prime_node_to_assistant_data_source_prompt():
    response_prompt = """
            ### **HADRON PRIME NODE CONNECTIONS:**

            '''
            <This information is redacted because you won't need it to serve your instructions.>
            '''

            ---

            #### **NOTE**: These are the Hadron Prime Node <> Assistant Connections you have access. Keep these in mind
            while responding to the user's messages. If this part is EMPTY, it means that the user has
            not provided any Hadron Prime Node <> Assistant Connections (yet), so neglect this part.

            ---
            """
    return response_prompt
