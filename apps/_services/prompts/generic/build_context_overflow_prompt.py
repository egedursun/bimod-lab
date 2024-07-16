from apps.assistants.models import Assistant


def get_structured_context_overflow_prompt(assistant: Assistant):
    return f"""
        **CONTEXT OVERFLOW MANAGEMENT**

        To prevent you from getting overwhelmed regarding your context window, we have set up a strategy
        for the users to set a limit on the number of messages that you can store in your memory and determining
        what to do when the limit is reached. The strategy that has been set for you is as follows:

        '''
        Strategy: {assistant.context_overflow_strategy}
        Maximum Messages: {assistant.max_context_messages}
        '''

        - **Stop Conversation**: When the limit is reached, the conversation will be stopped with the user. You will
        learn about this with a system message. If you get such a message, please let the user know about the context
        overflow and respectfully end the conversation.

        - **Forget Oldest Messages**: When the limit is reached, the oldest messages will be forgotten and the new
        messages will be stored. This will help you to keep the conversation going without any interruptions. If you
        don't remember something, you can let the user know about this strategy and ask them to repeat the message.

        - **Store as Vector**: When the limit is reached, the messages will be stored in the vector store.
        IF AND ONLY IF this strategy is set, the overflowed chat messages will be stored in the vector store
        that you can use to refer back to the messages. If you have such a strategy, you can refer to the relevant
        section (defined as a 'TOOL') in your prompt to understand how to use it.

        ---

    """
