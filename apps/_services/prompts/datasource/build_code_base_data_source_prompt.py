

from apps.assistants.models import Assistant
from apps.datasource_codebase.models import CodeRepositoryStorageConnection


def build_code_base_data_source_prompt(assistant: Assistant):
    # Gather the Code Base Storage datasource connections of the assistant
    knowledge_base_data_sources = CodeRepositoryStorageConnection.objects.filter(assistant=assistant)
    # Build the prompt
    response_prompt = """
            **CODE BASE STORAGE CONNECTIONS:**

            '''
            """

    for i, knowledge_base_data_source in enumerate(knowledge_base_data_sources):
        kb:CodeRepositoryStorageConnection = knowledge_base_data_source
        response_prompt += f"""
                [Code Base Storage ID: {kb.id}]
                    System Provider: {kb.provider}
                    Code Base Storage Name: {kb.name}
                    Code Base Class Name: {kb.class_name}
                    Code Base Description: {kb.description}
                    Number of Repositories in the Code Base Storage: {kb.code_base_repositories.count()}
                    Size of Each Chunk in Each Repository (tokens): {kb.embedding_chunk_size}
                    Overlaps of Each Chunk in Each Repository (tokens): {kb.embedding_chunk_overlap}
                    Maximum Records to Retrieve per Query (LIMIT): {kb.search_instance_retrieval_limit}

                """

    response_prompt += """
            -------

            '''

            **NOTE**: These are the Code Base Storage Connections you have access to. Make sure to keep these in mind
            while responding to the user's messages. If this part is EMPTY, it means that the user has
            not provided any Code Base Storage Connections (yet), so neglect this part if that is the case.

            **NOTE about RETRIEVAL LIMITS**: The user has specified limits for 'read' operations within
            the 'Maximum Records to Retrieve per Query (LIMIT)' field. This is already handled in the background,
            so you don't need to define it yourself. However, the limit is still shared with you so that you can
            think of a strategy to form multiple queries if you think a single search would not be enough to
            retrieve the data you need.

            **VERY IMPORTANT NOTE ABOUT 'REPOSITORIES' IN CODE BASE STORAGES: **
            - IF the user asks you about a certain topic, person, issue, or anything that is not within your own
            knowledge, instead of telling the user 'YOU DONT KNOW', 'USE' the code base storage to see if you can
            find something relevant to the user's question. This is much more helpful for the user.

            -------
            """

    return response_prompt


def build_lean_code_base_data_source_prompt():
    # Build the prompt
    response_prompt = """
            **CODE BASE STORAGE CONNECTIONS:**

            '''
            <This information is redacted because you won't need it to serve your instructions.>
            '''

            **NOTE**: These are the Code Base Storage Connections you have access to. Make sure to keep these in mind
            while responding to the user's messages. If this part is EMPTY, it means that the user has
            not provided any Knowledge Base Connections (yet), so neglect this part if that is the case.

            **NOTE about RETRIEVAL LIMITS**: The user has specified limits for 'read' operations within
            the 'Maximum Records to Retrieve per Query (LIMIT)' field. This is already handled in the background,
            so you don't need to define it yourself. However, the limit is still shared with you so that you can
            think of a strategy to form multiple queries if you think a single search would not be enough to
            retrieve the data you need.

            **VERY IMPORTANT NOTE ABOUT 'REPOSITORIES' IN CODE BASE STORAGES:**
            - IF the user asks you about a certain topic, person, issue, or anything that is not within your own
            knowledge, instead of telling the user 'YOU DONT KNOW', 'USE' the code base storage to see if you can
            find something relevant to the user's question. This is much more helpful for the user.

            -------
            """
    return response_prompt
