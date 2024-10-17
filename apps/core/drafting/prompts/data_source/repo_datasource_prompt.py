#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: repo_datasource_prompt.py
#  Last Modified: 2024-10-16 23:44:35
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-16 23:44:36
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
from apps.datasource_codebase.models import CodeRepositoryStorageConnection


def build_drafting_code_base_data_source_prompt(assistant: Assistant):
    code_base_data_sources = CodeRepositoryStorageConnection.objects.filter(assistant=assistant)
    response_prompt = """
            ### **CODE BASE STORAGE CONNECTIONS:**

            '''
            """

    for i, code_base_info_feed in enumerate(code_base_data_sources):
        kb: CodeRepositoryStorageConnection = code_base_info_feed
        response_prompt += f"""
                [Code Base Storage ID: {kb.id}]
                    System Provider: {kb.provider}
                    Code Base Storage Name: {kb.name}
                    Code Base Class Name: {kb.class_name}
                    Code Base Description: {kb.description}
                    Number of Repos in Storage: {kb.code_base_repositories.count()}
                    Size of Chunks in Each Repo (tokens): {kb.embedding_chunk_size}
                    Overlaps of Each Chunk in Repos (tokens): {kb.embedding_chunk_overlap}
                    Maximum Records to Retrieve / Query (LIMIT): {kb.search_instance_retrieval_limit}

                """

    response_prompt += """
            '''

            ---

            #### **NOTE**: These are the Code Base Storage Connections you have access. Keep these in mind
            while responding to the user's messages. If this part is EMPTY, it means that the user has
            not provided any Code Base Storage Connections (yet), so neglect this part.

            #### **NOTE ABOUT RETRIEVAL LIMITS**: The user has specified limits for 'read' operations within
            the 'Maximum Records to Retrieve / Query (LIMIT)' field. This is handled in the background, so you don't
            need to define it yourself. Yet, the limit is still shared with you so that you can think of a strategy
            to form multiple queries if you think a single search would not be enough to have enough data.

            #### **IMPORTANT NOTE ABOUT 'REPOSITORIES' IN CODE BASE STORAGES: **
            - IF the user asks you about a certain topic, person, issue, or anything that is not within your own
            knowledge, instead of telling the user 'YOU DONT KNOW', 'USE' the storages to see if you can find
            something relevant to the question.

            ---
            """

    return response_prompt
