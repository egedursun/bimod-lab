#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: openai.py
#  Last Modified: 2024-10-05 02:20:19
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:35
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

from openai import OpenAI

import apps.core.generative_ai.utils.constant_utils
from apps.core.data_security.ner.ner_executor import NERExecutor
from apps.core.generative_ai.auxiliary_methods.output_supply_prompts import BALANCE_OVERFLOW_LOG
from apps.core.generative_ai.auxiliary_methods.json_operations.json_operation_prompts import \
    get_maximum_tool_chains_reached_log, get_maximum_tool_attempts_reached_log, embed_tool_call_in_prompt
from apps.core.generative_ai.auxiliary_methods.errors.error_log_prompts import \
    get_technical_error_log, \
    get_json_decode_error_log
from apps.core.generative_ai.utils import find_tool_call_from_json, ChatRoles, \
    DEFAULT_ERROR_MESSAGE, GPT_DEFAULT_ENCODING_ENGINE, BIMOD_STREAMING_END_TAG, BIMOD_PROCESS_END, RetryCallersNames, \
    step_back_retry_mechanism
from apps.core.system_prompts.chat_history_factory_builder import HistoryBuilder
from apps.core.system_prompts.system_prompt_factory_builder import SystemPromptFactoryBuilder
from apps.core.tool_calls.tool_call_manager import ToolCallManager
from apps.multimodal_chat.utils import calculate_billable_cost_from_raw, transmit_websocket_log, BIMOD_NO_TAG_PLACEHOLDER


logger = logging.getLogger(__name__)


class OpenAIGPTClientManager:
    def __init__(self, assistant, chat_object):
        self.connection = OpenAI(api_key=assistant.llm_model.api_key)
        self.assistant = assistant
        self.chat = chat_object

    @staticmethod
    def get_naked_client(llm_model):
        return OpenAI(api_key=llm_model.api_key)

    def respond_stream(self, latest_message, prev_tool_name=None, with_media=False, file_uris=None, image_uris=None):
        from apps.multimodal_chat.models import MultimodalChatMessage
        from apps.llm_transaction.models import LLMTransaction

        transmit_websocket_log(f"""🤖 Assistant started processing the query...""", chat_id=self.chat.id)
        c = self.connection
        user = self.chat.user
        transmit_websocket_log(
            f"""🛜 Connection information and metadata extraction completed.""", chat_id=self.chat.id)

        ner_xc, encrypt_uuid = None, None
        try:
            transmit_websocket_log(f"""🗃️ System prompt is being prepared...""", chat_id=self.chat.id)
            try:
                system_prompt_msgs = [SystemPromptFactoryBuilder.build_system_prompts(
                    chat=self.chat, assistant=self.assistant, user=user, role=ChatRoles.SYSTEM
                )]
                transmit_websocket_log(f"""⚡ System prompt preparation is completed.""", chat_id=self.chat.id)
                transmit_websocket_log(f"""📜 Chat history is being prepared...""", chat_id=self.chat.id)
                if self.assistant.ner_integration is not None:
                    ner_xc = NERExecutor(ner_id=self.assistant.ner_integration.id)
                ext_msgs, encrypt_uuid = HistoryBuilder.build_chat_history(chat=self.chat, ner_executor=ner_xc)
                system_prompt_msgs.extend(ext_msgs)
                transmit_websocket_log(f"""💥 Chat history preparation is completed.""", chat_id=self.chat.id)

            except Exception as e:
                logger.error(f"Error occurred while preparing the prompts for the process: {str(e)}")
                transmit_websocket_log(f"""
                🚨 A critical error occurred while preparing the prompts for the process.
                """, chat_id=self.chat.id, stop_tag=BIMOD_PROCESS_END)
                return DEFAULT_ERROR_MESSAGE

            try:
                transmit_websocket_log(f"""📈 Transaction parameters are being inspected...""",
                                       chat_id=self.chat.id)
                latest_msg_billable_cost = calculate_billable_cost_from_raw(
                    encoding_engine=GPT_DEFAULT_ENCODING_ENGINE, model=self.chat.assistant.llm_model.model_name,
                    text=latest_message)
            except Exception as e:
                logger.error(f"Error occurred while inspecting the transaction parameters: {str(e)}")
                transmit_websocket_log(f"""
                🚨 A critical error occurred while inspecting the transaction parameters.
                """, stop_tag=BIMOD_PROCESS_END, chat_id=self.chat.id)
                return DEFAULT_ERROR_MESSAGE

            if latest_msg_billable_cost > self.chat.organization.balance:
                transmit_websocket_log(f"""
            🚨 Organization has insufficient balance to proceed with the transaction. Cancelling the process.
                """, stop_tag=BIMOD_PROCESS_END, chat_id=self.chat.id)
                response = BALANCE_OVERFLOW_LOG
                failure_tx = LLMTransaction.objects.create(
                    organization=self.chat.organization, model=self.chat.assistant.llm_model,
                    responsible_user=self.chat.user, responsible_assistant=self.chat.assistant,
                    encoding_engine=GPT_DEFAULT_ENCODING_ENGINE, transaction_context_content=response,
                    llm_cost=0, internal_service_cost=0, tax_cost=0, total_cost=0, total_billable_cost=0,
                    transaction_type=ChatRoles.ASSISTANT, transaction_source=self.chat.chat_source)
                self.chat.transactions.add(failure_tx)
                self.chat.save()
                final_resp = response
                return final_resp

            transmit_websocket_log(f"""♟️ Transaction parameters inspection is completed.""", chat_id=self.chat.id)
            transmit_websocket_log(f"""📡 Generating response in cooperation with the language model...""", chat_id=self.chat.id)
            try:
                ws_atoms = c.chat.completions.create(
                    model=self.assistant.llm_model.model_name, messages=system_prompt_msgs,
                    temperature=float(self.assistant.llm_model.temperature),
                    frequency_penalty=float(self.assistant.llm_model.frequency_penalty),
                    presence_penalty=float(self.assistant.llm_model.presence_penalty),
                    max_tokens=int(self.assistant.llm_model.maximum_tokens),
                    top_p=float(self.assistant.llm_model.top_p), stream=True)
            except Exception as e:
                logger.error(f"Error occurred while retrieving the response from the language model: {str(e)}")
                transmit_websocket_log(f"""
                🚨 A critical error occurred while retrieving the response from the language model.
                """, stop_tag=BIMOD_PROCESS_END, chat_id=self.chat.id)
                return DEFAULT_ERROR_MESSAGE

            transmit_websocket_log(f"""
            🧨 Response streamer is ready to process the response.
            """, chat_id=self.chat.id)
            try:
                transmit_websocket_log(f"""⚓ Response generation is in progress...""", chat_id=self.chat.id)
                acc_resp = ""
                for element in ws_atoms:
                    choices = element.choices
                    first_choice = choices[0]
                    delta = first_choice.delta
                    content = delta.content
                    if content is not None:
                        acc_resp += content
                        transmit_websocket_log(f"""{content}""", stop_tag=BIMOD_NO_TAG_PLACEHOLDER,
                                               chat_id=self.chat.id)

                transmit_websocket_log(f"""""", stop_tag=BIMOD_STREAMING_END_TAG, chat_id=self.chat.id)
                transmit_websocket_log(f"""
                🔌 Generation iterations has been successfully accomplished.
                """, chat_id=self.chat.id)

                ####################################################################################################
                # NER INTEGRATION - DECRYPTION
                ####################################################################################################
                if ner_xc:
                    decrypt_txt = ner_xc.decrypt_text(anonymized_text=acc_resp, uuid=encrypt_uuid)
                    if decrypt_txt:
                        acc_resp = decrypt_txt
                ####################################################################################################
                ####################################################################################################

                transmit_websocket_log(f"""📦 Preparing the response...""", chat_id=self.chat.id)
            except Exception as e:
                logger.error(f"Error occurred while processing the response from the language model: {str(e)}")
                transmit_websocket_log(f"""
                🚨 A critical error occurred while processing the response from the language model.
                """, stop_tag=BIMOD_PROCESS_END, chat_id=self.chat.id)
                return DEFAULT_ERROR_MESSAGE

            transmit_websocket_log(f"""
            🕹️ Raw response stream has been successfully delivered.
            """, chat_id=self.chat.id)
            transmit_websocket_log(f"""🚀 Processing the transactional information...""", chat_id=self.chat.id)
            try:
                LLMTransaction.objects.create(
                    organization=self.chat.organization, model=self.chat.assistant.llm_model,
                    responsible_user=self.chat.user, responsible_assistant=self.chat.assistant,
                    encoding_engine=GPT_DEFAULT_ENCODING_ENGINE, transaction_context_content=acc_resp,
                    llm_cost=0, internal_service_cost=0, tax_cost=0, total_cost=0, total_billable_cost=0,
                    transaction_type=ChatRoles.ASSISTANT, transaction_source=self.chat.chat_source)
            except Exception as e:
                logger.error(f"Error occurred while saving the transaction: {str(e)}")
                transmit_websocket_log(f"""
            🚨 A critical error occurred while saving the transaction. Cancelling the process.
                                """, stop_tag=BIMOD_PROCESS_END, chat_id=self.chat.id)
                return DEFAULT_ERROR_MESSAGE

            transmit_websocket_log(f"""
            🧲 Transactional information has been successfully processed.
            """, chat_id=self.chat.id)
            final_resp = acc_resp
        except Exception as e:
            logger.error(f"Error occurred while processing the response: {str(e)}")
            final_resp = step_back_retry_mechanism(
                client=self, latest_message=latest_message, caller=RetryCallersNames.RESPOND_STREAM)
            transmit_websocket_log(f"""
            🚨 Error occurred while processing the response. The assistant will attempt to retry...
                """, chat_id=self.chat.id)
            if final_resp == DEFAULT_ERROR_MESSAGE:
                final_resp += get_technical_error_log(error_logs=str(e))
                apps.core.generative_ai.utils.constant_utils.ACTIVE_RETRY_COUNT = 0

        tool_resp_list, json_content_of_resp = [], []
        if find_tool_call_from_json(final_resp):
            transmit_websocket_log(f"""
            🛠️ Tool usage call detected in the response. Processing with the tool execution steps...
                                """, chat_id=self.chat.id)
            if apps.core.generative_ai.utils.constant_utils.ACTIVE_CHAIN_SIZE > self.assistant.tool_max_chains:
                idle_tx_msg = get_maximum_tool_chains_reached_log(final_response=final_resp)
                transmit_websocket_log(f"""
            🚨 Maximum tool chain limit has been reached. Cancelling the process.
                                """, stop_tag=BIMOD_PROCESS_END, chat_id=self.chat.id)
                try:
                    failure_tx = LLMTransaction.objects.create(
                        organization=self.chat.organization, model=self.chat.assistant.llm_model,
                        responsible_user=self.chat.user, responsible_assistant=self.chat.assistant,
                        encoding_engine=GPT_DEFAULT_ENCODING_ENGINE, transaction_context_content=idle_tx_msg,
                        llm_cost=0, internal_service_cost=0, tax_cost=0, total_cost=0, total_billable_cost=0,
                        transaction_type=ChatRoles.ASSISTANT, transaction_source=self.chat.chat_source)
                    self.chat.transactions.add(failure_tx)
                    self.chat.save()
                except Exception as e:
                    logger.error(f"Error occurred while saving the transaction: {str(e)}")
                    transmit_websocket_log(f"""
            🚨 A critical error occurred while saving the transaction. Cancelling the process.
                                """, stop_tag=BIMOD_PROCESS_END, chat_id=self.chat.id)
                    return idle_tx_msg
                apps.core.generative_ai.utils.constant_utils.ACTIVE_CHAIN_SIZE = 0
                return idle_tx_msg
            if apps.core.generative_ai.utils.constant_utils.ACTIVE_TOOL_RETRY_COUNT > self.assistant.tool_max_attempts_per_instance:
                idle_tx_msg = get_maximum_tool_attempts_reached_log(final_response=final_resp)
                transmit_websocket_log(f"""
            🚨 Maximum same tool attempt limit has been reached. Cancelling the process.
                                """, stop_tag=BIMOD_PROCESS_END, chat_id=self.chat.id)
                try:
                    failure_tx = LLMTransaction.objects.create(
                        organization=self.chat.organization, model=self.chat.assistant.llm_model,
                        responsible_user=self.chat.user, responsible_assistant=self.chat.assistant,
                        encoding_engine=GPT_DEFAULT_ENCODING_ENGINE, transaction_context_content=idle_tx_msg,
                        llm_cost=0, internal_service_cost=0, tax_cost=0, total_cost=0, total_billable_cost=0,
                        transaction_type=ChatRoles.ASSISTANT, transaction_source=self.chat.chat_source)
                    self.chat.transactions.add(failure_tx)
                    self.chat.save()
                except Exception as e:
                    logger.error(f"Error occurred while saving the transaction: {str(e)}")
                    transmit_websocket_log(f"""
            🚨 A critical error occurred while saving the transaction. Cancelling the process.
                                """, stop_tag=BIMOD_PROCESS_END, chat_id=self.chat.id)
                    return idle_tx_msg
                apps.core.generative_ai.utils.constant_utils.ACTIVE_TOOL_RETRY_COUNT = 0
                return idle_tx_msg

            apps.core.generative_ai.utils.constant_utils.ACTIVE_TOOL_RETRY_COUNT += 1
            transmit_websocket_log(f"""🧰 Identifying the valid tool usage calls...""", chat_id=self.chat.id)

            json_content_of_resp = find_tool_call_from_json(final_resp)

            transmit_websocket_log(f"""💡️ Tool usage calls have been identified.""", chat_id=self.chat.id)
            transmit_websocket_log(f"""
            🧭 Number of tool usage calls that is delivered: {len(json_content_of_resp)}
                """, chat_id=self.chat.id)

            tool_name = None
            for i, json_part in enumerate(json_content_of_resp):
                transmit_websocket_log(f"""
                🧮 Executing the tool usage call index: {i + 1} out of {len(json_content_of_resp)} ...
                """, chat_id=self.chat.id)
                try:
                    tool_xc = ToolCallManager(assistant=self.assistant, chat=self.chat,
                                                    tool_usage_json_str=json_part)
                    tool_resp, tool_name, file_uris, image_uris = tool_xc.call_internal_tool_service()
                    transmit_websocket_log(f"""
                    🧰 Tool usage call for: '{tool_name}' has been successfully executed. Proceeding with the next actions...
                                        """, chat_id=self.chat.id)
                    if tool_name is not None and tool_name != prev_tool_name:
                        apps.core.generative_ai.utils.constant_utils.ACTIVE_CHAIN_SIZE += 1
                        prev_tool_name = tool_name
                    transmit_websocket_log(f"""
                    📦 Tool response from '{tool_name}' is being delivered to the assistant for further actions...
                                        """, chat_id=self.chat.id)
                    tool_resp_list.append(f"""
                                    [{i}] "tool_name": {tool_name},
                                        [{i}a.] "tool_response": {tool_resp},
                                        [{i}b.] "file_uris": {file_uris},
                                        [{i}c.] "image_uris": {image_uris}
                                """)
                    transmit_websocket_log(f"""
                    🎯 Tool response from '{tool_name}' has been successfully delivered to the assistant.
                                        """, chat_id=self.chat.id)
                except Exception as e:
                    logger.error(f"Error occurred while executing the tool: {str(e)}")
                    transmit_websocket_log(f"""
                    🚨 Error occurred while executing the tool. Attempting to recover...
                                        """, chat_id=self.chat.id)
                    if tool_name is not None:
                        tool_resp = get_json_decode_error_log(error_logs=str(e))
                        tool_resp_list.append(f"""
                                    [{i}] [FAILED] "tool_name": {tool_name},
                                        [{i}a.] "tool_response": {tool_resp},
                                        [{i}b.] "file_uris": [],
                                        [{i}c.] "image_uris": []
                                        [{i}d.] "error_logs": {str(e)}
                                """)
                    else:
                        tool_resp = get_json_decode_error_log(error_logs=str(e))
                        tool_resp_list.append(f"""
                                    [{i}] [FAILED / NO TOOL NAME] "tool_name": {tool_name},
                                        [{i}a.] "tool_response": {tool_resp},
                                        [{i}b.] "file_uris": [],
                                        [{i}c.] "image_uris": []
                                        [{i}d.] "error_logs": {str(e)}
                                """)
                    transmit_websocket_log(f"""
                    🚨 Error logs have been delivered to the assistant. Proceeding with the next actions...
                                        """, chat_id=self.chat.id)
        transmit_websocket_log(f"""
            🧠 The assistant is inspecting the responses of the tools...
                                """, chat_id=self.chat.id)
        if tool_resp_list:
            transmit_websocket_log(f"""
            📦 Communication records for the tool requests are being prepared...
                                """, chat_id=self.chat.id)
            try:
                tool_request = MultimodalChatMessage.objects.create(
                    multimodal_chat=self.chat, sender_type=ChatRoles.ASSISTANT.upper(),
                    message_text_content=embed_tool_call_in_prompt(json_parts_of_response=json_content_of_resp),
                    message_file_contents=[], message_image_contents=[])
                self.chat.chat_messages.add(tool_request)
                self.chat.save()
                transmit_websocket_log(f"""
                    ⚙️ Tool request records have been prepared. Proceeding with the next actions...
                """, chat_id=self.chat.id)

            except Exception as e:
                logger.error(f"Error occurred while recording the tool request: {str(e)}")
                transmit_websocket_log(f"""
            🚨 A critical error occurred while recording the tool request. Cancelling the process.
                                """, stop_tag=BIMOD_PROCESS_END, chat_id=self.chat.id)
                return DEFAULT_ERROR_MESSAGE
            try:
                transmit_websocket_log(f"""
            📦 Communication records for the tool responses are being prepared...
                                """, chat_id=self.chat.id)
                tool_message = MultimodalChatMessage.objects.create(
                    multimodal_chat=self.chat, sender_type=HistoryBuilder.ChatRoles.TOOL.upper(),
                    message_text_content=str(tool_resp_list), message_file_contents=file_uris,
                    message_image_contents=image_uris)
                self.chat.chat_messages.add(tool_message)
                self.chat.save()
                transmit_websocket_log(f"""
                    ⚙️ Tool response records have been prepared. Proceeding with the next actions...
                """, chat_id=self.chat.id)
            except Exception as e:
                logger.error(f"Error occurred while recording the tool response: {str(e)}")
                transmit_websocket_log(f"""
            🚨 A critical error occurred while recording the tool response. Cancelling the process.
                                """, stop_tag=BIMOD_PROCESS_END, chat_id=self.chat.id)
                return DEFAULT_ERROR_MESSAGE
            transmit_websocket_log(f"""
            ✨ Communication records for the tool requests and responses have been successfully prepared.
                """, chat_id=self.chat.id)

            transmit_websocket_log(f"""
            📦 Transactions are being prepared for the current level of operations...
                                """, chat_id=self.chat.id)
            try:
                LLMTransaction.objects.create(
                    organization=self.chat.organization, model=self.chat.assistant.llm_model,
                    responsible_user=self.chat.user, responsible_assistant=self.chat.assistant,
                    encoding_engine=GPT_DEFAULT_ENCODING_ENGINE, transaction_context_content=str(tool_resp_list),
                    llm_cost=0, internal_service_cost=0, tax_cost=0, total_cost=0, total_billable_cost=0,
                    transaction_type=ChatRoles.ASSISTANT, transaction_source=self.chat.chat_source)
            except Exception as e:
                logger.error(f"Error occurred while recording the transaction: {str(e)}")
                transmit_websocket_log(f"""
            🚨 A critical error occurred while recording the transaction. Cancelling the process.
                                """, stop_tag=BIMOD_PROCESS_END, chat_id=self.chat.id)

                return DEFAULT_ERROR_MESSAGE
            transmit_websocket_log(f"""
            ❇️ Transactions have been successfully prepared for the current level of operations.
                """, chat_id=self.chat.id)

            transmit_websocket_log(f"""
            🚀 The assistant is getting prepared for the next level of operations...
                                """, chat_id=self.chat.id)
            return self.respond_stream(latest_message=tool_message, prev_tool_name=prev_tool_name,
                                       with_media=with_media, file_uris=file_uris, image_uris=image_uris)

        apps.core.generative_ai.utils.constant_utils.ACTIVE_CHAIN_SIZE = 0
        if with_media:
            return final_resp, file_uris, image_uris
        transmit_websocket_log(f"""
            ✅ The assistant has successfully processed the query. The response is being delivered to the user...
        """, stop_tag=BIMOD_PROCESS_END, chat_id=self.chat.id)
        return final_resp

    def respond(self, latest_message, prev_tool_name=None, with_media=False, file_uris=None, image_uris=None):
        from apps.multimodal_chat.models import MultimodalChatMessage
        from apps.llm_transaction.models import LLMTransaction
        c = self.connection
        user = self.chat.user
        ner_xc, encrypt_msgs = None, None
        try:
            try:
                prompt_msgs = [SystemPromptFactoryBuilder.build_system_prompts(
                    chat=self.chat, assistant=self.assistant, user=user, role=ChatRoles.SYSTEM)]
                if self.assistant.ner_integration is not None:
                    ner_xc = NERExecutor(ner_id=self.assistant.ner_integration.id)
                ext_msgs, encrypt_msgs = HistoryBuilder.build_chat_history(chat=self.chat, ner_executor=ner_xc)
                prompt_msgs.extend(ext_msgs)
            except Exception as e:
                logger.error(f"Error occurred while preparing the prompts for the process: {str(e)}")
                return DEFAULT_ERROR_MESSAGE

            try:
                latest_msg_billable_cost = calculate_billable_cost_from_raw(
                    encoding_engine=GPT_DEFAULT_ENCODING_ENGINE, model=self.chat.assistant.llm_model.model_name,
                    text=latest_message)
            except Exception as e:
                logger.error(f"Error occurred while inspecting the transaction parameters: {str(e)}")
                return DEFAULT_ERROR_MESSAGE

            if latest_msg_billable_cost > self.chat.organization.balance:
                resp = BALANCE_OVERFLOW_LOG
                failure_tx = LLMTransaction.objects.create(
                    organization=self.chat.organization, model=self.chat.assistant.llm_model,
                    responsible_user=self.chat.user, responsible_assistant=self.chat.assistant,
                    encoding_engine=GPT_DEFAULT_ENCODING_ENGINE, transaction_context_content=resp,
                    llm_cost=0, internal_service_cost=0, tax_cost=0, total_cost=0, total_billable_cost=0,
                    transaction_type=ChatRoles.ASSISTANT, transaction_source=self.chat.chat_source
                )
                self.chat.transactions.add(failure_tx)
                self.chat.save()
                final_resp = resp
                return final_resp

            try:
                resp = c.chat.completions.create(
                    model=self.assistant.llm_model.model_name, messages=prompt_msgs,
                    temperature=float(self.assistant.llm_model.temperature),
                    frequency_penalty=float(self.assistant.llm_model.frequency_penalty),
                    presence_penalty=float(self.assistant.llm_model.presence_penalty),
                    max_tokens=int(self.assistant.llm_model.maximum_tokens),
                    top_p=float(self.assistant.llm_model.top_p))
            except Exception as e:
                logger.error(f"Error occurred while retrieving the response from the language model: {str(e)}")
                return DEFAULT_ERROR_MESSAGE
            try:
                choices = resp.choices
                first_choice = choices[0]
                choice_message = first_choice.message
                choice_message_content = choice_message.content
            except Exception as e:
                logger.error(f"Error occurred while processing the response from the language model: {str(e)}")
                return DEFAULT_ERROR_MESSAGE

            ####################################################################################################
            # NER INTEGRATION - DECRYPTION
            ####################################################################################################
            if ner_xc:
                decrypt_txt = ner_xc.decrypt_text(anonymized_text=choice_message_content, uuid=encrypt_msgs)
                if decrypt_txt:
                    choice_message_content = decrypt_txt
            ####################################################################################################
            ####################################################################################################

            try:
                LLMTransaction.objects.create(
                    organization=self.chat.organization, model=self.chat.assistant.llm_model,
                    responsible_user=self.chat.user, responsible_assistant=self.chat.assistant,
                    encoding_engine=GPT_DEFAULT_ENCODING_ENGINE, transaction_context_content=choice_message_content,
                    llm_cost=0, internal_service_cost=0, tax_cost=0, total_cost=0,  total_billable_cost=0,
                    transaction_type=ChatRoles.ASSISTANT, transaction_source=self.chat.chat_source
                )
            except Exception as e:
                logger.error(f"Error occurred while saving the transaction: {str(e)}")
                return DEFAULT_ERROR_MESSAGE
            final_resp = choice_message_content
        except Exception as e:
            logger.error(f"Error occurred while processing the response: {str(e)}")
            final_resp = step_back_retry_mechanism(client=self, latest_message=latest_message,
                                                       caller=RetryCallersNames.RESPOND)
            if final_resp == DEFAULT_ERROR_MESSAGE:
                final_resp += get_technical_error_log(error_logs=str(e))
                apps.core.generative_ai.utils.constant_utils.ACTIVE_RETRY_COUNT = 0

        tool_resp_list, json_content_of_resp = [], []
        if find_tool_call_from_json(final_resp):
            if apps.core.generative_ai.utils.constant_utils.ACTIVE_CHAIN_SIZE > self.assistant.tool_max_chains:
                idle_tx_msg = get_maximum_tool_chains_reached_log(final_response=final_resp)
                try:
                    failure_tx = LLMTransaction.objects.create(
                        organization=self.chat.organization, model=self.chat.assistant.llm_model,
                        responsible_user=self.chat.user, responsible_assistant=self.chat.assistant,
                        encoding_engine=GPT_DEFAULT_ENCODING_ENGINE, transaction_context_content=idle_tx_msg,
                        llm_cost=0, internal_service_cost=0, tax_cost=0, total_cost=0, total_billable_cost=0,
                        transaction_type=ChatRoles.ASSISTANT, transaction_source=self.chat.chat_source
                    )
                    self.chat.transactions.add(failure_tx)
                    self.chat.save()
                except Exception as e:
                    logger.error(f"Error occurred while saving the transaction: {str(e)}")
                    return idle_tx_msg
                apps.core.generative_ai.utils.constant_utils.ACTIVE_CHAIN_SIZE = 0
                return idle_tx_msg

            if apps.core.generative_ai.utils.constant_utils.ACTIVE_TOOL_RETRY_COUNT > self.assistant.tool_max_attempts_per_instance:
                idle_tx_msg = get_maximum_tool_attempts_reached_log(final_response=final_resp)
                try:
                    failure_tx = LLMTransaction.objects.create(
                        organization=self.chat.organization, model=self.chat.assistant.llm_model,
                        responsible_user=self.chat.user, responsible_assistant=self.chat.assistant,
                        encoding_engine=GPT_DEFAULT_ENCODING_ENGINE, transaction_context_content=idle_tx_msg,
                        llm_cost=0, internal_service_cost=0, tax_cost=0, total_cost=0, total_billable_cost=0,
                        transaction_type=ChatRoles.ASSISTANT, transaction_source=self.chat.chat_source
                    )
                    self.chat.transactions.add(failure_tx)
                    self.chat.save()
                except Exception as e:
                    logger.error(f"Error occurred while saving the transaction: {str(e)}")
                    return idle_tx_msg
                apps.core.generative_ai.utils.constant_utils.ACTIVE_TOOL_RETRY_COUNT = 0
                return idle_tx_msg

            apps.core.generative_ai.utils.constant_utils.ACTIVE_TOOL_RETRY_COUNT += 1
            json_content_of_resp = find_tool_call_from_json(final_resp)
            tool_name = None
            for i, json_part in enumerate(json_content_of_resp):
                try:
                    tool_executor = ToolCallManager(
                        assistant=self.assistant, chat=self.chat, tool_usage_json_str=json_part
                    )
                    tool_resp, tool_name, file_uris, image_uris = tool_executor.call_internal_tool_service()
                    if tool_name is not None and tool_name != prev_tool_name:
                        apps.core.generative_ai.utils.constant_utils.ACTIVE_CHAIN_SIZE += 1
                        prev_tool_name = tool_name
                    tool_resp_list.append(f"""
                            [{i}] "tool_name": {tool_name},
                                [{i}a.] "tool_response": {tool_resp},
                                [{i}b.] "file_uris": {file_uris},
                                [{i}c.] "image_uris": {image_uris}
                        """)
                except Exception as e:
                    logger.error(f"Error occurred while executing the tool: {str(e)}")
                    if tool_name is not None:
                        tool_resp = get_json_decode_error_log(error_logs=str(e))
                        tool_resp_list.append(f"""
                            [{i}] [FAILED] "tool_name": {tool_name},
                                [{i}a.] "tool_response": {tool_resp},
                                [{i}b.] "file_uris": [],
                                [{i}c.] "image_uris": []
                                [{i}d.] "error_logs": {str(e)}
                        """)
                    else:
                        tool_resp = get_json_decode_error_log(error_logs=str(e))
                        tool_resp_list.append(f"""
                            [{i}] [FAILED / NO TOOL NAME] "tool_name": {tool_name},
                                [{i}a.] "tool_response": {tool_resp},
                                [{i}b.] "file_uris": [],
                                [{i}c.] "image_uris": []
                                [{i}d.] "error_logs": {str(e)}
                        """)

        if tool_resp_list:
            try:
                tool_req = MultimodalChatMessage.objects.create(
                    multimodal_chat=self.chat, sender_type=ChatRoles.ASSISTANT.upper(),
                    message_text_content=embed_tool_call_in_prompt(json_parts_of_response=json_content_of_resp),
                    message_file_contents=[], message_image_contents=[])
                self.chat.chat_messages.add(tool_req)
                self.chat.save()
            except Exception as e:
                logger.error(f"Error occurred while recording the tool request: {str(e)}")
                return DEFAULT_ERROR_MESSAGE

            try:
                tool_msg = MultimodalChatMessage.objects.create(
                    multimodal_chat=self.chat, sender_type=HistoryBuilder.ChatRoles.TOOL.upper(),
                    message_text_content=str(tool_resp_list), message_file_contents=file_uris,
                    message_image_contents=image_uris)
                self.chat.chat_messages.add(tool_msg)
                self.chat.save()
            except Exception as e:
                logger.error(f"Error occurred while recording the tool response: {str(e)}")
                return DEFAULT_ERROR_MESSAGE

            try:
                LLMTransaction.objects.create(
                    organization=self.chat.organization, model=self.chat.assistant.llm_model,
                    responsible_user=self.chat.user, responsible_assistant=self.chat.assistant,
                    encoding_engine=GPT_DEFAULT_ENCODING_ENGINE, transaction_context_content=str(tool_resp_list),
                    llm_cost=0, internal_service_cost=0, tax_cost=0, total_cost=0, total_billable_cost=0,
                    transaction_type=ChatRoles.ASSISTANT, transaction_source=self.chat.chat_source)
            except Exception as e:
                logger.error(f"Error occurred while recording the transaction: {str(e)}")
                return DEFAULT_ERROR_MESSAGE
            return self.respond(latest_message=tool_msg, prev_tool_name=prev_tool_name, with_media=with_media,
                                file_uris=file_uris, image_uris=image_uris)

        apps.core.generative_ai.utils.constant_utils.ACTIVE_CHAIN_SIZE = 0
        if with_media:
            return final_resp, file_uris, image_uris
        return final_resp
