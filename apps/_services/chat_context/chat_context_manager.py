from apps._services.config.costs_map import ToolCostsMap
from apps._services.knowledge_base.memory.memory_executor import MemoryExecutor
from apps._services.prompts.context_memory.build_context_memory_instruction import \
    build_context_memory_instructions_prompt, build_context_memory_stop_conversation_prompt
from apps.assistants.models import ContextOverflowStrategyNames, Assistant
from apps.llm_transaction.models import LLMTransaction, TransactionSourcesNames


class ChatContextManager:
    def __init__(self):
        pass

    @staticmethod
    def forget_oldest(chat_history, max_messages):
        from apps._services.llms.openai import ChatRoles
        instructions = build_context_memory_instructions_prompt()
        message = {
            "role": ChatRoles.SYSTEM,
            "content": instructions
        }
        if len(chat_history) > max_messages:
            return chat_history[-max_messages:] + [message]
        else:
            return chat_history

    @staticmethod
    def stop_conversation(chat_history: list, max_messages):
        from apps._services.llms.openai import ChatRoles
        instructions = build_context_memory_stop_conversation_prompt()
        if len(chat_history) > max_messages:
            message = {
                "role": ChatRoles.SYSTEM,
                "content": instructions
            }
            chat_history = chat_history[-max_messages:] + [message]
            return chat_history
        else:
            return chat_history

    @staticmethod
    def store_as_vector(assistant, chat_history, max_messages,
                        chat_object):
        from apps._services.llms.openai import ChatRoles, GPT_DEFAULT_ENCODING_ENGINE
        from apps.datasource_knowledge_base.models import ContextHistoryKnowledgeBaseConnection
        connection = ContextHistoryKnowledgeBaseConnection.objects.filter(assistant=assistant, chat=chat_object).first()
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
                                  message_text=combined_history)

            transaction = LLMTransaction(
                organization=chat_object.assistant.organization,
                model=chat_object.assistant.llm_model,
                responsible_user=chat_object.user,
                responsible_assistant=chat_object.assistant,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                llm_cost=ToolCostsMap.ContextMemory.COST,
                transaction_type=ChatRoles.SYSTEM,
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
        chat_object
    ):
        context_overflow_strategy = assistant.context_overflow_strategy
        max_messages = assistant.max_context_messages

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
                max_messages=max_messages
            )
        else:
            # No strategy has been set, default to forget
            context_messages = ChatContextManager.forget_oldest(chat_history, max_messages)
        return context_messages
