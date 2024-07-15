from django.contrib.auth.models import User

from apps.assistants.models import Assistant


def build_knowledge_base_datasource_prompt(assistant: Assistant, user: User):

    # TODO-PROMPT: In this part, there needs to be the lists of knowledge bases the assistant has access to,
    #           and explanations about the knowledge bases. The assistant should be able to see the knowledge
    #           base ID, the name of the knowledge base, the description of the knowledge base, and the schema
    #           of the knowledge base. If the assistant has access to custom queries, the assistant should also
    #           be able to see the custom queries of the knowledge base, including the custom query ID, the name
    #           of the custom query, the description of the custom query, and the SQL query of the custom query.

    pass
