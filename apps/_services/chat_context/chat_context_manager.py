from apps._services.config.costs_map import ToolCostsMap
from apps._services.knowledge_base.memory.memory_executor import MemoryExecutor
from apps.assistants.models import ContextOverflowStrategyNames, Assistant
from apps.datasource_knowledge_base.models import ContextHistoryKnowledgeBaseConnection
from apps.llm_transaction.models import LLMTransaction, TransactionSourcesNames
from apps.multimodal_chat.models import MultimodalChat


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
    def store_as_vector(assistant, chat_history, max_messages, vectorizer_name, vectorizer_api_key,
                        chat_object):
        connection = ContextHistoryKnowledgeBaseConnection.objects.filter(assistant=assistant,
                                                                          chat=chat_object).first()
        executor = MemoryExecutor(connection=connection)

        if len(chat_history) > max_messages:
            combined_history = ""
            for message in chat_history[-max_messages:]:
                combined_history += f"""
                    ----------------------------------------
                    - Role: {message["role"]}
                    - Content:
                    '''
                    {message["content"]}
                    '''
                    ----------------------------------------
                """
            executor.index_memory(connection_id=connection.id,
                                  assistant_id=assistant.id,
                                  chat_id=chat_object.id,
                                  message_text=combined_history)

            transaction = LLMTransaction(
                organization=chat_object.assistant.organization,
                model=chat_object.assistant.llm_model,
                responsible_user=chat_object.user,
                responsible_assistant=chat_object.assistant,
                encoding_engine="cl100k_base",
                llm_cost=ToolCostsMap.ContextMemory.COST,
                transaction_type="system",
                transaction_source=TransactionSourcesNames.STORE_MEMORY,
                is_tool_cost=True
            )
            transaction.save()

            return chat_history[-max_messages:]
        return chat_history

    @staticmethod
    def handle_context(
        chat_history,
        assistant: Assistant,
        chat_object: MultimodalChat
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
            context_messages = ChatContextManager.store_as_vector(
                assistant=assistant,
                chat_history=chat_history,
                chat_object=chat_object,
                max_messages=max_messages,
                vectorizer_name=vectorizer_name,
                vectorizer_api_key=vectorizer_api_key
            )
        else:
            # No strategy has been set, default to forget
            context_messages = ChatContextManager.forget_oldest(chat_history, max_messages)

        return context_messages
