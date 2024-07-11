from django.contrib.auth.models import User

from apps.assistants.models import Assistant


def build_structured_memory_prompt(assistant: Assistant, user: User):
    response_prompt = ""
    # Gather assistant-specific queries
    assistant_memories = assistant.memories.filter(memory_type="assistant-specific")
    # Gather user-specific queries
    user_memories = assistant.memories.filter(memory_type="user-specific", user=user)
    # Combine the queries
    memories = list(assistant_memories) + list(user_memories)
    # Build the prompt
    response_prompt = """
        **MEMORIES:**

        '''
        """

    for i, memory in enumerate(memories):
        response_prompt += f"[Index: {i}]: '{memory.memory_text_content}\n'"

    response_prompt += """
        '''

        **NOTE**: These are the memories that have been entered by the user for you to be careful about
        certain topics. You MUST adhere to the guidelines in these memories and always keep these in mind
        while responding to the user's messages. If this part is EMPTY, you can respond to the user's
        messages without any specific considerations.
        """

    return response_prompt
