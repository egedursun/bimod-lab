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
        try:
            instructions = build_context_memory_instructions_prompt()
        except Exception as e:
            instructions = "[ChatContextManager.forget_oldest] Error occurred while building the instructions prompt."
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
        try:
            instructions = build_context_memory_stop_conversation_prompt()
        except Exception as e:
            instructions = "[ChatContextManager.stop_conversation] Error occurred while building the instructions prompt."
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
        try:
            connection = ContextHistoryKnowledgeBaseConnection.objects.filter(assistant=assistant, chat=chat_object).first()
            executor = MemoryExecutor(connection=connection)
            print(f"[ChatContextManager.store_as_vector] MemoryExecutor created successfully.")
        except Exception as e:
            print(f"[ChatContextManager.store_as_vector] Error occurred while creating the MemoryExecutor: {str(e)}")
            return chat_history

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
            print(f"[ChatContextManager.store_as_vector] Combined history has been created successfully.")
            try:
                executor.index_memory(connection_id=connection.id,
                                      message_text=combined_history)
                print(f"[ChatContextManager.store_as_vector] Memory has been indexed successfully.")
            except Exception as e:
                print(f"[ChatContextManager.store_as_vector] Error occurred while indexing the memory: {str(e)}")
                return chat_history[-max_messages:]

            try:
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
            except Exception as e:
                print(f"[ChatContextManager.store_as_vector] Error occurred while saving the transaction: {str(e)}")
                return chat_history[-max_messages:]
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
        print(f"[ChatContextManager.handle_context] Context overflow strategy: {context_overflow_strategy}")

        # This function will be called by the chat system, after every message.
        # It will check the context overflow strategy of the assistant, and handle the context accordingly.
        if context_overflow_strategy == ContextOverflowStrategyNames.FORGET:
            try:
                context_messages = ChatContextManager.forget_oldest(chat_history, max_messages)
                print(f"[ChatContextManager.handle_context] Context has been handled successfully by forgetting the oldest messages.")
            except Exception as e:
                print(f"[ChatContextManager.handle_context] Error occurred while forgetting the oldest messages: {str(e)}")
                context_messages = chat_history
        elif context_overflow_strategy == ContextOverflowStrategyNames.STOP:
            try:
                context_messages = ChatContextManager.stop_conversation(chat_history, max_messages)
                print(f"[ChatContextManager.handle_context] Context has been handled successfully by stopping the conversation.")
            except Exception as e:
                print(f"[ChatContextManager.handle_context] Error occurred while stopping the conversation: {str(e)}")
                context_messages = chat_history
        elif context_overflow_strategy == ContextOverflowStrategyNames.VECTORIZE:
            try:
                context_messages = ChatContextManager.store_as_vector(
                    assistant=assistant,
                    chat_history=chat_history,
                    chat_object=chat_object,
                    max_messages=max_messages
                )
                print(f"[ChatContextManager.handle_context] Context has been handled successfully by storing the context as vector.")
            except Exception as e:
                print(f"[ChatContextManager.handle_context] Error occurred while storing the context as vector: {str(e)}")
                context_messages = chat_history
        else:
            # No strategy has been set, default to forget
            try:
                context_messages = ChatContextManager.forget_oldest(chat_history, max_messages)
                print(f"[ChatContextManager.handle_context] Context has been handled successfully by forgetting the oldest messages.")
            except Exception as e:
                print(f"[ChatContextManager.handle_context] Error occurred while forgetting the oldest messages: {str(e)}")
                context_messages = chat_history
        print(f"[ChatContextManager.handle_context] Returning the context messages.")
        return context_messages
