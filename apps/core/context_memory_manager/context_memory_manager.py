#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: chat_context_manager.py
#  Last Modified: 2024-10-05 02:13:34
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:36
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
import logging

from apps.core.context_memory_manager.utils import (get_error_on_context_memory_handling_log,
                                                    get_structured_memory_contents)
from apps.core.internal_cost_manager.costs_map import InternalServiceCosts
from apps.core.vector_operations.intra_context_memory.memory_executor import IntraContextMemoryExecutor
from apps.core.system_prompts.chat_history_memory.build_chat_history_memory_instruction import \
    build_chat_history_memory_handling_prompt, build_chat_history_memory_stop_communication_handler_prompt
from apps.assistants.models import Assistant
from apps.assistants.utils import ContextManagementStrategyNames
from apps.llm_transaction.models import LLMTransaction
from apps.llm_transaction.utils import LLMTransactionSourcesTypesNames


logger = logging.getLogger(__name__)


class ContextMemoryManager:
    @staticmethod
    def forget_oldest_chat_messages(message_history, maximum_allowed_messages):
        from apps.core.generative_ai.utils import ChatRoles
        try:
            system_prompt = build_chat_history_memory_handling_prompt()
            logger.info(f"[ChatContextManager.forget_oldest_chat_messages] System prompt: {system_prompt}")
        except Exception as e:
            system_prompt = get_error_on_context_memory_handling_log(error_log=str(e))
            logger.error(f"[ChatContextManager.forget_oldest_chat_messages] Error creating system prompt: {e}")
        msg = {"role": ChatRoles.SYSTEM, "content": system_prompt}
        len_msg_history = len(message_history)
        if len_msg_history > maximum_allowed_messages:
            trimmed_msg_history = message_history[-maximum_allowed_messages:] + [msg]
            return trimmed_msg_history
        else:
            return message_history

    @staticmethod
    def stop_communication_at_threshold(message_history: list, maximum_allowed_messages):
        from apps.core.generative_ai.utils import ChatRoles
        try:
            system_prompt = build_chat_history_memory_stop_communication_handler_prompt()
            logger.info(f"[ChatContextManager.stop_communication_at_threshold] System prompt: {system_prompt}")
        except Exception as e:
            logger.error(f"[ChatContextManager.stop_communication_at_threshold] Error creating system prompt: {e}")
            system_prompt = get_error_on_context_memory_handling_log(error_log=str(e))
        len_msg_history = len(message_history)
        if len_msg_history > maximum_allowed_messages:
            msg = {"role": ChatRoles.SYSTEM, "content": system_prompt}
            trimmed_msg_history = message_history[-maximum_allowed_messages:] + [msg]
            return trimmed_msg_history
        else:
            return message_history

    @staticmethod
    def store_context_memory_as_embedding(context_agent, message_history, maximum_allowed_messages,
                                          communication_object):
        from apps.core.generative_ai.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps.core.generative_ai.utils import ChatRoles
        from apps.datasource_knowledge_base.models import ContextHistoryKnowledgeBaseConnection
        try:
            c = ContextHistoryKnowledgeBaseConnection.objects.filter(
                assistant=context_agent, chat=communication_object).first()
            x = IntraContextMemoryExecutor(connection=c)
        except Exception as e:
            logger.error(f"[ChatContextManager.store_context_memory_as_embedding] Error getting the connection: {e}")
            return message_history

        chat_history_length = len(message_history)
        if chat_history_length > maximum_allowed_messages:
            comb_msgs_history = ContextMemoryManager._generate_combined_context_history(message_history,
                                                                                       maximum_allowed_messages)
            try:
                x.index_memory(connection_id=c.id, message_text=comb_msgs_history)
                logger.info(f"[ChatContextManager.store_context_memory_as_embedding] Indexed the memory")
            except Exception as e:
                logger.error(f"[ChatContextManager.store_context_memory_as_embedding] Error indexing the memory: {e}")
                return message_history[-maximum_allowed_messages:]

            try:
                tx = LLMTransaction(
                    organization=communication_object.assistant.organization,
                    model=communication_object.assistant.llm_model, responsible_user=communication_object.user,
                    responsible_assistant=communication_object.assistant, encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                    llm_cost=InternalServiceCosts.ContextMemory.COST, transaction_type=ChatRoles.SYSTEM,
                    transaction_source=LLMTransactionSourcesTypesNames.STORE_MEMORY, is_tool_cost=True)
                tx.save()
                logger.info(f"[ChatContextManager.store_context_memory_as_embedding] Created the transaction")
            except Exception as e:
                logger.error(f"[ChatContextManager.store_context_memory_as_embedding] Error creating the transaction: {e}")
                trimmed_msgs_history = message_history[-maximum_allowed_messages:]
                return trimmed_msgs_history
            logger.info(f"[ChatContextManager.store_context_memory_as_embedding] Stored the memory")
            trimmed_msgs_history = message_history[-maximum_allowed_messages:]
            return trimmed_msgs_history
        return message_history

    @staticmethod
    def _generate_combined_context_history(chat_history, max_messages):
        comb_msgs_history = ""
        for message in chat_history[-max_messages:]:
            comb_msgs_history += get_structured_memory_contents(message=message)
        logger.info(f"[ChatContextManager._generate_combined_context_history] Combined messages.")
        return comb_msgs_history

    @staticmethod
    def handle_context(chat_history, assistant: Assistant, chat_object):
        mgm_strategy = assistant.context_overflow_strategy
        max_context_msgs = assistant.max_context_messages
        if mgm_strategy == ContextManagementStrategyNames.FORGET:
            ctx_msgs = ContextMemoryManager._handle_strategy_forget_oldest(chat_history, max_context_msgs)
        elif mgm_strategy == ContextManagementStrategyNames.STOP:
            ctx_msgs = ContextMemoryManager._handle_strategy_stop_conversation(chat_history, max_context_msgs)
        else:
            ctx_msgs = ContextMemoryManager._handle_strategy_forget_oldest(chat_history, max_context_msgs)

        # TODO: optimize the vectorization strategy, then will be uncommented
        """
        elif mgm_strategy == ContextManagementStrategyNames.VECTORIZE:
            ctx_msgs = ContextMemoryManager._handle_strategy_vectorize_history(assistant, chat_history,
                                                                                       chat_object, max_context_msgs)
        """

        logger.info(f"[ChatContextManager.handle_context] Handled the context.")
        return ctx_msgs

    @staticmethod
    def _handle_strategy_vectorize_history(assistant, chat_history, chat_object, max_messages):
        try:
            ctx_msgs = ContextMemoryManager.store_context_memory_as_embedding(
                context_agent=assistant, message_history=chat_history,
                communication_object=chat_object, maximum_allowed_messages=max_messages
            )
            logger.info(f"[ChatContextManager._handle_strategy_vectorize_history] Vectorized the history.")
        except Exception as e:
            logger.error(f"[ChatContextManager._handle_strategy_vectorize_history] Error vectorizing the history: {e}")
            ctx_msgs = chat_history
        return ctx_msgs

    @staticmethod
    def _handle_strategy_stop_conversation(chat_history, max_messages):
        try:
            ctx_msgs = ContextMemoryManager.stop_communication_at_threshold(chat_history, max_messages)
            logger.info(f"[ChatContextManager._handle_strategy_stop_conversation] Stopped the conversation.")
        except Exception as e:
            ctx_msgs = chat_history
            logger.error(f"[ChatContextManager._handle_strategy_stop_conversation] Error stopping the conversation: {e}")
        return ctx_msgs

    @staticmethod
    def _handle_strategy_forget_oldest(chat_history, max_messages):
        try:
            ctx_msgs = ContextMemoryManager.forget_oldest_chat_messages(chat_history, max_messages)
            logger.info(f"[ChatContextManager._handle_strategy_forget_oldest] Forgot the oldest messages.")
        except Exception as e:
            ctx_msgs = chat_history
            logger.error(f"[ChatContextManager._handle_strategy_forget_oldest] Error forgetting the oldest messages: {e}")
        return ctx_msgs
