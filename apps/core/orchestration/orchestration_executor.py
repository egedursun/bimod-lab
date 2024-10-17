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
import logging

import websockets

from apps.core.generative_ai.gpt_openai_manager import OpenAIGPTClientManager
from apps.core.generative_ai.utils import find_tool_call_from_json, ChatRoles
from apps.core.orchestration.orchestration_tool_manager import OrchestrationToolManager
from apps.core.orchestration.prompts.calls.build_maestro_to_assistant_instructions import \
    build_maestro_to_assistant_instructions_prompt
from apps.core.orchestration.prompts.orchestration_history_builder import OrchestrationHistoryBuilder
from apps.core.orchestration.prompts.orchestration_prompt_builder import OrchestrationPromptBuilder
from apps.core.orchestration.utils import send_orchestration_message, embed_orchestration_tool_call_in_prompt, \
    DEFAULT_ORCHESTRATION_ERROR_MESSAGE, DEFAULT_WORKER_ASSISTANT_ERROR_MESSAGE, \
    get_orchestration_json_decode_error_log
from apps.assistants.models import Assistant
from apps.multimodal_chat.models import MultimodalChat, MultimodalChatMessage
from apps.multimodal_chat.utils import BIMOD_NO_TAG_PLACEHOLDER, BIMOD_STREAMING_END_TAG, BIMOD_PROCESS_END, \
    SourcesForMultimodalChatsNames
from apps.orchestrations.models import OrchestrationQuery, OrchestrationQueryLog
from apps.orchestrations.utils import OrchestrationQueryLogTypesNames


logger = logging.getLogger(__name__)


class OrchestrationExecutor:

    def __init__(self, maestro, query_chat):
        self.maestro = maestro
        self.query_chat = query_chat
        ############################################################################################################
        self.client = OpenAIGPTClientManager.get_naked_client(llm_model=self.maestro.llm_model)
        ############################################################################################################
        self.worker_chats = {
            #___________________________________________#
            # This dictionary is to be filled with IDs of the Worker Assistants' chats as they get created.
            #       `worker_assistant_id: chat_id`,
            #       `worker_assistant_id: chat_id`,
            #        ...
            # ...
            #___________________________________________#
        }

    def execute_for_query(self, fs_urls=None, img_urls=None):
        send_orchestration_message(f"""
        🤖 Orchestrator has started processing the query.
        """, query_id=self.query_chat.id)

        query_chat = self.query_chat
        try:
            c = self.client
            user = self.query_chat.created_by_user
            logger.info(f"User: {user}")
        except Exception as e:
            logger.error(f"Error while setting the connection and user: {e}")
            send_orchestration_message(f"""
            🚨 Error while setting the connection and user: {e}
            """, query_id=self.query_chat.id)
            return DEFAULT_ORCHESTRATION_ERROR_MESSAGE

        send_orchestration_message(f"""
        📡 Connection and user are successfully set.
        """, query_id=self.query_chat.id)

        try:
            prompt_msgs = [
                OrchestrationPromptBuilder.build(
                    query_chat=self.query_chat, maestro=self.maestro, user=user, role=ChatRoles.SYSTEM
                )]
        except Exception as e:
            logger.error(f"Error while creating the system prompt for the orchestration process: {e}")
            send_orchestration_message(f"""
            🚨 Error while creating the system prompt for the orchestration process: {e}
            """, query_id=self.query_chat.id)
            return DEFAULT_ORCHESTRATION_ERROR_MESSAGE

        send_orchestration_message(f"""
        📝 System prompt is successfully created.
        """, query_id=self.query_chat.id)

        try:
            prompt_msgs.extend(OrchestrationHistoryBuilder.build(query_chat=query_chat))
        except Exception as e:
            logger.error(f"Error while creating the history prompt for the orchestration process: {e}")
            send_orchestration_message(f"""
            🚨 Error while creating the history prompt for the orchestration process: {e}
            """, query_id=self.query_chat.id)
            return DEFAULT_ORCHESTRATION_ERROR_MESSAGE

        send_orchestration_message(f"""
        📝 History prompt is successfully created.
        """, query_id=self.query_chat.id)
        send_orchestration_message(f"""
        📡 Generating response in cooperation with the orchestrator...
        """, query_id=self.query_chat.id)

        try:
            resp_chunks = c.chat.completions.create(
                model=self.maestro.llm_model.model_name, messages=prompt_msgs,
                temperature=float(self.maestro.llm_model.temperature),
                frequency_penalty=float(self.maestro.llm_model.frequency_penalty),
                presence_penalty=float(self.maestro.llm_model.presence_penalty),
                max_tokens=int(self.maestro.llm_model.maximum_tokens), top_p=float(self.maestro.llm_model.top_p),
                stream=True)
        except Exception as e:
            logger.error(f"Error occurred while generating the response in cooperation with the orchestrator: {e}")
            send_orchestration_message(f"""
            🚨 Error occurred while generating the response in cooperation with the orchestrator: {str(e)}
            """, query_id=self.query_chat.id)
            return DEFAULT_ORCHESTRATION_ERROR_MESSAGE

        send_orchestration_message(f"""
        🧨 Response streamer is ready to process the response.
        """, query_id=self.query_chat.id)

        try:
            send_orchestration_message(f"""
            ⚓ Orchestration Response generation is in progress...
            """, query_id=self.query_chat.id)

            acc_resp = ""
            for element in resp_chunks:
                choices = element.choices
                first_choice = choices[0]
                delta = first_choice.delta
                content = delta.content
                if content is not None:
                    acc_resp += content
                    send_orchestration_message(f"""{content}""", stop_tag=BIMOD_NO_TAG_PLACEHOLDER,
                                               query_id=self.query_chat.id)
            send_orchestration_message(f"""""", stop_tag=BIMOD_STREAMING_END_TAG,
                                       query_id=self.query_chat.id)

            send_orchestration_message(f"""
            🔌 Orchestration generation iterations has been successfully accomplished.
            """, query_id=self.query_chat.id)
            send_orchestration_message(f"""
            📦 Orchestrator is preparing the response...
            """, query_id=self.query_chat.id)
        except Exception as e:
            logger.error(f"Error occurred while processing the Orchestration response from the language model: {e}")
            send_orchestration_message(f"""
            🚨 A critical error occurred while processing the Orchestration response from the language model.
            """, stop_tag=BIMOD_PROCESS_END, query_id=self.query_chat.id)
            return DEFAULT_ORCHESTRATION_ERROR_MESSAGE

        send_orchestration_message(f"""
        🕹️ Raw Orchestration response stream has been successfully delivered.
        """, query_id=self.query_chat.id)

        final_resp = acc_resp
        send_orchestration_message(f"""
        🧲 Transactional information has been successfully processed.
        """, query_id=self.query_chat.id)

        tool_name, agent_id = None, None
        tool_resp, json_part = None, None
        if find_tool_call_from_json(final_resp):
            send_orchestration_message(f"""
            🛠️ Worker assistant call detected in the response. Processing with the worker execution steps...
            """, query_id=self.query_chat.id)
            send_orchestration_message(f"""
            🧰 Identifying the valid worker assistant calls...
            """, query_id=self.query_chat.id)

            json_part = find_tool_call_from_json(final_resp)[0]  # for now only a single JSON at a time
            send_orchestration_message(f"""
            💡️ Worker assistant usage call has been identified.
            """, query_id=self.query_chat.id)

            send_orchestration_message(f"""
            🧮 Executing the worker assistant call...
            """, query_id=self.query_chat.id)
            try:
                tool_xc = OrchestrationToolManager(
                    maestro=self.maestro, query_chat=self.query_chat, tool_usage_json_str=json_part)
                tool_resp, tool_name, agent_id, fs_urls, img_urls = tool_xc.use_tool()
                agent = Assistant.objects.get(id=agent_id)
                send_orchestration_message(f"""
                 🧰 Worker Assistant call to: {agent.name} has been successfully delivered.
                """, query_id=self.query_chat.id)

                send_orchestration_message(f"""
                📦 Worker Assistant Response from: '{agent.name}' is being delivered to the Orchestrator for further actions...
                """, query_id=self.query_chat.id)
                send_orchestration_message(f"""
                 🎯 Tool response from: '{agent.name}' has been successfully delivered to the Orchestrator.
                """, query_id=self.query_chat.id)

            except Exception as e:
                logger.error(f"Error occurred while calling the worker assistant: {e}")
                send_orchestration_message(f"""
                🚨 Error occurred while calling the worker assistant. Attempting to recover...
                """, query_id=self.query_chat.id)

                if tool_name is not None:
                    tool_resp = f"""
                         ---
                         There has been an error while executing the tool: {tool_name}
                         Insights:
                            - Tool Name field is not None, unlikely to be related to the lack of tool in the system.
                         Error Log: {get_orchestration_json_decode_error_log(error_logs=str(e))}
                         ---
                    """
                else:
                    tool_resp = f"""
                        ---
                        There has been an error while executing the tool.
                        Insights:
                            - Tool Name field is None, likely to be related to the lack of tool in the system.
                        Error Log: {get_orchestration_json_decode_error_log(error_logs=str(e))}
                        ---
                    """

                send_orchestration_message(f"""
                🚨 Error logs have been delivered to the assistant. Proceeding with the next actions...
                """, query_id=self.query_chat.id)

        send_orchestration_message(f"""
        🧠 The Orchestrator is inspecting the responses of the worker assistants...
        """, query_id=self.query_chat.id)
        if tool_resp is not None:
            send_orchestration_message(f"""
            📦 Orchestration records for the worker tool calls are being prepared...
            """, query_id=self.query_chat.id)

            try:
                self.query_chat: OrchestrationQuery
                tool_req = OrchestrationQueryLog.objects.create(
                    orchestration_query=self.query_chat, log_type=OrchestrationQueryLogTypesNames.WORKER_REQUEST,
                    log_text_content=embed_orchestration_tool_call_in_prompt(json_part=json_part),
                    log_file_contents=[], log_image_contents=[], context_worker=Assistant.objects.get(id=agent_id))
                self.query_chat.logs.add(tool_req)
                self.query_chat.save()
                send_orchestration_message(f"""
                ⚙️ Worker Assistant call records have been prepared. Proceeding with the next actions...
                """, query_id=self.query_chat.id)
            except Exception as e:
                logger.error(f"Error occurred while recording the tool request: {e}")
                send_orchestration_message(f"""
                🚨 A critical error occurred while recording the tool request. Cancelling the process.
                """, stop_tag=BIMOD_PROCESS_END, query_id=self.query_chat.id)
                return DEFAULT_ORCHESTRATION_ERROR_MESSAGE

            try:
                send_orchestration_message(f"""
                📦 Orchestration communication records for the Worker Assistant responses are being prepared...
                """, query_id=self.query_chat.id)
                tool_msg = OrchestrationQueryLog.objects.create(
                    orchestration_query=self.query_chat, log_type=OrchestrationQueryLogTypesNames.WORKER_RESPONSE,
                    log_text_content=str(tool_resp), log_file_contents=fs_urls, log_image_contents=img_urls,
                    context_worker=Assistant.objects.get(id=agent_id))
                self.query_chat.logs.add(tool_msg)
                self.query_chat.save()

                send_orchestration_message(f"""
                ⚙️ Worker Assistant response records have been prepared. Proceeding with the next actions...
                """, query_id=self.query_chat.id)
            except Exception as e:
                logger.error(f"Error occurred while recording the Worker Assistant response: {e}")
                send_orchestration_message(f"""
                🚨 A critical error occurred while recording the Worker Assistant response. Cancelling the process.
                """, stop_tag=BIMOD_PROCESS_END, query_id=self.query_chat.id)
                return DEFAULT_ORCHESTRATION_ERROR_MESSAGE

            send_orchestration_message(f"""
            ❇️ Orchestrator transactions have been successfully prepared for the current level of operations.
            """, query_id=self.query_chat.id)
            send_orchestration_message(f"""
            🚀 The Orchestrator is getting prepared for the next level of operations...
            """, query_id=self.query_chat.id)
            return self.execute_for_query(fs_urls=fs_urls, img_urls=img_urls)

        send_orchestration_message(f"""
        ❇️❇️ Orchestrator has accomplished the operation processes!
        """, query_id=self.query_chat.id)
        _ = OrchestrationQueryLog.objects.create(
            orchestration_query=self.query_chat,
            log_type=OrchestrationQueryLogTypesNames.MAESTRO_ANSWER,
            log_text_content=final_resp,
            log_file_contents=[],
            log_image_contents=[],
        )
        return final_resp

    @staticmethod
    async def listen_to_websocket(websocket_url):
        try:
            async with websockets.connect(websocket_url) as websocket:
                while True:
                    msg = await websocket.recv()
        except Exception as e:
            pass

    def ask_worker_assistant(self, assistant_id, maestro_query, file_urls=None, image_urls=None):
        send_orchestration_message(f"""
        🧑‍🚀 >> Worker Assistant began processing the order.
        """, query_id=self.query_chat.id)
        send_orchestration_message(f"""
        🧑‍🚀⚙️ >> Worker Assistant is preparing the instructions for the order.
        """, query_id=self.query_chat.id)

        structured_maestro_order = build_maestro_to_assistant_instructions_prompt(maestro_query_text=maestro_query)
        send_orchestration_message(f"""
        🧑‍🚀✅ >> Worker Assistant has successfully prepared the instructions for the order.
        """, query_id=self.query_chat.id)

        if assistant_id in self.worker_chats:
            send_orchestration_message(f"""
            🧑‍🚀🔍 >> Worker Assistant already has a chat object. Connecting to the chat object...
            """, query_id=self.query_chat.id)
            chat_id = self.worker_chats[assistant_id]
            chat = MultimodalChat.objects.get(id=chat_id)
            agent = Assistant.objects.get(id=assistant_id)
        else:
            send_orchestration_message(f"""
            🧑‍🚀🔧 >> Worker Assistant does not yet have a chat object. Creating a chat object for the assistant...
            """, query_id=self.query_chat.id)
            try:
                agent = Assistant.objects.get(id=assistant_id)
                new_chat_object = MultimodalChat.objects.create(
                    organization=self.maestro.organization, assistant=agent, user=self.query_chat.created_by_user,
                    chat_source=SourcesForMultimodalChatsNames.ORCHESTRATION, is_archived=False,
                    created_by_user_id=self.query_chat.created_by_user.id)
                self.worker_chats[assistant_id] = new_chat_object.id
                chat_id = self.worker_chats[assistant_id]
                chat = MultimodalChat.objects.get(id=chat_id)

                send_orchestration_message(f"""
                🧑‍🚀🔧✅ >> Worker Assistant chat object has been successfully created.
                """, query_id=self.query_chat.id)
            except Exception as e:
                logger.error(f"Error while creating the chat object for the Worker Assistant: {e}")
                send_orchestration_message(f"""
                🧑‍🚀🔧🚨 >> Error while creating the chat object for the Worker Assistant: {e}
                """, query_id=self.query_chat.id)
                return DEFAULT_WORKER_ASSISTANT_ERROR_MESSAGE

        try:
            internal_llm_client = OpenAIGPTClientManager(assistant=agent, chat_object=chat)
        except Exception as e:
            logger.error(f"Error while creating the internal LLM client for the Worker Assistant: {e}")
            send_orchestration_message(f"""
            🧑‍🚀🚨 Error while setting the connection and user: {e}
            """, query_id=self.query_chat.id)
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

        MultimodalChatMessage.objects.create(
            multimodal_chat=chat, sender_type='USER', message_text_content=structured_maestro_order,
            message_image_contents=image_urls, message_file_contents=file_urls)
        final_resp = internal_llm_client.respond_stream(
            latest_message=structured_maestro_order, image_uris=image_urls, file_uris=file_urls)
        MultimodalChatMessage.objects.create(
            multimodal_chat=chat, sender_type='ASSISTANT', message_text_content=final_resp)
        logger.info(f"Worker Assistant response is ready.")
        return final_resp
