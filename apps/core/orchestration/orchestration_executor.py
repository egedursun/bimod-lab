#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: orchestration_executor.py
#  Last Modified: 2024-10-05 02:25:59
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
import json
import logging

from apps.core.generative_ai.utils import (
    find_tool_call_from_json,
    ChatRoles
)

from apps.core.orchestration.orchestration_tool_manager import (
    OrchestrationToolManager
)

from apps.core.orchestration.prompts.calls.build_maestro_to_assistant_instructions import (
    build_maestro_to_assistant_instructions_prompt
)

from apps.core.orchestration.prompts.orchestration_history_builder import (
    OrchestrationHistoryBuilder
)

from apps.core.orchestration.prompts.orchestration_prompt_builder import (
    OrchestrationPromptBuilder
)

from apps.core.orchestration.utils import (
    embed_orchestration_tool_call_in_prompt,
    DEFAULT_ORCHESTRATION_ERROR_MESSAGE,
    DEFAULT_WORKER_ASSISTANT_ERROR_MESSAGE,
)

from apps.assistants.models import Assistant

from apps.core.sinaptera.sinaptera_executor import (
    SinapteraBoosterManager
)
from apps.core.sinaptera.utils import (
    SinapteraCallerTypes
)

from apps.multimodal_chat.models import (
    MultimodalChat,
    MultimodalChatMessage
)

from apps.multimodal_chat.utils import (
    BIMOD_NO_TAG_PLACEHOLDER,
    BIMOD_STREAMING_END_TAG,
    BIMOD_PROCESS_END,
    SourcesForMultimodalChatsNames,
    transmit_websocket_log,
    TransmitWebsocketLogSenderType
)

from apps.orchestrations.models import (
    OrchestrationQuery,
    OrchestrationQueryLog
)

from apps.orchestrations.utils import (
    OrchestrationQueryLogTypesNames
)

logger = logging.getLogger(__name__)


class OrchestrationExecutor:

    def __init__(
        self,
        maestro,
        query_chat
    ):

        from apps.core.generative_ai.gpt_openai_manager import (
            OpenAIGPTClientManager
        )

        self.maestro = maestro
        self.query_chat: OrchestrationQuery = query_chat

        ############################################################################################################

        self.client = OpenAIGPTClientManager.get_naked_client(
            llm_model=self.maestro.llm_model
        )

        ############################################################################################################

        self.worker_chats = {
            # ___________________________________________#
            # This dictionary is to be filled with IDs of the Worker Assistants' chats as they get created.
            #       `worker_assistant_id: chat_id`,
            #       `worker_assistant_id: chat_id`,
            #        ...
            # ...
            # ___________________________________________#
        }

    def execute_for_query(
        self,
        latest_message=None,
        fs_urls=None,
        img_urls=None,
        result_affirmed=False,
    ):

        transmit_websocket_log(
            log_message=f""" 🤖 Orchestrator has started processing the query.""",
            chat_id=self.query_chat.id,
            sender_type=TransmitWebsocketLogSenderType.ORCHESTRATION,
        )

        query_chat = self.query_chat

        try:
            c = self.client
            user = self.query_chat.created_by_user
            logger.info(f"User: {user}")

        except Exception as e:
            logger.error(f"Error while setting the connection and user: {e}")

            transmit_websocket_log(
                log_message=f"""🚨 Error while setting the connection and user: {e}""",
                chat_id=self.query_chat.id,
                sender_type=TransmitWebsocketLogSenderType.ORCHESTRATION,
            )

            return DEFAULT_ORCHESTRATION_ERROR_MESSAGE

        transmit_websocket_log(
            log_message=f"""📡 Connection and user are successfully set.""",
            chat_id=self.query_chat.id,
            sender_type=TransmitWebsocketLogSenderType.ORCHESTRATION,
        )

        try:
            prompt_msgs = [
                OrchestrationPromptBuilder.build(
                    query_chat=self.query_chat,
                    maestro=self.maestro,
                    user=user,
                    role=ChatRoles.SYSTEM
                )
            ]

        except Exception as e:

            logger.error(f"Error while creating the system prompt for the orchestration process: {e}")

            transmit_websocket_log(
                log_message=f"""🚨 Error while creating the system prompt for the orchestration process: {e}""",
                chat_id=self.query_chat.id,
                sender_type=TransmitWebsocketLogSenderType.ORCHESTRATION,
            )

            return DEFAULT_ORCHESTRATION_ERROR_MESSAGE

        transmit_websocket_log(
            log_message=f"""📝 System prompt is successfully created.""",
            chat_id=self.query_chat.id,
            sender_type=TransmitWebsocketLogSenderType.ORCHESTRATION,
        )

        try:
            prompt_msgs.extend(
                OrchestrationHistoryBuilder.build(
                    query_chat=query_chat
                )
            )

        except Exception as e:

            logger.error(f"Error while creating the history prompt for the orchestration process: {e}")

            transmit_websocket_log(
                log_message=f"""🚨 Error while creating the history prompt for the orchestration process: {e}""",
                chat_id=self.query_chat.id,
                sender_type=TransmitWebsocketLogSenderType.ORCHESTRATION,
            )

            return DEFAULT_ORCHESTRATION_ERROR_MESSAGE

        transmit_websocket_log(
            log_message=f"""📝 History prompt is successfully created. """,
            chat_id=self.query_chat.id,
            sender_type=TransmitWebsocketLogSenderType.ORCHESTRATION,
        )

        transmit_websocket_log(
            log_message=f""" 📡 Generating response in cooperation with the orchestrator...""",
            chat_id=self.query_chat.id,
            sender_type=TransmitWebsocketLogSenderType.ORCHESTRATION,
        )

        try:

            tree_booster: SinapteraBoosterManager = SinapteraBoosterManager(
                user=user,
                llm_core=self.query_chat.maestro.llm_model,
                caller_type=SinapteraCallerTypes.ORCHESTRATOR,
            )

            if (
                tree_booster.sinaptera_configuration.is_active_on_assistants is True and
                result_affirmed is False
            ):

                resp = tree_booster.execute(
                    structured_conversation_history=prompt_msgs,
                    chat_id=self.query_chat.id,
                )

            else:

                resp = c.chat.completions.create(
                    model=self.maestro.llm_model.model_name,
                    messages=prompt_msgs,
                    temperature=float(self.maestro.llm_model.temperature),
                    frequency_penalty=float(self.maestro.llm_model.frequency_penalty),
                    presence_penalty=float(self.maestro.llm_model.presence_penalty),
                    max_tokens=int(self.maestro.llm_model.maximum_tokens),
                    top_p=float(self.maestro.llm_model.top_p)
                )

        except Exception as e:
            logger.error(f"Error occurred while retrieving the response from the language model: {str(e)}")

            transmit_websocket_log(
                f"""🚨 A critical error occurred while retrieving the response from the language model.""",
                stop_tag=BIMOD_PROCESS_END,
                chat_id=self.maestro.id,
                sender_type=TransmitWebsocketLogSenderType.ORCHESTRATION,
            )

            return DEFAULT_ORCHESTRATION_ERROR_MESSAGE

        transmit_websocket_log(
            f"""🧨 Response streamer is ready to process the response. """,
            chat_id=self.query_chat.id,
            sender_type=TransmitWebsocketLogSenderType.ORCHESTRATION,
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
                chat_id=self.query_chat.id,
                sender_type=TransmitWebsocketLogSenderType.ORCHESTRATION,
            )

            transmit_websocket_log(
                f"""""",
                stop_tag=BIMOD_STREAMING_END_TAG,
                chat_id=self.query_chat.id,
                sender_type=TransmitWebsocketLogSenderType.ORCHESTRATION,
            )

            transmit_websocket_log(
                f"""🔌 Generation iterations has been successfully accomplished.""",
                chat_id=self.query_chat.id,
                sender_type=TransmitWebsocketLogSenderType.ORCHESTRATION,
            )

            transmit_websocket_log(
                f"""📦 Preparing the response...""",
                chat_id=self.query_chat.id,
                sender_type=TransmitWebsocketLogSenderType.ORCHESTRATION,
            )

        except Exception as e:
            logger.error(f"Error occurred while processing the response from the language model: {str(e)}")

            transmit_websocket_log(
                f""" 🚨 A critical error occurred while processing the response from the language model.""",
                stop_tag=BIMOD_PROCESS_END,
                chat_id=self.query_chat.id,
                sender_type=TransmitWebsocketLogSenderType.ORCHESTRATION,
            )

            return DEFAULT_ORCHESTRATION_ERROR_MESSAGE

        transmit_websocket_log(
            log_message=f"""🕹️ Raw Orchestration response stream has been successfully delivered.""",
            chat_id=self.query_chat.id,
            sender_type=TransmitWebsocketLogSenderType.ORCHESTRATION,
        )

        final_resp = acc_resp

        final_resp_object = OrchestrationQueryLog.objects.create(
            orchestration_query=self.query_chat,
            log_type=OrchestrationQueryLogTypesNames.MAESTRO_ANSWER,
            log_text_content=final_resp,
            log_file_contents=[],
            log_image_contents=[],
        )

        transmit_websocket_log(
            log_message=f"""🧲 Transactional information has been successfully processed.""",
            chat_id=self.query_chat.id,
            sender_type=TransmitWebsocketLogSenderType.ORCHESTRATION,
        )

        tool_name, agent_id = None, None
        tool_resp_list, json_content_of_resp = [], []

        if find_tool_call_from_json(final_resp):

            transmit_websocket_log(
                log_message=f"""🛠️ Worker assistant call detected in the response. Processing with the worker execution steps...""",
                chat_id=self.query_chat.id,
                sender_type=TransmitWebsocketLogSenderType.ORCHESTRATION,
            )

            transmit_websocket_log(
                log_message=f"""🧰 Identifying the valid worker assistant calls...""",
                chat_id=self.query_chat.id,
                sender_type=TransmitWebsocketLogSenderType.ORCHESTRATION,
            )

            json_content_of_resp = find_tool_call_from_json(final_resp)

            transmit_websocket_log(
                log_message=f""" 💡️ Worker assistant usage calls have been identified. """,
                chat_id=self.query_chat.id,
                sender_type=TransmitWebsocketLogSenderType.ORCHESTRATION,
            )

            tool_name, tool_resp = None, None

            for i, json_part in enumerate(json_content_of_resp):

                transmit_websocket_log(
                    log_message=f"""🧮 Executing the worker assistant call... """,
                    chat_id=self.query_chat.id,
                    sender_type=TransmitWebsocketLogSenderType.ORCHESTRATION,
                )

                try:

                    tool_xc = OrchestrationToolManager(
                        maestro=self.maestro,
                        query_chat=self.query_chat,
                        tool_usage_json_str=json_part
                    )

                    tool_resp, tool_name, agent_id, fs_urls, img_urls = tool_xc.use_tool()

                    agent = Assistant.objects.get(
                        id=agent_id
                    )

                    transmit_websocket_log(
                        log_message=f""" 🧰 Worker Assistant call to: {agent.name} has been successfully delivered. """,
                        chat_id=self.query_chat.id,
                        sender_type=TransmitWebsocketLogSenderType.ORCHESTRATION,
                    )

                    transmit_websocket_log(
                        log_message=f""" 📦 Worker Assistant Response from: '{agent.name}' is being delivered to the Orchestrator for further actions...""",
                        chat_id=self.query_chat.id,
                        sender_type=TransmitWebsocketLogSenderType.ORCHESTRATION,
                    )

                    transmit_websocket_log(
                        log_message=f"""🎯 Tool response from: '{agent.name}' has been successfully delivered to the Orchestrator.""",
                        chat_id=self.query_chat.id,
                        sender_type=TransmitWebsocketLogSenderType.ORCHESTRATION,
                    )

                    tool_resp_list.append(
                        json.dumps(
                            {
                                "tool_name": tool_name,
                                "tool_response": tool_resp,
                                "file_uris": fs_urls,
                                "status": "SUCCESS",
                                "image_uris": img_urls,
                            },
                            indent=4
                        )
                    )

                except Exception as e:

                    logger.error(f"Error occurred while calling the worker assistant: {e}")

                    transmit_websocket_log(
                        log_message=f"""🚨 Error occurred while calling the worker assistant. Attempting to recover... """,
                        chat_id=self.query_chat.id,
                        sender_type=TransmitWebsocketLogSenderType.ORCHESTRATION,
                    )

                    if tool_name is not None:
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
                        log_message=f"""🚨 Error logs have been delivered to the assistant. Proceeding with the next actions...""",
                        chat_id=self.query_chat.id,
                        sender_type=TransmitWebsocketLogSenderType.ORCHESTRATION,
                    )

        transmit_websocket_log(
            log_message=f""" 🧠 The Orchestrator is inspecting the responses of the worker assistants... """,
            chat_id=self.query_chat.id,
            sender_type=TransmitWebsocketLogSenderType.ORCHESTRATION,
        )

        if tool_resp_list:

            transmit_websocket_log(
                log_message=f"""📦 Orchestration records for the worker tool calls are being prepared...""",
                chat_id=self.query_chat.id,
                sender_type=TransmitWebsocketLogSenderType.ORCHESTRATION,
            )

            try:

                self.query_chat: OrchestrationQuery

                tool_req = OrchestrationQueryLog.objects.create(
                    orchestration_query=self.query_chat,
                    log_type=OrchestrationQueryLogTypesNames.WORKER_REQUEST,
                    log_text_content=embed_orchestration_tool_call_in_prompt(
                        json_part=json_content_of_resp
                    ),
                    log_file_contents=[],
                    log_image_contents=[],
                    context_worker=Assistant.objects.get(
                        id=agent_id
                    )
                )

                self.query_chat.logs.add(
                    tool_req
                )

                self.query_chat.save()

                transmit_websocket_log(
                    log_message=f"""⚙️ Worker Assistant call records have been prepared. Proceeding with the next actions... """,
                    chat_id=self.query_chat.id,
                    sender_type=TransmitWebsocketLogSenderType.ORCHESTRATION,
                )

            except Exception as e:

                logger.error(f"Error occurred while recording the tool request: {e}")

                transmit_websocket_log(
                    log_message=f""" 🚨 A critical error occurred while recording the tool request. Cancelling the process.""",
                    chat_id=self.query_chat.id,
                    stop_tag=BIMOD_PROCESS_END,
                    sender_type=TransmitWebsocketLogSenderType.ORCHESTRATION,
                )

                return DEFAULT_ORCHESTRATION_ERROR_MESSAGE

            try:

                transmit_websocket_log(
                    log_message=f"""📦 Orchestration communication records for the Worker Assistant responses are being prepared...""",
                    chat_id=self.query_chat.id,
                    sender_type=TransmitWebsocketLogSenderType.ORCHESTRATION,
                )

                tool_msg = OrchestrationQueryLog.objects.create(
                    orchestration_query=self.query_chat,
                    log_type=OrchestrationQueryLogTypesNames.WORKER_RESPONSE,
                    log_text_content=str(tool_resp_list),
                    log_file_contents=fs_urls,
                    log_image_contents=img_urls,
                    context_worker=Assistant.objects.get(
                        id=agent_id
                    )
                )

                self.query_chat.logs.add(
                    tool_msg
                )

                self.query_chat.save()

                transmit_websocket_log(
                    log_message=f"""⚙️ Worker Assistant response records have been prepared. Proceeding with the next actions... """,
                    chat_id=self.query_chat.id,
                    sender_type=TransmitWebsocketLogSenderType.ORCHESTRATION,
                )

            except Exception as e:

                logger.error(f"Error occurred while recording the Worker Assistant response: {e}")

                transmit_websocket_log(
                    log_message=f"""🚨 A critical error occurred while recording the Worker Assistant response. Cancelling the process.""",
                    chat_id=self.query_chat.id,
                    stop_tag=BIMOD_PROCESS_END,
                    sender_type=TransmitWebsocketLogSenderType.ORCHESTRATION,
                )

                return DEFAULT_ORCHESTRATION_ERROR_MESSAGE

            transmit_websocket_log(
                log_message=f"""❇️ Orchestrator transactions have been successfully prepared for the current level of operations.""",
                chat_id=self.query_chat.id,
                sender_type=TransmitWebsocketLogSenderType.ORCHESTRATION,
            )

            transmit_websocket_log(
                log_message=f""" 🚀 The Orchestrator is getting prepared for the next level of operations... """,
                chat_id=self.query_chat.id,
                sender_type=TransmitWebsocketLogSenderType.ORCHESTRATION,
            )

            return self.execute_for_query(
                fs_urls=fs_urls,
                img_urls=img_urls,
                latest_message=final_resp_object,
                result_affirmed=False,
            )

        transmit_websocket_log(
            log_message=f"""❇️❇️ Orchestrator has accomplished the operation processes!""",
            chat_id=self.query_chat.id,
            stop_tag=BIMOD_PROCESS_END,
            sender_type=TransmitWebsocketLogSenderType.ORCHESTRATION,
        )

        ###################################################################
        # to check if tools are attempted by assistant, run one more time
        ###################################################################

        if result_affirmed is False:
            # Save the assistants message

            OrchestrationQueryLog.objects.create(
                orchestration_query=self.query_chat,
                log_type=OrchestrationQueryLogTypesNames.MAESTRO_ANSWER,
                hidden=True,
                log_text_content=f"""
                    Your last response in conversation history:

                    '''

                    {final_resp_object.log_text_content}

                    '''

                    -------------------------

                    [1] If you don't need to do anything: Write a follow up message, depending on the context and conversation history.
                    [2] If in the previous message you decided to use a tool, proceed into the tool usage directly.
                    [3] If you provided an important piece of data in the previous message, you can interpret this data to make it more clear for the user.

                    -------------------------
                """,
            )

            final_resp_object = self.execute_for_query(
                fs_urls=fs_urls,
                img_urls=img_urls,
                latest_message=final_resp_object,
                result_affirmed=True,
            )

        ###################################################################
        ###################################################################

        return final_resp_object

    def ask_worker_assistant(
        self,
        assistant_id,
        maestro_query,
        file_urls=None,
        image_urls=None
    ):

        transmit_websocket_log(
            log_message=f"""🧑‍🚀 >> Worker Assistant began processing the order. """,
            chat_id=self.query_chat.id,
            sender_type=TransmitWebsocketLogSenderType.ORCHESTRATION,
        )

        transmit_websocket_log(
            log_message=f"""🧑‍🚀⚙️ >> Worker Assistant is preparing the instructions for the order.""",
            chat_id=self.query_chat.id,
            sender_type=TransmitWebsocketLogSenderType.ORCHESTRATION,
        )

        structured_maestro_order = build_maestro_to_assistant_instructions_prompt(
            maestro_query_text=maestro_query
        )

        transmit_websocket_log(
            log_message=f"""🧑‍🚀✅ >> Worker Assistant has successfully prepared the instructions for the order.""",
            chat_id=self.query_chat.id,
            sender_type=TransmitWebsocketLogSenderType.ORCHESTRATION,
        )

        if assistant_id in self.worker_chats:

            transmit_websocket_log(
                log_message=f"""🧑‍🚀🔍 >> Worker Assistant already has a chat object. Connecting to the chat object...""",
                chat_id=self.query_chat.id,
                sender_type=TransmitWebsocketLogSenderType.ORCHESTRATION,
            )

            chat_id = self.worker_chats[
                assistant_id
            ]

            chat = MultimodalChat.objects.get(
                id=chat_id
            )

            agent = Assistant.objects.get(
                id=assistant_id
            )

        else:

            transmit_websocket_log(
                log_message=f"""🧑‍🚀🔧 >> Worker Assistant does not yet have a chat object. Creating a chat object for the assistant... """,
                chat_id=self.query_chat.id,
                sender_type=TransmitWebsocketLogSenderType.ORCHESTRATION,
            )

            try:
                agent = Assistant.objects.get(
                    id=assistant_id
                )
                new_chat_object = MultimodalChat.objects.create(
                    organization=self.maestro.organization,
                    assistant=agent,
                    user=self.query_chat.created_by_user,
                    chat_source=SourcesForMultimodalChatsNames.ORCHESTRATION,
                    is_archived=False,
                    created_by_user_id=self.query_chat.created_by_user.id)

                self.worker_chats[
                    assistant_id
                ] = new_chat_object.id

                chat_id = self.worker_chats[
                    assistant_id
                ]

                chat = MultimodalChat.objects.get(
                    id=chat_id
                )

                transmit_websocket_log(
                    log_message=f""" 🧑‍🚀🔧✅ >> Worker Assistant chat object has been successfully created.""",
                    chat_id=self.query_chat.id,
                    sender_type=TransmitWebsocketLogSenderType.ORCHESTRATION,
                )

            except Exception as e:
                logger.error(f"Error while creating the chat object for the Worker Assistant: {e}")

                transmit_websocket_log(
                    log_message=f"""🧑‍🚀🔧🚨 >> Error while creating the chat object for the Worker Assistant: {e}""",
                    chat_id=self.query_chat.id,
                    sender_type=TransmitWebsocketLogSenderType.ORCHESTRATION,
                )

                return DEFAULT_WORKER_ASSISTANT_ERROR_MESSAGE

        try:
            from apps.core.generative_ai.gpt_openai_manager import (
                OpenAIGPTClientManager
            )

            internal_llm_client = OpenAIGPTClientManager(
                assistant=agent,
                chat_object=chat
            )

        except Exception as e:
            logger.error(f"Error while creating the internal LLM client for the Worker Assistant: {e}")

            transmit_websocket_log(
                log_message=f"""🧑‍🚀🚨 Error while setting the connection and user: {e} """,
                chat_id=self.query_chat.id,
                sender_type=TransmitWebsocketLogSenderType.ORCHESTRATION,
            )

            return DEFAULT_WORKER_ASSISTANT_ERROR_MESSAGE

        if image_urls is not None:

            structured_maestro_order += """
                ---
                *IMAGE URLS*
            """

            for image_url in image_urls:
                structured_maestro_order += f"""
                - {image_url}
            """
            structured_maestro_order += "---"

        if file_urls is not None:

            structured_maestro_order += """
                *FILE URLS*
            """

            for file_url in file_urls:
                structured_maestro_order += f"""
                - {file_url}
            """

            structured_maestro_order += "---"

        structured_maestro_order_object = MultimodalChatMessage.objects.create(
            multimodal_chat=chat,
            sender_type='USER',
            message_text_content=structured_maestro_order,
            message_image_contents=image_urls,
            message_file_contents=file_urls
        )

        final_resp = internal_llm_client.respond_stream(
            latest_message=structured_maestro_order_object,
            image_uris=image_urls,
            file_uris=file_urls
        )

        MultimodalChatMessage.objects.create(
            multimodal_chat=chat,
            sender_type='ASSISTANT',
            message_text_content=final_resp
        )

        logger.info(f"Worker Assistant response is ready.")

        return final_resp
