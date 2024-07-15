

def build_structured_tool_prompt__vectorized_context_history__query_execution_tool_prompt():

    # TODO-RETRIEVAL: As can be guessed, there are several things that needs to be considered on retrieval:
    #       - Before generative search:
    #           - The assistant needs to have a "limit" for the objects to retrieve.
    #           - The assistant needs to have a "specific graphQL query" to retrieve the objects.
    #           - The assistant needs to have an "alpha" value, determining the semantic similarity of the objects.
    #           - There can be other additional things.
    #   ...
    #   **UNLIKE KNOWLEDGE BASE FOR DOCUMENTS**, this tool is for context history retrieval, if the vectorized
    #   context retrieval has been selected for the assistant by the user.
    #   ...
    #   You need to explain the assistant how to perform the queries, and explain how to accomplish the usage

    pass
