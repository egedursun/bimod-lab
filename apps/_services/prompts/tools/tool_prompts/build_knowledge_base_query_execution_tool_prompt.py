from apps._services.tools.utils import ToolTypeNames


def build_structured_tool_prompt__knowledge_base_query_execution():
    response_prompt = f"""
            **TOOL**: Knowledge Base Document Search Query Execution

            - The Knowledge Base Query Execution Tool is a tool you can use to search within the uploaded documents
            of the user to provide a more accurate response to the user's questions. You can try to reach any of the
            specified knowledge bases defined within the "Knowledge Base Connections" section.

            - The standardized format for the dictionary that you will output to use the Knowledge Base Query Execution
            Tool is as follows:

            '''
                {{
                    "tool": "{ToolTypeNames.KNOWLEDGE_BASE_QUERY_EXECUTION}",
                    "parameters": {{
                        "knowledge_base_connection_id": "...",
                        "query": "...",
                        "alpha": 0.0 <= value_of_alpha <= 1.0,
                        }}
                    }}
            '''

            **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

            **INSTRUCTIONS:** The "knowledge_base_connection_id" will be the ID of the Knowledge Base Connection that
            you would like to execute your query on, and the "query" will be the string that you would like to search
            within the knowledge base documents. The "alpha" parameter is a float value between 0.0 and 1.0 that
            determines the weight of semantic versus keyword-based search in the search algorithm:

            - An alpha of 1.0 means that the search will be purely vector-based (semantic) search.
            - An alpha of 0.0 means that the search will be purely keyword-based search.
            - Thus, the value of alpha can be adjusted between float values of 0.0 and 1.0 to adjust the balance
            between semantic and keyword-based search, according to the question of the user and your judgment.

            To use this tool, you need to provide the following fields for the system 'VERY CAREFULLY':

            1. The "query" field should be a string that you would like to search within the knowledge base documents.
            This string can be a question or a keyword that you would like to search within the documents.

            2. The "alpha" field should be a float value between 0.0 and 1.0 that determines the weight of semantic
            versus keyword-based search in the search algorithm.

            **NOTE**: The system will provide you with the results of the search in the next 'assistant' message.
            This message will have a list of documents that are most relevant to the query you have provided. The
            fields will include "chunk_document_file_name", which is the name of the document that contains the
            retrieved information; "chunk_number", which is the number of the chunk within the document (ordered)
            that contains the retrieved information; and "chunk_content", which is the text of the chunk that
            contains the retrieved information (which is the primary field that you will use to search answers
            for the user).

            - You are expected to take in this response, and use it to provide an answer to the user's question.

        """
    return response_prompt
