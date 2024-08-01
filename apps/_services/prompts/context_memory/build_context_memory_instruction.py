

def build_context_memory_instructions_prompt():
    context_memory_instructions = f"""
        ---
        **SYSTEM MESSAGE:**

        - This conversation has more messages than you are actually able to see. Some of the
        messages has been deleted since the context window limit determined by the user has been reached.
        Therefore, please be aware of the fact that you might not be remembering some of the things the
        user has said. If you don't remember something, you can let the user know about this strategy and
        ask them to repeat the message.
        ---
    """
    return context_memory_instructions


def build_context_memory_stop_conversation_prompt():
    stop_conversation_prompt = f"""
        ---
        **SYSTEM MESSAGE:**

        - The conversation needs to be stopped. Please let the user know about the context
        overflow and respectfully end the conversation.
        ---
    """
    return stop_conversation_prompt
