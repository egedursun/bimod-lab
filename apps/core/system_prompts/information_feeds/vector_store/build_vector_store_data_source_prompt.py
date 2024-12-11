#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: build_knowledge_base_data_source_prompt.py
#  Last Modified: 2024-10-05 02:25:59
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


from apps.assistants.models import Assistant

from apps.datasource_knowledge_base.models import (
    DocumentKnowledgeBaseConnection
)


def build_vector_store_data_source_prompt(assistant: Assistant):
    knowledge_base_data_sources = DocumentKnowledgeBaseConnection.objects.filter(
        assistant=assistant
    )

    response_prompt = """
            ### **KNOWLEDGE BASE CONNECTIONS:**

            '''
            """

    for i, knowledge_base_data_source in enumerate(knowledge_base_data_sources):
        kb: DocumentKnowledgeBaseConnection = knowledge_base_data_source

        response_prompt += f"""
                [Knowledge Base Data Source ID: {kb.id}]
                    System Provider: {kb.provider}
                    Knowledge Base Name: {kb.name}
                    Knowledge Base Class Name: {kb.class_name}
                    Knowledge Base Description: {kb.description or "N/A"}
                    Number of Documents in it: {kb.knowledge_base_documents.count()}
                    Size of Chunk in a Doc (tokens): {kb.embedding_chunk_size}
                    Overlaps of Each Chunk in Each Doc (tokens): {kb.embedding_chunk_overlap}
                    Maximum Records to Retrieve / Query (LIMIT): {kb.search_instance_retrieval_limit}

                """

    response_prompt += """
            '''

            ---

            #### **NOTE**: These are the Knowledge Base Connections you have access. Keep these in mind while
            responding  to user. If this part is EMPTY, it means that the user has not provided any Knowledge Base
            Connections (yet), so neglect this part.

            #### **NOTE ABOUT RETRIEVAL LIMITS**: The user has specified limits for 'read' operations within
            the 'Maximum Records to Retrieve per Query (LIMIT)' field. This is already handled in the background,
            so you don't need to define it. Yet, the limit is still shared so that you can think of a strategy to
            form multiple queries if you think one search would not be enough to retrieve enough data.

            #### **VERY IMPORTANT NOTE ABOUT 'DOCUMENT' KNOWLEDGE BASES:**
            - IF the user asks you about a certain topic, person, issue, or anything that is not within your own
            knowledge, instead of telling the user 'YOU DONT KNOW', 'USE' the knowledge base to see if you can
            find something relevant to the question.

            ---
            """

    return response_prompt


def build_semantor_vector_store_data_source_prompt(temporary_sources: dict):
    knowledge_base_data_sources = temporary_sources.get("data_sources").get("knowledge_bases")

    response_prompt = """
            ### **KNOWLEDGE BASE CONNECTIONS:**

            '''
            """

    for i, knowledge_base_data_source in enumerate(knowledge_base_data_sources):
        kb: DocumentKnowledgeBaseConnection = knowledge_base_data_source

        response_prompt += f"""
                [Knowledge Base Data Source ID: {kb.id}]
                    System Provider: {kb.provider}
                    Knowledge Base Name: {kb.name}
                    Knowledge Base Class Name: {kb.class_name}
                    Knowledge Base Description: {kb.description or "N/A"}
                    Number of Documents in it: {kb.knowledge_base_documents.count()}
                    Size of Chunk in a Doc (tokens): {kb.embedding_chunk_size}
                    Overlaps of Each Chunk in Each Doc (tokens): {kb.embedding_chunk_overlap}
                    Maximum Records to Retrieve / Query (LIMIT): {kb.search_instance_retrieval_limit}

                """

    response_prompt += """
            '''

            ---

            #### **NOTE**: These are the Knowledge Base Connections you have access. Keep these in mind while
            responding  to user. If this part is EMPTY, it means that the user has not provided any Knowledge Base
            Connections (yet), so neglect this part.

            #### **NOTE ABOUT RETRIEVAL LIMITS**: The user has specified limits for 'read' operations within
            the 'Maximum Records to Retrieve per Query (LIMIT)' field. This is already handled in the background,
            so you don't need to define it. Yet, the limit is still shared so that you can think of a strategy to
            form multiple queries if you think one search would not be enough to retrieve enough data.

            #### **VERY IMPORTANT NOTE ABOUT 'DOCUMENT' KNOWLEDGE BASES:**
            - IF the user asks you about a certain topic, person, issue, or anything that is not within your own
            knowledge, instead of telling the user 'YOU DONT KNOW', 'USE' the knowledge base to see if you can
            find something relevant to the question.

            ---
            """

    return response_prompt


def build_lean_vector_store_data_source_prompt():
    response_prompt = """
            ### **KNOWLEDGE BASE CONNECTIONS:**

            '''
            <This information is redacted because you won't need it to serve your instructions.>
            '''

            ---

            #### **NOTE**: These are the Knowledge Base Connections you have access. Keep these in mind while
            responding  to user. If this part is EMPTY, it means that the user has not provided any Knowledge Base
            Connections (yet), so neglect this part.

            #### **NOTE ABOUT RETRIEVAL LIMITS**: The user has specified limits for 'read' operations within
            the 'Maximum Records to Retrieve per Query (LIMIT)' field. This is already handled in the background,
            so you don't need to define it. Yet, the limit is still shared so that you can think of a strategy to
            form multiple queries if you think one search would not be enough to retrieve enough data.

            #### **VERY IMPORTANT NOTE ABOUT 'DOCUMENT' KNOWLEDGE BASES:**
            - IF the user asks you about a certain topic, person, issue, or anything that is not within your own
            knowledge, instead of telling the user 'YOU DONT KNOW', 'USE' the knowledge base to see if you can
            find something relevant to the question.

            ---

            """
    return response_prompt
