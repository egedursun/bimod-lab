#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: orchestration_executor.py
#  Last Modified: 2024-09-28 22:17:13
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:35
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: orchestration_executor.py
#  Last Modified: 2024-09-28 20:38:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:09:26
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

import websockets

from apps._services.llms.openai import InternalOpenAIClient
from apps._services.llms.utils import find_json_presence, ChatRoles
from apps._services.orchestration.orchestration_tool_manager import OrchestrationToolManager
from apps._services.orchestration.prompts.calls.build_maestro_to_assistant_instructions import \
    build_maestro_to_assistant_instructions_prompt
from apps._services.orchestration.prompts.orchestration_history_builder import OrchestrationHistoryBuilder
from apps._services.orchestration.prompts.orchestration_prompt_builder import OrchestrationPromptBuilder
from apps._services.orchestration.utils import send_orchestration_message, embed_orchestration_tool_call_in_prompt, \
    DEFAULT_ORCHESTRATION_ERROR_MESSAGE, DEFAULT_WORKER_ASSISTANT_ERROR_MESSAGE, \
    get_orchestration_json_decode_error_log
from apps.assistants.models import Assistant
from apps.multimodal_chat.models import MultimodalChat, MultimodalChatMessage
from apps.multimodal_chat.utils import BIMOD_NO_TAG_PLACEHOLDER, BIMOD_STREAMING_END_TAG, BIMOD_PROCESS_END, \
    ChatSourcesNames
from apps.orchestrations.models import OrchestrationQuery, OrchestrationQueryLog
from apps.orchestrations.utils import OrchestrationQueryLogTypesNames


class OrchestrationExecutor:

    def __init__(self, maestro, query_chat):
        self.maestro = maestro
        self.query_chat = query_chat
        ############################################################################################################
        self.client = InternalOpenAIClient.get_no_scope_connection(llm_model=self.maestro.llm_model)
        ############################################################################################################
        self.worker_chats = {
            ############################################
            # This dictionary is to be filled with IDs of the Worker Assistants' chats as they get created.
            #       `worker_assistant_id: chat_id`,
            #       `worker_assistant_id: chat_id`,
            #        ...
            # ...
            ############################################
        }

    def execute_for_query(self, file_urls=None, image_urls=None):

        send_orchestration_message(f"""
        🤖 Orchestrator has started processing the query.
        """, query_id=self.query_chat.id)

        query_chat = self.query_chat

        try:
            c = self.client
            user = self.query_chat.created_by_user
        except Exception as e:
            print(f"[OrchestrationExecutor.execute_for_query] Error while setting the connection and user: {e}")

            send_orchestration_message(f"""
            🚨 Error while setting the connection and user: {e}
            """, query_id=self.query_chat.id)
            return DEFAULT_ORCHESTRATION_ERROR_MESSAGE

        send_orchestration_message(f"""
        📡 Connection and user are successfully set.
        """, query_id=self.query_chat.id)

        try:
            # Create the system prompt for the Orchestrator
            prompt_messages = [OrchestrationPromptBuilder.build(
                query_chat=self.query_chat,
                maestro=self.maestro,
                user=user,
                role=ChatRoles.SYSTEM)]
        except Exception as e:
            print(f"[OrchestrationExecutor.execute_for_query] Error while creating the system prompt: {e}")

            send_orchestration_message(f"""
            🚨 Error while creating the system prompt for the orchestration process: {e}
            """, query_id=self.query_chat.id)

            return DEFAULT_ORCHESTRATION_ERROR_MESSAGE

        send_orchestration_message(f"""
        📝 System prompt is successfully created.
        """, query_id=self.query_chat.id)

        try:
            # Create the history prompt for the Orchestrator
            prompt_messages.extend(OrchestrationHistoryBuilder.build(query_chat=query_chat))
        except Exception as e:
            print(f"[OrchestrationExecutor.execute_for_query] Error while creating the history prompt: {e}")

            send_orchestration_message(f"""
            🚨 Error while creating the history prompt for the orchestration process: {e}
            """, query_id=self.query_chat.id)

            return DEFAULT_ORCHESTRATION_ERROR_MESSAGE

        send_orchestration_message(f"""
        📝 History prompt is successfully created.
        """, query_id=self.query_chat.id)

        ############################################################################################################
        ############################################################################################################
        # Generate the response of the Orchestrator via OpenAI Client
        ############################################################################################################

        send_orchestration_message(f"""
        📡 Generating response in cooperation with the orchestrator...
        """, query_id=self.query_chat.id)

        try:
            response_chunks = c.chat.completions.create(
                model=self.maestro.llm_model.model_name,
                messages=prompt_messages,
                temperature=float(self.maestro.llm_model.temperature),
                frequency_penalty=float(self.maestro.llm_model.frequency_penalty),
                presence_penalty=float(self.maestro.llm_model.presence_penalty),
                max_tokens=int(self.maestro.llm_model.maximum_tokens),
                top_p=float(self.maestro.llm_model.top_p),
                stream=True
            )
            print(f"[InternalOpenAIClient.respond_stream] Retrieved the response from the LLM.")
        except Exception as e:
            print(
                f"[InternalOpenAIClient.respond_stream] Error occurred while retrieving the response from the LLM: {str(e)}")

            send_orchestration_message(f"""
            🚨 Error occurred while generating the response in cooperation with the orchestrator: {str(e)}
            """, query_id=self.query_chat.id)

            return DEFAULT_ORCHESTRATION_ERROR_MESSAGE

        ############################################################################################################
        ############################################################################################################

        send_orchestration_message(f"""
        🧨 Response streamer is ready to process the response.
        """, query_id=self.query_chat.id)

        # Accumulate and stream the response of the Orchestrator
        try:
            send_orchestration_message(f"""
        ⚓ Orchestration Response generation is in progress...
                            """, query_id=self.query_chat.id)

            # Accumulate the orchestration response for backend processing
            accumulated_response = ""
            for element in response_chunks:
                ############################
                choices = element.choices
                first_choice = choices[0]
                delta = first_choice.delta
                content = delta.content
                ############################
                if content is not None:
                    accumulated_response += content
                    send_orchestration_message(f"""{content}""", stop_tag=BIMOD_NO_TAG_PLACEHOLDER,
                                               query_id=self.query_chat.id)
            send_orchestration_message(f"""""", stop_tag=BIMOD_STREAMING_END_TAG, query_id=self.query_chat.id)

            send_orchestration_message(f"""
        🔌 Orchestration generation iterations has been successfully accomplished.
                            """, query_id=self.query_chat.id)

            send_orchestration_message(f"""
        📦 Orchestrator is preparing the response...
                            """, query_id=self.query_chat.id)

            print(f"[OrchestrationExecutor.execute_for_query] Processed the response from the LLM.")
            print(
                f"[OrchestrationExecutor.execute_for_query] Accumulated the Orchestrator response: {accumulated_response}")
        except Exception as e:
            print(
                f"[OrchestrationExecutor.execute_for_query] Error occurred while processing the response from the LLM: {str(e)}")

            send_orchestration_message(f"""
        🚨 A critical error occurred while processing the Orchestration response from the language model.
            """, stop_tag=BIMOD_PROCESS_END, query_id=self.query_chat.id)

            return DEFAULT_ORCHESTRATION_ERROR_MESSAGE

        send_orchestration_message(f"""
        🕹️ Raw Orchestration response stream has been successfully delivered.
        """, query_id=self.query_chat.id)

        final_response = accumulated_response
        print(f"[OrchestrationExecutor.execute_for_query] Final response: {final_response}")

        send_orchestration_message(f"""
        🧲 Transactional information has been successfully processed.
        """, query_id=self.query_chat.id)

        # Check for 'Worker Calls':
        tool_name, assistant_id = None, None
        tool_response, json_part = None, None
        # If Worker Calls are present;
        if find_json_presence(final_response):
            send_orchestration_message(f"""
        🛠️ Worker assistant call detected in the response. Processing with the worker execution steps...
            """, query_id=self.query_chat.id)

            # Identify the Worker Call
            send_orchestration_message(f"""
        🧰 Identifying the valid worker assistant calls...
            """, query_id=self.query_chat.id)

            json_part = find_json_presence(final_response)[0]  # for now only a single JSON at a time

            send_orchestration_message(f"""
        💡️ Worker assistant usage call has been identified.
            """, query_id=self.query_chat.id)

            send_orchestration_message(f"""
        🧮 Executing the worker assistant call...
            """, query_id=self.query_chat.id)

            try:
                tool_executor = OrchestrationToolManager(
                    maestro=self.maestro,
                    query_chat=self.query_chat,
                    tool_usage_json_str=json_part
                )

                tool_response, tool_name, assistant_id, file_urls, image_urls = tool_executor.use_tool()

                assistant = Assistant.objects.get(id=assistant_id)

                send_orchestration_message(f"""
            🧰 Worker Assistant call to: {assistant.name} has been successfully delivered.
                """, query_id=self.query_chat.id)

                send_orchestration_message(f"""
            📦 Worker Assistant Response from: '{assistant.name}' is being delivered to the Orchestrator for further actions...
                """, query_id=self.query_chat.id)

                print(
                    f"[OrchestrationExecutor.execute_for_query] Response from the assistant worker is received: {tool_response}")

                send_orchestration_message(f"""
            🎯 Tool response from: '{assistant.name}' has been successfully delivered to the Orchestrator.
                """, query_id=self.query_chat.id)

            except Exception as e:
                send_orchestration_message(f"""
            🚨 Error occurred while calling the worker assistant. Attempting to recover...
                """, query_id=self.query_chat.id)

                if tool_name is not None:
                    tool_response = f"""
                         ---
                         There has been an error while executing the tool: {tool_name}
                         Insights:
                            - Tool Name field is not None, unlikely to be related to the lack of tool in the system.
                         Error Log: {get_orchestration_json_decode_error_log(error_logs=str(e))}
                         ---
                    """
                    print(f"[OrchestrationExecutor.execute_for_query] Error occurred while calling the "
                          f"worker assistant: {e}")
                else:
                    tool_response = f"""
                        ---
                        There has been an error while executing the tool.
                        Insights:
                            - Tool Name field is None, likely to be related to the lack of tool in the system.
                        Error Log: {get_orchestration_json_decode_error_log(error_logs=str(e))}
                        ---
                    """
                    print(f"[InternalOpenAIClient.respond_stream] Error occurred while executing the tool: {str(e)}")

                send_orchestration_message(f"""
            🚨 Error logs have been delivered to the assistant. Proceeding with the next actions...
               """, query_id=self.query_chat.id)

        send_orchestration_message(f"""
                    🧠 The Orchestrator is inspecting the responses of the worker assistants...
        """, query_id=self.query_chat.id)

        if tool_response is not None:

            send_orchestration_message(f"""
            📦 Orchestration records for the worker tool calls are being prepared...
            """, query_id=self.query_chat.id)

            try:
                self.query_chat: OrchestrationQuery
                tool_request = OrchestrationQueryLog.objects.create(
                    orchestration_query=self.query_chat,
                    log_type=OrchestrationQueryLogTypesNames.WORKER_REQUEST,
                    log_text_content=embed_orchestration_tool_call_in_prompt(json_part=json_part),
                    log_file_contents=[],
                    log_image_contents=[],
                    context_worker=Assistant.objects.get(id=assistant_id)
                )
                self.query_chat.logs.add(tool_request)
                self.query_chat.save()
                print(f"[OrchestrationExecutor.execute_for_query] Worker Assistant call records have been prepared.")

                # Stream the tool request to the UI
                send_orchestration_message(f"""
            ⚙️ Worker Assistant call records have been prepared. Proceeding with the next actions...
                """, query_id=self.query_chat.id)

            except Exception as e:
                print(
                    f"[OrchestrationExecutor.execute_for_query] Error while saving the Worker Assistant call record: {e}")

                send_orchestration_message(f"""
            🚨 A critical error occurred while recording the tool request. Cancelling the process.
                """, stop_tag=BIMOD_PROCESS_END, query_id=self.query_chat.id)

                return DEFAULT_ORCHESTRATION_ERROR_MESSAGE

            try:

                send_orchestration_message(f"""
            📦 Orchestration communication records for the Worker Assistant responses are being prepared...
                                """, query_id=self.query_chat.id)

                tool_message = OrchestrationQueryLog.objects.create(
                    orchestration_query=self.query_chat,
                    log_type=OrchestrationQueryLogTypesNames.WORKER_RESPONSE,
                    log_text_content=str(tool_response),
                    log_file_contents=file_urls,
                    log_image_contents=image_urls,
                    context_worker=Assistant.objects.get(id=assistant_id)
                )
                self.query_chat.logs.add(tool_message)
                self.query_chat.save()
                print(
                    f"[OrchestrationExecutor.execute_for_query] Worker Assistant response records have been prepared.")

                # Stream the tool response to the UI
                send_orchestration_message(f"""
             ⚙️ Worker Assistant response records have been prepared. Proceeding with the next actions...
                """, query_id=self.query_chat.id)

            except Exception as e:
                print(f"[OrchestrationExecutor.execute_for_query] Error while saving the Worker "
                      f"Assistant response record: {e}")

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

            # apply the recursive call to the self function to get another reply from the assistant
            print(f"[OrchestrationExecutor.execute_for_query] Recursive call to the execute_for_query function.")
            print(f"[IOrchestrationExecutor.execute_for_query] Worker Assistant Tool message: {tool_message}")

            return self.execute_for_query(
                file_urls=file_urls,
                image_urls=image_urls
            )

        send_orchestration_message(f"""
        ❇️❇️ Orchestrator has accomplished the operation processes!
        """, query_id=self.query_chat.id)

        # save the final response to the chat
        _ = OrchestrationQueryLog.objects.create(
            orchestration_query=self.query_chat,
            log_type=OrchestrationQueryLogTypesNames.MAESTRO_ANSWER,
            log_text_content=final_response,
            log_file_contents=[],
            log_image_contents=[],
        )

        print(f"[OrchestrationExecutor.execute_for_query] Returning the final response to the user: {final_response}")
        return final_response

    @staticmethod
    async def listen_to_websocket(websocket_url):
        try:
            async with websockets.connect(websocket_url) as websocket:
                while True:
                    message = await websocket.recv()
                    # send_orchestration_message(f"🧑‍🚀📡 >> Update @ Worker Assistant: {message}")
                    print(f"[OrchestrationExecutor.listen_to_websocket] Update @ Worker Assistant: {message}")
        except Exception as e:
            print(f"[OrchestrationExecutor.listen_to_websocket] Error while listening to the websocket: {e}")
            pass

    def ask_worker_assistant(self, assistant_id, maestro_query, file_urls=None, image_urls=None):

        send_orchestration_message(f"""
        🧑‍🚀 >> Worker Assistant began processing the order.
        """, query_id=self.query_chat.id)

        send_orchestration_message(f"""
        🧑‍🚀⚙️ >> Worker Assistant is preparing the instructions for the order.
        """, query_id=self.query_chat.id)

        # i. Build the 'instructions' and include 'maestro_query' in it
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
            assistant = Assistant.objects.get(id=assistant_id)
        else:
            send_orchestration_message(f"""
        🧑‍🚀🔧 >> Worker Assistant does not yet have a chat object. Creating a chat object for the assistant...
            """, query_id=self.query_chat.id)

            try:
                assistant = Assistant.objects.get(id=assistant_id)
                new_chat_object = MultimodalChat.objects.create(
                    organization=self.maestro.organization,
                    assistant=assistant,
                    user=self.query_chat.created_by_user,
                    chat_source=ChatSourcesNames.ORCHESTRATION,
                    is_archived=False,
                    created_by_user_id=self.query_chat.created_by_user.id,
                )
                self.worker_chats[assistant_id] = new_chat_object.id
                chat_id = self.worker_chats[assistant_id]
                chat = MultimodalChat.objects.get(id=chat_id)

                send_orchestration_message(f"""
            🧑‍🚀🔧✅ >> Worker Assistant chat object has been successfully created.
                """, query_id=self.query_chat.id)
            except Exception as e:
                print(f"[OrchestrationsExecutor.ask_worker_assistant] Error while creating the chat object: {e}")

                send_orchestration_message(f"""
            🧑‍🚀🔧🚨 >> Error while creating the chat object for the Worker Assistant: {e}
                """, query_id=self.query_chat.id)

                return DEFAULT_WORKER_ASSISTANT_ERROR_MESSAGE

        try:
            internal_llm_client = InternalOpenAIClient(
                assistant=assistant,
                multimodal_chat=chat,
            )
        except Exception as e:
            print(f"[OrchestrationExecutor.ask_worker_assistant] Error while setting the LLM connection: {e}")

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
            message_image_contents=image_urls, message_file_contents=file_urls
        )
        final_response = internal_llm_client.respond_stream(
            latest_message=structured_maestro_order,
            image_uris=image_urls,
            file_uris=file_urls
        )
        MultimodalChatMessage.objects.create(
            multimodal_chat=chat, sender_type='ASSISTANT', message_text_content=final_response
        )

        # v. Stream the responses of the assistant as they come

        # listen to the stream from the web socket, not implemented yet
        """
        protocol = "ws" if "http" in BASE_URL else "wss"
        websocket_url = f"{protocol}://{BASE_URL}/ws/logs/"
        asyncio.run(self.listen_to_websocket(websocket_url))
        """

        # vi. Return the final response of the assistant as text
        return final_response
