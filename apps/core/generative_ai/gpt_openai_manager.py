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
import json
import logging

from openai import OpenAI

import apps.core.generative_ai.utils.constant_utils

from apps.core.data_security.ner.ner_executor import (
    NERExecutor
)

from apps.core.generative_ai.auxiliary_methods.output_supply_prompts import (
    BALANCE_OVERFLOW_LOG
)

from apps.core.generative_ai.auxiliary_methods.json_operations.json_operation_prompts import (
    get_maximum_tool_chains_reached_log,
    get_maximum_tool_attempts_reached_log,
    embed_tool_call_in_prompt
)

from apps.core.generative_ai.auxiliary_methods.errors.error_log_prompts import (
    get_technical_error_log,
    get_json_decode_error_log
)

from apps.core.generative_ai.utils import (
    find_tool_call_from_json,
    ChatRoles,
    DEFAULT_ERROR_MESSAGE,
    GPT_DEFAULT_ENCODING_ENGINE,
    BIMOD_STREAMING_END_TAG,
    BIMOD_PROCESS_END,
    RetryCallersNames,
    step_back_retry_mechanism
)

from apps.core.sinaptera.sinaptera_executor import (
    SinapteraBoosterManager
)

from apps.core.sinaptera.utils import (
    SinapteraCallerTypes
)

from apps.core.system_prompts.chat_history_factory_builder import (
    HistoryBuilder
)

from apps.core.system_prompts.system_prompt_factory_builder import (
    SystemPromptFactoryBuilder
)

from apps.core.tool_calls.tool_call_manager import (
    ToolCallManager
)

from apps.multimodal_chat.utils import (
    calculate_billable_cost_from_raw,
    transmit_websocket_log,
    BIMOD_NO_TAG_PLACEHOLDER,
    TransmitWebsocketLogSenderType,
)

logger = logging.getLogger(__name__)


class OpenAIGPTClientManager:
    def __init__(
        self,
        assistant,
        chat_object
    ):
        self.connection = OpenAI(
            api_key=assistant.llm_model.api_key
        )

        self.assistant = assistant
        self.chat = chat_object

    @staticmethod
    def get_naked_client(llm_model):
        return OpenAI(
            api_key=llm_model.api_key
        )

    @staticmethod
    def get_naked_client_with_api_key(api_key):
        return OpenAI(
            api_key=api_key
        )

    def respond_stream(
        self,
        latest_message,
        prev_tool_name=None,
        with_media=False,
        file_uris=None,
        image_uris=None,
        with_custom_system_prompt=False,
        custom_system_prompt=None,
        fermion__is_fermion_supervised=False,
        fermion__export_type=None,
        fermion__endpoint=None,
        result_affirmed=False
    ):

        from apps.multimodal_chat.models import (
            MultimodalChatMessage
        )

        from apps.llm_transaction.models import (
            LLMTransaction
        )

        latest_message: MultimodalChatMessage

        transmit_websocket_log(
            f"""🤖 Assistant started processing the query...""",
            chat_id=self.chat.id,
            sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
            fermion__is_fermion_supervised=fermion__is_fermion_supervised,
            fermion__export_type=fermion__export_type,
            fermion__endpoint=fermion__endpoint
        )

        c = self.connection
        user = self.chat.user

        transmit_websocket_log(
            f"""🛜 Connection information and metadata extraction completed.""",
            chat_id=self.chat.id,
            sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
            fermion__is_fermion_supervised=fermion__is_fermion_supervised,
            fermion__export_type=fermion__export_type,
            fermion__endpoint=fermion__endpoint
        )

        ner_xc, encrypt_uuid = None, None
        try:

            transmit_websocket_log(
                f"""🗃️ System prompt is being prepared...""",
                chat_id=self.chat.id,
                sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                fermion__export_type=fermion__export_type,
                fermion__endpoint=fermion__endpoint
            )

            try:
                if with_custom_system_prompt is False:
                    system_prompt_msgs = [
                        SystemPromptFactoryBuilder.build_system_prompts(
                            chat=self.chat,
                            assistant=self.assistant,
                            user=user,
                            role=ChatRoles.SYSTEM
                        )
                    ]

                else:
                    system_prompt_msgs = [
                        custom_system_prompt
                    ]

                transmit_websocket_log(
                    f"""⚡ System prompt preparation is completed.""",
                    chat_id=self.chat.id,
                    sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                    fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                    fermion__export_type=fermion__export_type,
                    fermion__endpoint=fermion__endpoint
                )

                transmit_websocket_log(
                    f"""📜 Chat history is being prepared...""",
                    chat_id=self.chat.id,
                    sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                    fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                    fermion__export_type=fermion__export_type,
                    fermion__endpoint=fermion__endpoint
                )

                if self.assistant.ner_integration is not None:
                    ner_xc = NERExecutor(
                        ner_id=self.assistant.ner_integration.id
                    )

                ext_msgs, encrypt_uuid = HistoryBuilder.build_chat_history(
                    chat=self.chat,
                    ner_executor=ner_xc
                )

                system_prompt_msgs.extend(ext_msgs)

                transmit_websocket_log(
                    f"""💥 Chat history preparation is completed.""",
                    chat_id=self.chat.id,
                    sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                    fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                    fermion__export_type=fermion__export_type,
                    fermion__endpoint=fermion__endpoint
                )

            except Exception as e:

                logger.error(f"Error occurred while preparing the prompts for the process: {str(e)}")

                transmit_websocket_log(
                    f"""🚨 A critical error occurred while preparing the prompts for the process.""",
                    chat_id=self.chat.id,
                    stop_tag=BIMOD_PROCESS_END,
                    sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                    fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                    fermion__export_type=fermion__export_type,
                    fermion__endpoint=fermion__endpoint
                )

                return DEFAULT_ERROR_MESSAGE

            try:
                transmit_websocket_log(
                    f"""📈 Transaction parameters are being inspected...""",
                    chat_id=self.chat.id,
                    sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                    fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                    fermion__export_type=fermion__export_type,
                    fermion__endpoint=fermion__endpoint
                )

                latest_msg_billable_cost = calculate_billable_cost_from_raw(
                    encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                    model=self.chat.assistant.llm_model.model_name,
                    text=latest_message.message_text_content
                )

            except Exception as e:

                logger.error(f"Error occurred while inspecting the transaction parameters: {str(e)}")

                transmit_websocket_log(
                    f"""🚨 A critical error occurred while inspecting the transaction parameters.""",
                    stop_tag=BIMOD_PROCESS_END,
                    chat_id=self.chat.id,
                    sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                    fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                    fermion__export_type=fermion__export_type,
                    fermion__endpoint=fermion__endpoint
                )

                return DEFAULT_ERROR_MESSAGE

            if latest_msg_billable_cost > self.chat.organization.balance:
                transmit_websocket_log(
                    f"""🚨 Organization has insufficient balance to proceed with the transaction. Cancelling the process.""",
                    stop_tag=BIMOD_PROCESS_END,
                    chat_id=self.chat.id,
                    sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                    fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                    fermion__export_type=fermion__export_type,
                    fermion__endpoint=fermion__endpoint
                )

                response = BALANCE_OVERFLOW_LOG

                failure_tx = LLMTransaction.objects.create(
                    organization=self.chat.organization,
                    model=self.chat.assistant.llm_model,
                    responsible_user=self.chat.user,
                    responsible_assistant=self.chat.assistant,
                    encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                    transaction_context_content=response,
                    llm_cost=0,
                    internal_service_cost=0,
                    tax_cost=0,
                    total_cost=0,
                    total_billable_cost=0,
                    transaction_type=ChatRoles.ASSISTANT,
                    transaction_source=self.chat.chat_source
                )

                self.chat.transactions.add(failure_tx)
                self.chat.save()

                final_resp = response

                return final_resp

            transmit_websocket_log(
                f"""♟️ Transaction parameters inspection is completed.""",
                chat_id=self.chat.id,
                sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                fermion__export_type=fermion__export_type,
                fermion__endpoint=fermion__endpoint
            )

            transmit_websocket_log(
                f"""📡 Generating response in cooperation with the language model...""",
                chat_id=self.chat.id,
                sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                fermion__export_type=fermion__export_type,
                fermion__endpoint=fermion__endpoint
            )

            try:

                tree_booster: SinapteraBoosterManager = SinapteraBoosterManager(
                    user=user,
                    llm_core=self.chat.assistant.llm_model,
                    caller_type=SinapteraCallerTypes.ASSISTANT,
                )

                if (
                    tree_booster.sinaptera_configuration.is_active_on_assistants is True and
                    result_affirmed is False
                ):

                    resp = tree_booster.execute(
                        structured_conversation_history=system_prompt_msgs,
                        chat_id=self.chat.id,
                    )

                else:

                    resp = c.chat.completions.create(
                        model=self.assistant.llm_model.model_name,
                        messages=system_prompt_msgs,
                        # temperature=float(self.assistant.llm_model.temperature),
                        # frequency_penalty=float(self.assistant.llm_model.frequency_penalty),
                        # presence_penalty=float(self.assistant.llm_model.presence_penalty),
                        # max_tokens=int(self.assistant.llm_model.maximum_tokens),
                        # top_p=float(self.assistant.llm_model.top_p)
                    )

            except Exception as e:
                logger.error(f"Error occurred while retrieving the response from the language model: {str(e)}")

                transmit_websocket_log(
                    f"""🚨 A critical error occurred while retrieving the response from the language model.""",
                    stop_tag=BIMOD_PROCESS_END,
                    chat_id=self.chat.id,
                    sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                    fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                    fermion__export_type=fermion__export_type,
                    fermion__endpoint=fermion__endpoint
                )

                return DEFAULT_ERROR_MESSAGE

            transmit_websocket_log(
                f"""🧨 Response streamer is ready to process the response. """,
                chat_id=self.chat.id,
                sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                fermion__export_type=fermion__export_type,
                fermion__endpoint=fermion__endpoint
            )

            try:

                if (
                    tree_booster is not None and
                    tree_booster.sinaptera_configuration.is_active_on_assistants is True and
                    result_affirmed is False
                ):
                    acc_resp = resp

                else:

                    choices = resp.choices
                    first_choice = choices[0]
                    choice_message = first_choice.message
                    acc_resp = choice_message.content

                transmit_websocket_log(
                    f"""{acc_resp}""",
                    stop_tag=BIMOD_NO_TAG_PLACEHOLDER,
                    chat_id=self.chat.id,
                    sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                    fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                    fermion__export_type=fermion__export_type,
                    fermion__endpoint=fermion__endpoint
                )

                transmit_websocket_log(
                    f"""""",
                    stop_tag=BIMOD_STREAMING_END_TAG,
                    chat_id=self.chat.id,
                    sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                    fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                    fermion__export_type=fermion__export_type,
                    fermion__endpoint=fermion__endpoint
                )

                transmit_websocket_log(
                    f"""🔌 Generation iterations has been successfully accomplished.""",
                    chat_id=self.chat.id,
                    sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                    fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                    fermion__export_type=fermion__export_type,
                    fermion__endpoint=fermion__endpoint
                )

                ####################################################################################################
                # NER INTEGRATION - DECRYPTION
                ####################################################################################################

                if ner_xc:
                    decrypt_txt = ner_xc.decrypt_text(
                        anonymized_text=acc_resp,
                        uuid=encrypt_uuid
                    )

                    if decrypt_txt:
                        acc_resp = decrypt_txt

                ####################################################################################################
                ####################################################################################################

                transmit_websocket_log(
                    f"""📦 Preparing the response...""",
                    chat_id=self.chat.id,
                    sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                    fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                    fermion__export_type=fermion__export_type,
                    fermion__endpoint=fermion__endpoint
                )

            except Exception as e:
                logger.error(f"Error occurred while processing the response from the language model: {str(e)}")

                transmit_websocket_log(
                    f""" 🚨 A critical error occurred while processing the response from the language model.""",
                    stop_tag=BIMOD_PROCESS_END,
                    chat_id=self.chat.id,
                    sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                    fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                    fermion__export_type=fermion__export_type,
                    fermion__endpoint=fermion__endpoint
                )

                return DEFAULT_ERROR_MESSAGE

            transmit_websocket_log(
                f"""🕹️ Raw response stream has been successfully delivered.""",
                chat_id=self.chat.id,
                sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                fermion__export_type=fermion__export_type,
                fermion__endpoint=fermion__endpoint
            )

            transmit_websocket_log(
                f"""🚀 Processing the transactional information...""",
                chat_id=self.chat.id,
                sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                fermion__export_type=fermion__export_type,
                fermion__endpoint=fermion__endpoint
            )

            try:
                LLMTransaction.objects.create(
                    organization=self.chat.organization,
                    model=self.chat.assistant.llm_model,
                    responsible_user=self.chat.user,
                    responsible_assistant=self.chat.assistant,
                    encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                    transaction_context_content=acc_resp,
                    llm_cost=0,
                    internal_service_cost=0,
                    tax_cost=0,
                    total_cost=0,
                    total_billable_cost=0,
                    transaction_type=ChatRoles.ASSISTANT,
                    transaction_source=self.chat.chat_source
                )

            except Exception as e:
                logger.error(f"Error occurred while saving the transaction: {str(e)}")

                transmit_websocket_log(
                    f"""🚨 A critical error occurred while saving the transaction. Cancelling the process.""",
                    stop_tag=BIMOD_PROCESS_END,
                    chat_id=self.chat.id,
                    sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                    fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                    fermion__export_type=fermion__export_type,
                    fermion__endpoint=fermion__endpoint
                )

                return DEFAULT_ERROR_MESSAGE

            transmit_websocket_log(
                f"""🧲 Transactional information has been successfully processed.""",
                chat_id=self.chat.id,
                sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                fermion__export_type=fermion__export_type,
                fermion__endpoint=fermion__endpoint
            )

            final_resp = acc_resp

        except Exception as e:
            logger.error(f"Error occurred while processing the response: {str(e)}")

            final_resp = step_back_retry_mechanism(
                client=self,
                latest_message=latest_message,
                caller=RetryCallersNames.RESPOND_STREAM
            )

            transmit_websocket_log(
                f""" 🚨 Error occurred while processing the response. The assistant will attempt to retry...""",
                chat_id=self.chat.id,
                sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                fermion__export_type=fermion__export_type,
                fermion__endpoint=fermion__endpoint
            )

            if final_resp == DEFAULT_ERROR_MESSAGE:
                final_resp += get_technical_error_log(
                    error_logs=str(e)
                )

                apps.core.generative_ai.utils.constant_utils.ACTIVE_RETRY_COUNT = 0

        tool_resp_list, json_content_of_resp = [], []

        if find_tool_call_from_json(final_resp):

            transmit_websocket_log(
                f"""🛠️ Tool usage call detected in the response. Processing with the tool execution steps...""",
                chat_id=self.chat.id,
                sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                fermion__export_type=fermion__export_type,
                fermion__endpoint=fermion__endpoint
            )

            if apps.core.generative_ai.utils.constant_utils.ACTIVE_CHAIN_SIZE > self.assistant.tool_max_chains:
                idle_tx_msg = get_maximum_tool_chains_reached_log(
                    final_response=final_resp
                )

                transmit_websocket_log(
                    f""" 🚨 Maximum tool chain limit has been reached. Cancelling the process.""",
                    stop_tag=BIMOD_PROCESS_END,
                    chat_id=self.chat.id,
                    sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                    fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                    fermion__export_type=fermion__export_type,
                    fermion__endpoint=fermion__endpoint
                )

                try:
                    failure_tx = LLMTransaction.objects.create(
                        organization=self.chat.organization,
                        model=self.chat.assistant.llm_model,
                        responsible_user=self.chat.user,
                        responsible_assistant=self.chat.assistant,
                        encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                        transaction_context_content=idle_tx_msg,
                        llm_cost=0,
                        internal_service_cost=0,
                        tax_cost=0,
                        total_cost=0,
                        total_billable_cost=0,
                        transaction_type=ChatRoles.ASSISTANT,
                        transaction_source=self.chat.chat_source
                    )

                    self.chat.transactions.add(failure_tx)
                    self.chat.save()

                except Exception as e:
                    logger.error(f"Error occurred while saving the transaction: {str(e)}")

                    transmit_websocket_log(
                        f"""🚨 A critical error occurred while saving the transaction. Cancelling the process. """,
                        stop_tag=BIMOD_PROCESS_END,
                        chat_id=self.chat.id,
                        sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                        fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                        fermion__export_type=fermion__export_type,
                        fermion__endpoint=fermion__endpoint
                    )

                    return idle_tx_msg

                apps.core.generative_ai.utils.constant_utils.ACTIVE_CHAIN_SIZE = 0
                return idle_tx_msg

            if apps.core.generative_ai.utils.constant_utils.ACTIVE_TOOL_RETRY_COUNT > self.assistant.tool_max_attempts_per_instance:

                idle_tx_msg = get_maximum_tool_attempts_reached_log(
                    final_response=final_resp
                )

                transmit_websocket_log(
                    f"""🚨 Maximum same tool attempt limit has been reached. Cancelling the process.""",
                    stop_tag=BIMOD_PROCESS_END,
                    chat_id=self.chat.id,
                    sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                    fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                    fermion__export_type=fermion__export_type,
                    fermion__endpoint=fermion__endpoint
                )

                try:
                    failure_tx = LLMTransaction.objects.create(
                        organization=self.chat.organization,
                        model=self.chat.assistant.llm_model,
                        responsible_user=self.chat.user,
                        responsible_assistant=self.chat.assistant,
                        encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                        transaction_context_content=idle_tx_msg,
                        llm_cost=0,
                        internal_service_cost=0,
                        tax_cost=0,
                        total_cost=0,
                        total_billable_cost=0,
                        transaction_type=ChatRoles.ASSISTANT,
                        transaction_source=self.chat.chat_source
                    )

                    self.chat.transactions.add(failure_tx)
                    self.chat.save()

                except Exception as e:
                    logger.error(f"Error occurred while saving the transaction: {str(e)}")

                    transmit_websocket_log(
                        f"""🚨 A critical error occurred while saving the transaction. Cancelling the process.""",
                        stop_tag=BIMOD_PROCESS_END,
                        chat_id=self.chat.id,
                        sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                        fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                        fermion__export_type=fermion__export_type,
                        fermion__endpoint=fermion__endpoint
                    )

                    return idle_tx_msg

                apps.core.generative_ai.utils.constant_utils.ACTIVE_TOOL_RETRY_COUNT = 0

                return idle_tx_msg

            apps.core.generative_ai.utils.constant_utils.ACTIVE_TOOL_RETRY_COUNT += 1

            transmit_websocket_log(
                f"""🧰 Identifying the valid tool usage calls...""",
                chat_id=self.chat.id,
                sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                fermion__export_type=fermion__export_type,
                fermion__endpoint=fermion__endpoint
            )

            json_content_of_resp = find_tool_call_from_json(final_resp)

            transmit_websocket_log(
                f"""💡️ Tool usage calls have been identified.""",
                chat_id=self.chat.id,
                sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                fermion__export_type=fermion__export_type,
                fermion__endpoint=fermion__endpoint
            )

            transmit_websocket_log(
                f"""🧭 Number of tool usage calls that is delivered: {len(json_content_of_resp)}""",
                chat_id=self.chat.id,
                sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                fermion__export_type=fermion__export_type,
                fermion__endpoint=fermion__endpoint
            )

            tool_name = None
            for i, json_part in enumerate(json_content_of_resp):

                transmit_websocket_log(
                    f"""🧮 Executing the tool usage call index: {i + 1} out of {len(json_content_of_resp)} ... """,
                    chat_id=self.chat.id,
                    sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                    fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                    fermion__export_type=fermion__export_type,
                    fermion__endpoint=fermion__endpoint
                )

                try:

                    tool_xc = ToolCallManager(
                        assistant=self.assistant,
                        chat=self.chat,
                        tool_usage_json_str=json_part
                    )

                    tool_resp, tool_name, file_uris, image_uris = tool_xc.call_internal_tool_service()

                    transmit_websocket_log(
                        f"""🧰 Tool usage call for: '{tool_name}' has been successfully executed. Proceeding with the next actions...""",
                        chat_id=self.chat.id,
                        sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                        fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                        fermion__export_type=fermion__export_type,
                        fermion__endpoint=fermion__endpoint
                    )

                    if tool_name is not None and tool_name != prev_tool_name:
                        apps.core.generative_ai.utils.constant_utils.ACTIVE_CHAIN_SIZE += 1
                        prev_tool_name = tool_name

                    transmit_websocket_log(
                        f"""📦 Tool response from '{tool_name}' is being delivered to the assistant for further actions...""",
                        chat_id=self.chat.id,
                        sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                        fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                        fermion__export_type=fermion__export_type,
                        fermion__endpoint=fermion__endpoint
                    )

                    tool_resp_list.append(
                        json.dumps(
                            {
                                "tool_name": tool_name,
                                "tool_response": tool_resp,
                                "file_uris": file_uris,
                                "status": "SUCCESS",
                                "image_uris": image_uris
                            },
                            indent=4
                        )
                    )

                    transmit_websocket_log(
                        f"""🎯 Tool response from '{tool_name}' has been successfully delivered to the assistant.""",
                        chat_id=self.chat.id,
                        sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                        fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                        fermion__export_type=fermion__export_type,
                        fermion__endpoint=fermion__endpoint
                    )

                except Exception as e:
                    logger.error(f"Error occurred while executing the tool: {str(e)}")

                    transmit_websocket_log(
                        f"""🚨 Error occurred while executing the tool. Attempting to recover...""",
                        chat_id=self.chat.id,
                        sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                        fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                        fermion__export_type=fermion__export_type,
                        fermion__endpoint=fermion__endpoint
                    )

                    if tool_name is not None:
                        tool_resp = get_json_decode_error_log(
                            error_logs=str(e)
                        )

                        tool_resp_list.append(
                            json.dumps(
                                {
                                    "tool_name": tool_name,
                                    "tool_response": tool_resp,
                                    "file_uris": [],
                                    "image_uris": [],
                                    "status": "FAILED",
                                    "error_logs": str(e)
                                },
                                indent=4
                            )
                        )

                    else:
                        tool_resp = get_json_decode_error_log(
                            error_logs=str(e)
                        )

                        tool_resp_list.append(
                            json.dumps(
                                {
                                    "tool_name": "NO VALID TOOL NAME",
                                    "tool_response": tool_resp,
                                    "file_uris": [],
                                    "image_uris": [],
                                    "status": "FAILED",
                                    "error_logs": str(e)
                                }
                            )
                        )

                    transmit_websocket_log(
                        f""" 🚨 Error logs have been delivered to the assistant. Proceeding with the next actions... """,
                        chat_id=self.chat.id,
                        sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                        fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                        fermion__export_type=fermion__export_type,
                        fermion__endpoint=fermion__endpoint
                    )

        transmit_websocket_log(
            f"""🧠 The assistant is inspecting the responses of the tools...""",
            chat_id=self.chat.id,
            sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
            fermion__is_fermion_supervised=fermion__is_fermion_supervised,
            fermion__export_type=fermion__export_type,
            fermion__endpoint=fermion__endpoint
        )

        if tool_resp_list:

            transmit_websocket_log(
                f"""📦 Communication records for the tool requests are being prepared...""",
                chat_id=self.chat.id,
                sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                fermion__export_type=fermion__export_type,
                fermion__endpoint=fermion__endpoint
            )

            try:

                tool_request = MultimodalChatMessage.objects.create(
                    multimodal_chat=self.chat,
                    sender_type=ChatRoles.ASSISTANT.upper(),
                    message_text_content=embed_tool_call_in_prompt(
                        json_parts_of_response=json_content_of_resp
                    ),
                    message_file_contents=[],
                    message_image_contents=[]
                )

                self.chat.chat_messages.add(
                    tool_request
                )

                self.chat.save()

                transmit_websocket_log(
                    f""" ⚙️ Tool request records have been prepared. Proceeding with the next actions...""",
                    chat_id=self.chat.id,
                    sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                    fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                    fermion__export_type=fermion__export_type,
                    fermion__endpoint=fermion__endpoint
                )

            except Exception as e:

                logger.error(f"Error occurred while recording the tool request: {str(e)}")

                transmit_websocket_log(
                    f"""🚨 A critical error occurred while recording the tool request. Cancelling the process.""",
                    stop_tag=BIMOD_PROCESS_END,
                    chat_id=self.chat.id,
                    sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                    fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                    fermion__export_type=fermion__export_type,
                    fermion__endpoint=fermion__endpoint
                )

                return DEFAULT_ERROR_MESSAGE

            try:
                transmit_websocket_log(
                    f""" 📦 Communication records for the tool responses are being prepared... """,
                    chat_id=self.chat.id,
                    sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                    fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                    fermion__export_type=fermion__export_type,
                    fermion__endpoint=fermion__endpoint
                )

                tool_message = MultimodalChatMessage.objects.create(
                    multimodal_chat=self.chat,
                    sender_type=HistoryBuilder.ChatRoles.TOOL.upper(),
                    message_text_content=str(tool_resp_list),
                    message_file_contents=file_uris,
                    message_image_contents=image_uris
                )

                self.chat.chat_messages.add(
                    tool_message
                )

                self.chat.save()

                transmit_websocket_log(
                    f"""⚙️ Tool response records have been prepared. Proceeding with the next actions...""",
                    chat_id=self.chat.id,
                    sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                    fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                    fermion__export_type=fermion__export_type,
                    fermion__endpoint=fermion__endpoint
                )

            except Exception as e:

                logger.error(f"Error occurred while recording the tool response: {str(e)}")

                transmit_websocket_log(
                    f""" 🚨 A critical error occurred while recording the tool response. Cancelling the process. """,
                    stop_tag=BIMOD_PROCESS_END,
                    chat_id=self.chat.id,
                    sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                    fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                    fermion__export_type=fermion__export_type,
                    fermion__endpoint=fermion__endpoint
                )
                return DEFAULT_ERROR_MESSAGE

            transmit_websocket_log(
                f"""✨ Communication records for the tool requests and responses have been successfully prepared.""",
                chat_id=self.chat.id,
                sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                fermion__export_type=fermion__export_type,
                fermion__endpoint=fermion__endpoint
            )

            transmit_websocket_log(
                f"""📦 Transactions are being prepared for the current level of operations...""",
                chat_id=self.chat.id,
                sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                fermion__export_type=fermion__export_type,
                fermion__endpoint=fermion__endpoint
            )

            try:
                LLMTransaction.objects.create(
                    organization=self.chat.organization,
                    model=self.chat.assistant.llm_model,
                    responsible_user=self.chat.user,
                    responsible_assistant=self.chat.assistant,
                    encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                    transaction_context_content=str(tool_resp_list),
                    llm_cost=0,
                    internal_service_cost=0,
                    tax_cost=0,
                    total_cost=0,
                    total_billable_cost=0,
                    transaction_type=ChatRoles.ASSISTANT,
                    transaction_source=self.chat.chat_source
                )

            except Exception as e:
                logger.error(f"Error occurred while recording the transaction: {str(e)}")

                transmit_websocket_log(
                    f"""🚨 A critical error occurred while recording the transaction. Cancelling the process.""",
                    stop_tag=BIMOD_PROCESS_END,
                    chat_id=self.chat.id,
                    sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                    fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                    fermion__export_type=fermion__export_type,
                    fermion__endpoint=fermion__endpoint
                )

                return DEFAULT_ERROR_MESSAGE

            transmit_websocket_log(
                f"""❇️ Transactions have been successfully prepared for the current level of operations.""",
                chat_id=self.chat.id,
                sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                fermion__export_type=fermion__export_type,
                fermion__endpoint=fermion__endpoint
            )

            transmit_websocket_log(
                f"""🚀 The assistant is getting prepared for the next level of operations...""",
                chat_id=self.chat.id,
                sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
                fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                fermion__export_type=fermion__export_type,
                fermion__endpoint=fermion__endpoint
            )

            return self.respond_stream(
                latest_message=tool_message,
                prev_tool_name=prev_tool_name,
                with_media=with_media,
                file_uris=file_uris,
                image_uris=image_uris,
                result_affirmed=False,
            )

        transmit_websocket_log(
            f""" ✅ The assistant has successfully processed the query. The response is being delivered to the user...""",
            stop_tag=BIMOD_PROCESS_END,
            chat_id=self.chat.id,
            sender_type=TransmitWebsocketLogSenderType.ASSISTANT,
            fermion__is_fermion_supervised=fermion__is_fermion_supervised,
            fermion__export_type=fermion__export_type,
            fermion__endpoint=fermion__endpoint
        )

        apps.core.generative_ai.utils.constant_utils.ACTIVE_CHAIN_SIZE = 0

        ###################################################################
        # to check if tools are attempted by assistant, run one more time
        ###################################################################

        if result_affirmed is False:
            # Save the assistants message

            latest_message = MultimodalChatMessage.objects.create(
                multimodal_chat=self.chat,
                sender_type=ChatRoles.ASSISTANT.upper(),
                hidden=True,
                message_text_content=f"""
                    Your last response in conversation history:

                    '''

                    {latest_message.message_text_content}

                    '''

                    -------------------------

                    [1] If you don't need to do anything: Write a follow up message, depending on the context and conversation history.
                    [2] If in the previous message you decided to use a tool, proceed into the tool usage directly.
                    [3] If you provided an important piece of data in the previous message, you can interpret this data to make it more clear for the user.

                    -------------------------
                """,
            )

            final_resp = self.respond_stream(
                latest_message=latest_message,
                prev_tool_name=prev_tool_name,
                with_media=with_media,
                file_uris=file_uris,
                image_uris=image_uris,
                result_affirmed=True,
            )

        ###################################################################
        ###################################################################

        if with_media:
            return final_resp, file_uris, image_uris

        return final_resp
