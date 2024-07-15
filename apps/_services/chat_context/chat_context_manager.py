from apps.assistants.models import ContextOverflowStrategyNames, Assistant


class ChatContextManager:

    # Create a summarizer prompt manager, we will pass these as a parameter to the chat system prompt

    def __init__(self):
        pass

    @staticmethod
    def forget_oldest(chat_history, max_messages):
        message = {
            "role": "system",
            "content": f"""
                ---
                **[SYSTEM]**: This conversation has more messages than you are actually able to see. Some of the
                messages has been deleted since the context window limit determined by the user has been reached.
                Therefore, please be aware of the fact that you might not be remembering some of the things the
                user has said. If you don't remember something, you can let the user know about this strategy and
                ask them to repeat the message.
                ---
            """
        }
        if len(chat_history) > max_messages:
            return chat_history[-max_messages:] + [message]
        else:
            return chat_history

    @staticmethod
    def stop_conversation(chat_history: list, max_messages):
        if len(chat_history) > max_messages:
            message = {
                "role": "system",
                "content": f"""
                    ---
                    **[SYSTEM]**: The conversation needs to be stopped. Please let the user know about the context
                    overflow and respectfully end the conversation.
                    ---
                """
            }
            chat_history = chat_history[-max_messages:] + [message]
            return chat_history
        else:
            return chat_history

    @staticmethod
    def store_as_vector(chat_history, max_messages, vectorizer_name, vectorizer_api_key):
        # TODO-VECTOR-CONTEXT-HISTORY-EMBEDDING: manage the embedding strategies here
        return chat_history

    @staticmethod
    def handle_context(
        chat_history,
        assistant: Assistant
    ):
        context_overflow_strategy = assistant.context_overflow_strategy
        max_messages = assistant.max_context_messages
        vectorizer_name = assistant.vectorizer_name
        vectorizer_api_key = assistant.vectorizer_api_key

        # This function will be called by the chat system, after every message.
        # It will check the context overflow strategy of the assistant, and handle the context accordingly.
        if context_overflow_strategy == ContextOverflowStrategyNames.FORGET:
            context_messages = ChatContextManager.forget_oldest(chat_history, max_messages)
        elif context_overflow_strategy == ContextOverflowStrategyNames.STOP:
            context_messages = ChatContextManager.stop_conversation(chat_history, max_messages)
        elif context_overflow_strategy == ContextOverflowStrategyNames.VECTORIZE:
            context_messages = ChatContextManager.store_as_vector(chat_history, max_messages, vectorizer_name, vectorizer_api_key)
        else:
            # No strategy has been set, default to forget
            context_messages = ChatContextManager.forget_oldest(chat_history, max_messages)

        return context_messages
