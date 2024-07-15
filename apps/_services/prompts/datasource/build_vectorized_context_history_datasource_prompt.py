from django.contrib.auth.models import User

from apps.assistants.models import Assistant


def build_vectorized_context_history_datasource_prompt(assistant: Assistant, user: User):

    # TODO-PROMPT: In this part, there needs to be "A SINGLE KNOWLEDGE BASE" the assistant has access to,
    #           and explanations about the knowledge base.
    #   ...
    #   **THIS IS FOR THE VECTORIZED CONTEXT HISTORY RETRIEVAL ONLY**.

    pass
