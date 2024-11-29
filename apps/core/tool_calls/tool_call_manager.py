#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: tool_call_manager.py
#  Last Modified: 2024-10-05 02:31:01
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

from django.contrib.auth.models import User

from apps.core.browsers.utils import BrowserActionsNames
from apps.core.generative_ai.auxiliary_methods.errors.error_log_prompts import get_json_decode_error_log
from apps.core.tool_calls.core_services.core_service_dashboard_statistics_query import run_query_dashboard_statistics
from apps.core.tool_calls.core_services.core_service_execute_metakanban_query import run_query_execute_metakanban
from apps.core.tool_calls.core_services.core_service_execute_metatempo_query import run_query_execute_metatempo
from apps.core.tool_calls.core_services.core_service_execute_orchestration_trigger import \
    run_query_trigger_orchestration
from apps.core.tool_calls.core_services.core_service_execute_scheduled_job_logs_query import \
    run_query_execute_scheduled_job_logs
from apps.core.tool_calls.core_services.core_service_execute_smart_contract_query import \
    run_query_execute_smart_contract_generation_query
from apps.core.tool_calls.core_services.core_service_execute_triggered_job_logs_query import \
    run_query_execute_triggered_job_logs
from apps.core.tool_calls.core_services.core_service_hadron_node_query import run_query_execute_hadron_node
from apps.core.tool_calls.core_services.core_service_process_reasoning import run_process_reasoning
from apps.core.tool_calls.core_services.core_service_generate_video import run_generate_video
from apps.core.tool_calls.input_verifiers.verify_dashboard_statistics_query import \
    verify_dashboard_statistics_query_content
from apps.core.tool_calls.input_verifiers.verify_hadron_node_query import verify_hadron_node_query_content
from apps.core.tool_calls.input_verifiers.verify_metakanban_query import verify_metakanban_query_content
from apps.core.tool_calls.input_verifiers.verify_metatempo_query import verify_metatempo_query_content
from apps.core.tool_calls.input_verifiers.verify_orchestration_trigger import verify_orchestration_trigger_content
from apps.core.tool_calls.input_verifiers.verify_scheduled_job_logs_query import \
    verify_scheduled_job_logs_query_content
from apps.core.tool_calls.input_verifiers.verify_smart_contract_query import \
    verify_smart_contract_generation_query_content
from apps.core.tool_calls.input_verifiers.verify_triggered_job_logs_query import \
    verify_triggered_job_logs_query_content
from apps.core.tool_calls.leanmod.core_services.core_service_consultation_semantor import \
    execute_semantor_consultation_query
from apps.core.tool_calls.leanmod.core_services.core_service_leanmod_memory_query import run_query_leanmod_memory
from apps.core.tool_calls.leanmod.core_services.core_service_query_semantor import execute_semantor_search_query
from apps.core.tool_calls.leanmod.input_verifiers.verify_query_leanmod_memory import \
    verify_leanmod_memory_query_content
from apps.core.tool_calls.leanmod.input_verifiers.verify_semantor_consultation_query import \
    verify_semantor_consultation_query_content
from apps.core.tool_calls.leanmod.input_verifiers.verify_semantor_query import verify_semantor_search_query_content
from apps.core.tool_calls.input_verifiers.verify_analyze_code import verify_analyze_code_content
from apps.core.tool_calls.input_verifiers.verify_audio_processing_query import verify_audio_processing_query
from apps.core.tool_calls.input_verifiers.verify_browser_query import verify_browser_query_content
from apps.core.tool_calls.input_verifiers.verify_dream_image import verify_dream_image_content
from apps.core.tool_calls.input_verifiers.verify_edit_image import verify_edit_image_content
from apps.core.tool_calls.input_verifiers.verify_generate_image import verify_generate_image_content
from apps.core.tool_calls.input_verifiers.verify_generate_video import verify_generate_video_content
from apps.core.tool_calls.input_verifiers.verify_http_retrieval_query import verify_http_retrieval_query_content
from apps.core.tool_calls.input_verifiers.verify_infer_ml_query import verify_infer_ml_query_content
from apps.core.tool_calls.input_verifiers.verify_main_query_or_run_call import verify_main_call_or_query_content
from apps.core.tool_calls.input_verifiers.verify_media_manager_query import verify_media_manager_query_content
from apps.core.tool_calls.input_verifiers.verify_process_reasoning_query import verify_process_reasoning_query_content
from apps.core.tool_calls.input_verifiers.verify_query_code_base import verify_code_base_query_content
from apps.core.tool_calls.input_verifiers.verify_query_intra_memory import verify_intra_memory_query_content
from apps.core.tool_calls.input_verifiers.verify_run_custom_api import verify_run_custom_api_content
from apps.core.tool_calls.input_verifiers.verify_run_custom_function import verify_run_custom_function_content
from apps.core.tool_calls.input_verifiers.verify_run_custom_script import verify_run_custom_script_content
from apps.core.tool_calls.input_verifiers.verify_run_nosql_query import verify_run_nosql_query_content
from apps.core.tool_calls.input_verifiers.verify_run_sql_query import verify_run_sql_query_content
from apps.core.tool_calls.input_verifiers.verify_ssh_system_command import verify_ssh_system_command_content
from apps.core.tool_calls.input_verifiers.verify_vector_store_query import verify_vector_store_query_content
from apps.core.tool_calls.leanmod.input_verifiers.verify_expert_network_query import \
    verify_expert_network_query_content
from apps.core.tool_calls.utils import ToolCallDescriptorNames, \
    get_no_tool_found_error_log, IMAGE_GENERATION_AFFIRMATION_PROMPT
from apps.core.tool_calls.core_services.core_service_process_audio import \
    run_process_audio
from apps.core.tool_calls.core_services.core_service_execute_browser import run_execute_browsing
from apps.core.tool_calls.core_services.core_service_code_base_query import run_query_code_base
from apps.core.tool_calls.core_services.core_service_analyze_code import run_analyze_code
from apps.core.tool_calls.core_services.core_service_execute_custom_api import run_execute_custom_api
from apps.core.tool_calls.core_services.core_service_execute_custom_function import run_execute_custom_code
from apps.core.tool_calls.core_services.core_service_execute_custom_script import run_execute_custom_script
from apps.core.tool_calls.core_services.core_service_execute_ssh_system_command import run_execute_ssh_system_commands
from apps.core.tool_calls.core_services.core_service_generate_image import run_generate_image
from apps.core.tool_calls.core_services.core_service_edit_image import run_edit_image
from apps.core.tool_calls.core_services.core_service_dream_image import run_dream_image
from apps.core.tool_calls.core_services.core_service_vector_store_query import run_query_vector_store
from apps.core.tool_calls.core_services.core_service_intra_memory_query import run_query_intra_memory
from apps.core.tool_calls.core_services.core_service_infer_with_ml import run_predict_with_ml
from apps.core.tool_calls.core_services.core_service_sql_query import run_sql_query
from apps.core.tool_calls.core_services.core_service_nosql_query import run_nosql_query
from apps.core.tool_calls.core_services.core_service_http_retrieval import run_http_retrieval
from apps.core.tool_calls.leanmod.core_services.core_service_query_expert_network import \
    execute_expert_network_query
from apps.assistants.models import Assistant
from apps.core.tool_calls.voidforger.core_services import execute_voidforger_old_message_search_query, \
    execute_voidforger_action_history_log_search_query, execute_voidforger_auto_execution_log_search_query, \
    execute_voidforger_leanmod_oracle_search_query, execute_voidforger_leanmod_oracle_command_order
from apps.core.tool_calls.voidforger.input_verifiers import verify_voidforger_old_message_search_query_content, \
    verify_voidforger_action_history_log_search_query_content, \
    verify_voidforger_auto_execution_log_search_query_content, verify_voidforger_leanmod_oracle_search_query_content, \
    verify_voidforger_leanmod_oracle_command_order_content
from apps.multimodal_chat.models import MultimodalChat
from apps.multimodal_chat.utils import transmit_websocket_log
from apps.video_generations.models import GeneratedVideo, VideoGeneratorConnection
from apps.voidforger.models import VoidForgerActionMemoryLog
from apps.voidforger.utils import VoidForgerActionTypesNames
from config.settings import MEDIA_URL

logger = logging.getLogger(__name__)


class ToolCallManager:

    def __init__(
        self,
        assistant: Assistant,
        chat: MultimodalChat,
        tool_usage_json_str: dict,
        user: User = None
    ):

        self.user = user
        self.assistant = assistant
        self.chat = chat
        self.tool_usage_dict_stringified = tool_usage_json_str
        self.tool_usage_dict = {}

    def call_internal_tool_service(self):

        try:
            if isinstance(self.tool_usage_dict_stringified, dict):
                logger.info("Tool usage dictionary is already a dictionary.")
                self.tool_usage_dict = self.tool_usage_dict_stringified

            else:
                logger.info("Tool usage dictionary is a string. Converting it to a dictionary.")
                self.tool_usage_dict = json.loads(self.tool_usage_dict_stringified)

        except Exception as e:
            logger.error(f"Error occurred while converting the tool usage dictionary to a dictionary: {e}")
            return get_json_decode_error_log(
                error_logs=str(e)
            ), None, None, None

        f_uris, img_uris = [], []

        error = verify_main_call_or_query_content(
            content=self.tool_usage_dict
        )
        if error:
            logger.error(f"Error occurred while verifying the main call or query content: {error}")
            return error, None, None, None

        defined_tool_descriptor = self.tool_usage_dict.get("tool")
        output_tool_call = f"""
            Tool Response: {defined_tool_descriptor}

            '''
        """

        if defined_tool_descriptor == ToolCallDescriptorNames.EXECUTE_SQL_QUERY:
            error = verify_run_sql_query_content(
                content=self.tool_usage_dict
            )

            if error:
                logger.error(f"Error occurred while verifying the SQL query content: {error}")
                return error, None, None, None

            output_tool_call = self._handle_tool_sql_query(output_tool_call)

        elif defined_tool_descriptor == ToolCallDescriptorNames.EXECUTE_NOSQL_QUERY:
            error = verify_run_nosql_query_content(
                content=self.tool_usage_dict
            )

            if error:
                logger.error(f"Error occurred while verifying the NoSQL query content: {error}")
                return error, None, None, None

            output_tool_call = self._handle_tool_nosql_query(output_tool_call)

        elif defined_tool_descriptor == ToolCallDescriptorNames.EXECUTE_VECTOR_STORE_QUERY:
            error = verify_vector_store_query_content(
                content=self.tool_usage_dict
            )

            if error:
                logger.error(f"Error occurred while verifying the vector store query content: {error}")
                return error, None, None, None

            output_tool_call = self._handle_tool_vector_base_query(output_tool_call)

        elif defined_tool_descriptor == ToolCallDescriptorNames.EXECUTE_CODE_BASE_QUERY:
            error = verify_code_base_query_content(
                content=self.tool_usage_dict
            )

            if error:
                logger.error(f"Error occurred while verifying the code base query content: {error}")
                return error, None, None, None

            output_tool_call = self._handle_tool_code_base_query(output_tool_call)

        elif defined_tool_descriptor == ToolCallDescriptorNames.EXECUTE_INTRA_MEMORY_QUERY:
            error = verify_intra_memory_query_content(
                content=self.tool_usage_dict
            )

            if error:
                logger.error(f"Error occurred while verifying the intra memory query content: {error}")
                return error, None, None, None

            output_tool_call = self._handle_tool_intra_memory_query(output_tool_call)

        elif defined_tool_descriptor == ToolCallDescriptorNames.EXECUTE_SSH_SYSTEM_QUERY:
            error = verify_ssh_system_command_content(
                content=self.tool_usage_dict
            )

            if error:
                logger.error(f"Error occurred while verifying the SSH system command content: {error}")
                return error, None, None, None

            output_tool_call = self._handle_tool_ssh_system(output_tool_call)

        elif defined_tool_descriptor == ToolCallDescriptorNames.EXECUTE_MEDIA_MANAGER_QUERY:
            error = verify_media_manager_query_content(content=self.tool_usage_dict)

            if error:
                logger.error(f"Error occurred while verifying the media manager query content: {error}")
                return error, None, None, None

            f_uris, img_uris, output_tool_call = self._handle_tool_media_manager_query(f_uris, img_uris,
                                                                                       output_tool_call)

        elif defined_tool_descriptor == ToolCallDescriptorNames.EXECUTE_HTTP_RETRIEVAL:
            error = verify_http_retrieval_query_content(
                content=self.tool_usage_dict
            )

            if error:
                logger.error(f"Error occurred while verifying the HTTP retrieval query content: {error}")
                return error, None, None, None

            output_tool_call = self._handle_tool_http_client_retrieval(output_tool_call)

        elif defined_tool_descriptor == ToolCallDescriptorNames.EXECUTE_INFER_WITH_ML:

            error = verify_infer_ml_query_content(
                content=self.tool_usage_dict
            )
            if error:
                logger.error(f"Error occurred while verifying the infer with ML query content: {error}")
                return error, None, None, None

            output_tool_call = self._handle_tool_infer_with_ml(output_tool_call)

        elif defined_tool_descriptor == ToolCallDescriptorNames.EXECUTE_ANALYZE_CODE:

            error = verify_analyze_code_content(
                content=self.tool_usage_dict
            )
            if error:
                logger.error(f"Error occurred while verifying the analyze code content: {error}")
                return error, None, None, None

            f_uris, img_uris, output_tool_call = self._handle_tool_analyze_code(f_uris, img_uris, output_tool_call)

        elif defined_tool_descriptor == ToolCallDescriptorNames.EXECUTE_REASONING_PROCESS:

            error = verify_process_reasoning_query_content(
                content=self.tool_usage_dict
            )
            if error:
                logger.error(f"Error occurred while verifying the reasoning process content: {error}")
                return error, None, None, None

            output_tool_call = self._handle_tool_reasoning(output_tool_call)

        elif defined_tool_descriptor == ToolCallDescriptorNames.EXECUTE_CUSTOM_FUNCTION:

            error = verify_run_custom_function_content(
                content=self.tool_usage_dict
            )
            if error:
                logger.error(f"Error occurred while verifying the custom function content: {error}")
                return error, None, None, None

            output_tool_call = self._handle_tool_execute_function(output_tool_call)

        elif defined_tool_descriptor == ToolCallDescriptorNames.EXECUTE_CUSTOM_API:

            error = verify_run_custom_api_content(
                content=self.tool_usage_dict
            )
            if error:
                logger.error(f"Error occurred while verifying the custom API content: {error}")
                return error, None, None, None

            output_tool_call = self._handle_tool_execute_api(output_tool_call)

        elif defined_tool_descriptor == ToolCallDescriptorNames.EXECUTE_CUSTOM_SCRIPT:

            error = verify_run_custom_script_content(
                content=self.tool_usage_dict
            )
            if error:
                logger.error(f"Error occurred while verifying the custom script content: {error}")
                return error, None, None, None

            output_tool_call = self._handle_tool_execute_script(output_tool_call)

        elif defined_tool_descriptor == ToolCallDescriptorNames.EXECUTE_GENERATE_IMAGE:

            error = verify_generate_image_content(
                content=self.tool_usage_dict
            )
            if error:
                logger.error(f"Error occurred while verifying the generate image content: {error}")
                return error, None, None, None

            output_tool_call = self._handle_tool_generate_image(img_uris, output_tool_call)

        elif defined_tool_descriptor == ToolCallDescriptorNames.EXECUTE_EDIT_IMAGE:

            error = verify_edit_image_content(
                content=self.tool_usage_dict
            )
            if error:
                logger.error(f"Error occurred while verifying the edit image content: {error}")
                return error, None, None, None

            output_tool_call = self._handle_tool_edit_image(img_uris, output_tool_call)

        elif defined_tool_descriptor == ToolCallDescriptorNames.EXECUTE_DREAM_IMAGE:

            error = verify_dream_image_content(
                content=self.tool_usage_dict
            )
            if error:
                logger.error(f"Error occurred while verifying the dream image content: {error}")
                return error, None, None, None

            output_tool_call = self._handle_tool_dream_image(img_uris, output_tool_call)

        elif defined_tool_descriptor == ToolCallDescriptorNames.EXECUTE_BROWSING:

            error = verify_browser_query_content(
                content=self.tool_usage_dict
            )
            if error:
                logger.error(f"Error occurred while verifying the browsing content: {error}")
                return error, None, None, None

            output_tool_call = self._handle_tool_execute_browsing(output_tool_call)

        elif defined_tool_descriptor == ToolCallDescriptorNames.EXECUTE_PROCESS_AUDIO:

            error = verify_audio_processing_query(
                content=self.tool_usage_dict
            )
            if error:
                logger.error(f"Error occurred while verifying the audio processing content: {error}")
                return error, None, None, None

            output_tool_call = self._handle_tool_execute_audio(output_tool_call)

        elif defined_tool_descriptor == ToolCallDescriptorNames.EXECUTE_GENERATE_VIDEO:

            error = verify_generate_video_content(
                content=self.tool_usage_dict
            )
            if error:
                logger.error(f"Error occurred while verifying the generate video content: {error}")
                return error, None, None, None

            c_id, video_generation_response = self._handle_execute_video()

            if video_generation_response.get("error") is not None:
                logger.error(f"Error occurred while generating the video: {video_generation_response.get('error')}")
                return video_generation_response.get("error"), None, None, None

            if video_generation_response.get("video_url") is None:
                logger.error("Video URL is NULL. A problem might have happened within the generation process.")
                return ("Video URL is NULL. A problem might have happened within the "
                        "generation process."), None, None, None

            video_url = video_generation_response.get("video_url")
            video_generator_connection = VideoGeneratorConnection.objects.get(id=c_id)

            GeneratedVideo.objects.create(
                organization=video_generator_connection.assistant.organization,
                assistant=self.assistant,
                multimodal_chat=self.chat,
                created_by_user=self.chat.created_by_user,
                video_url=video_url
            )

            video_generation_response_raw_str = json.dumps(
                video_generation_response,
                sort_keys=True,
                default=str
            )

            output_tool_call += video_generation_response_raw_str

        elif defined_tool_descriptor == ToolCallDescriptorNames.EXECUTE_DASHBOARD_STATISTICS_QUERY:
            error = verify_dashboard_statistics_query_content(
                content=self.tool_usage_dict
            )

            if error:
                logger.error(f"Error occurred while verifying the dashboard statistics query content: {error}")
                return error, None, None, None

            output_tool_call = self._handle_tool_dashboard_statistics_query(output_tool_call)

        elif defined_tool_descriptor == ToolCallDescriptorNames.EXECUTE_HADRON_PRIME_NODE_QUERY:
            error = verify_hadron_node_query_content(
                content=self.tool_usage_dict
            )

            if error:
                logger.error(f"Error occurred while verifying the Hadron Prime Node query content: {error}")
                return error, None, None, None

            output_tool_call = self._handle_tool_hadron_node_query(output_tool_call)

        elif defined_tool_descriptor == ToolCallDescriptorNames.EXECUTE_METAKANBAN_QUERY:
            error = verify_metakanban_query_content(
                content=self.tool_usage_dict
            )

            if error:
                logger.error(f"Error occurred while verifying the MetaKanban board query content: {error}")
                return error, None, None, None

            output_tool_call = self._handle_tool_metakanban_query(output_tool_call)

        elif defined_tool_descriptor == ToolCallDescriptorNames.EXECUTE_METATEMPO_QUERY:
            error = verify_metatempo_query_content(
                content=self.tool_usage_dict
            )

            if error:
                logger.error(f"Error occurred while verifying the MetaTempo tracker query content: {error}")
                return error, None, None, None

            output_tool_call = self._handle_tool_metatempo_query(output_tool_call)

        elif defined_tool_descriptor == ToolCallDescriptorNames.EXECUTE_ORCHESTRATION_TRIGGER:
            error = verify_orchestration_trigger_content(
                content=self.tool_usage_dict
            )

            if error:
                logger.error(f"Error occurred while verifying the Orchestration trigger content: {error}")
                return error, None, None, None

            output_tool_call = self._handle_tool_orchestration_trigger(output_tool_call)

        elif defined_tool_descriptor == ToolCallDescriptorNames.EXECUTE_SCHEDULED_JOB_LOGS_QUERY:
            error = verify_scheduled_job_logs_query_content(
                content=self.tool_usage_dict
            )

            if error:
                logger.error(f"Error occurred while verifying the scheduled job logs query content: {error}")
                return error, None, None, None

            output_tool_call = self._handle_tool_scheduled_job_logs_query(output_tool_call)

        elif defined_tool_descriptor == ToolCallDescriptorNames.EXECUTE_TRIGGERED_JOB_LOGS_QUERY:
            error = verify_triggered_job_logs_query_content(
                content=self.tool_usage_dict
            )

            if error:
                logger.error(f"Error occurred while verifying the triggered job logs query content: {error}")
                return error, None, None, None

            output_tool_call = self._handle_tool_triggered_job_logs_query(output_tool_call)

        elif defined_tool_descriptor == ToolCallDescriptorNames.EXECUTE_SMART_CONTRACT_GENERATION_QUERY:
            error = verify_smart_contract_generation_query_content(
                content=self.tool_usage_dict
            )

            if error:
                logger.error(
                    f"Error occurred while verifying the Smart Contract Generation query tool content: {error}")
                return error, None, None, None

            output_tool_call = self._handle_tool_smart_contract_gen_query(output_tool_call)

        ##################################################

        # NO TOOL FOUND

        else:
            logger.error(f"No tool found with the descriptor: {defined_tool_descriptor}")
            return get_no_tool_found_error_log(
                query_name=defined_tool_descriptor
            ), defined_tool_descriptor, f_uris, img_uris

        ##################################################

        output_tool_call += f"""
            '''
        """

        if f_uris:
            for i, uri in enumerate(f_uris):

                if not uri.startswith("http"):
                    uri = f"{MEDIA_URL}{uri}"
                f_uris[i] = uri

        if img_uris:
            for i, uri in enumerate(img_uris):

                if not uri.startswith("http"):
                    uri = f"{MEDIA_URL}{uri}"
                img_uris[i] = uri

        logger.info(f"Processed the files and images. Returning the output.")
        return output_tool_call, defined_tool_descriptor, f_uris, img_uris

    def _handle_execute_video(self):

        logger.info("Executing the video generation process.")

        c_id = self.tool_usage_dict.get("parameters").get("connection_id")
        action_type = self.tool_usage_dict.get("parameters").get("action_type")
        query = self.tool_usage_dict.get("parameters").get("query")

        aspect_ratio = self.tool_usage_dict.get("parameters").get(
            "aspect_ratio") if "aspect_ratio" in self.tool_usage_dict.get("parameters") else None

        start_frame_url = self.tool_usage_dict.get("parameters").get(
            "start_frame_url") if "start_frame_url" in self.tool_usage_dict.get("parameters") else None

        end_frame_url = self.tool_usage_dict.get("parameters").get(
            "end_frame_url") if "end_frame_url" in self.tool_usage_dict.get("parameters") else None

        output = run_generate_video(
            connection_id=c_id,
            video_generator_action_type=action_type,
            video_generator_query=query,
            aspect_ratio=aspect_ratio,
            start_frame_url=start_frame_url,
            end_frame_url=end_frame_url
        )

        logger.info(f"Video generation response retrieved.")
        return c_id, output

    def _handle_tool_execute_audio(self, output_tool_call):

        logger.info("Executing the audio processing process.")

        action = self.tool_usage_dict.get("parameters").get("action")
        audio_file_path = self.tool_usage_dict.get("parameters").get("audio_file_path")
        text_content = self.tool_usage_dict.get("parameters").get("text_content")
        voice_selection = self.tool_usage_dict.get("parameters").get("voice_selection")

        output = run_process_audio(
            agent_id=self.assistant.id,
            chat_id=self.chat.id,
            process_audio_action_type=action,
            audio_uri=audio_file_path,
            txt_data=text_content,
            llm_voice_type=voice_selection
        )

        output_str = json.dumps(
            output,
            sort_keys=True,
            default=str
        )

        output_tool_call += output_str
        logger.info(f"Audio processing response retrieved.")
        return output_tool_call

    def _handle_tool_execute_browsing(self, output_tool_call):

        logger.info("Executing the browsing process.")

        c_id = self.tool_usage_dict.get("parameters").get("browser_connection_id")
        action = self.tool_usage_dict.get("parameters").get("action")
        query, page, search_results, click_url = None, None, None, None

        if action == BrowserActionsNames.BROWSER_SEARCH:
            query = self.tool_usage_dict.get("parameters").get("query")
            page = self.tool_usage_dict.get("parameters").get("page")

        elif action == BrowserActionsNames.CLICK_URL_IN_SEARCH:
            search_results = self.tool_usage_dict.get("parameters").get("search_results")
            click_url = self.tool_usage_dict.get("parameters").get("click_url")

        output = run_execute_browsing(
            connection_id=c_id,
            browsing_action=action,
            browsing_query=query,
            page_definition=page,
            search_results=search_results,
            click_url=click_url
        )

        output_str = json.dumps(
            output,
            sort_keys=True,
            default=str
        )

        output_tool_call += output_str
        logger.info(f"Browsing response retrieved.")
        return output_tool_call

    def _handle_tool_dream_image(self, image_uris, output_tool_call):

        logger.info("Executing the dream image process.")

        image_uri = self.tool_usage_dict.get("parameters").get("image_uri")
        image_size = self.tool_usage_dict.get("parameters").get("image_size")

        image_variation_response = run_dream_image(
            agent_id=self.assistant.id,
            chat_id=self.chat.id,
            img_uri=image_uri,
            img_dimension=image_size
        )

        image_uri = image_variation_response.get("image_uri")
        image_uris.append(image_uri)

        output = json.dumps(
            image_variation_response,
            sort_keys=True,
            default=str
        )

        output_tool_call += output
        logger.info(f"Dream image response retrieved.")
        return output_tool_call

    def _handle_tool_edit_image(self, image_uris, output_tool_call):

        logger.info("Executing the edit image process.")

        prompt = self.tool_usage_dict.get("parameters").get("prompt")
        edit_image_uri = self.tool_usage_dict.get("parameters").get("edit_image_uri")
        edit_image_mask_uri = self.tool_usage_dict.get("parameters").get("edit_image_mask_uri")
        image_size = self.tool_usage_dict.get("parameters").get("image_size")

        image_modification_response = run_edit_image(
            agent_id=self.assistant.id,
            chat_id=self.chat.id,
            edit_prompt=prompt,
            edit_img_uri=edit_image_uri,
            edit_img_uri_mask=edit_image_mask_uri,
            img_dimensions=image_size
        )

        image_uri = image_modification_response.get("image_uri")
        image_uris.append(image_uri)

        output_str = json.dumps(
            image_modification_response,
            sort_keys=True,
            default=str
        )

        output_tool_call += output_str
        logger.info(f"Edit image response retrieved.")
        return output_tool_call

    def _handle_tool_generate_image(
        self,
        image_uris,
        output_tool_call
    ):

        logger.info("Executing the generate image process.")

        prompt = self.tool_usage_dict.get("parameters").get("prompt")
        size = self.tool_usage_dict.get("parameters").get("size")
        quality = self.tool_usage_dict.get("parameters").get("quality")

        image_generation_response = run_generate_image(
            agent_id=self.assistant.id,
            chat_id=self.chat.id,
            img_generation_prompt=prompt + IMAGE_GENERATION_AFFIRMATION_PROMPT,
            img_dimensions=size,
            img_resolution=quality
        )

        image_uri = image_generation_response.get("image_uri")
        image_uris.append(image_uri)

        output_str = json.dumps(
            image_generation_response,
            sort_keys=True,
            default=str
        )

        output_tool_call += output_str
        logger.info(f"Generate image response retrieved.")
        return output_tool_call

    def _handle_tool_execute_script(self, output_tool_call):

        logger.info("Executing the custom script process.")

        custom_script_reference_id = self.tool_usage_dict.get("parameters").get("custom_script_reference_id")

        output = run_execute_custom_script(
            ref_id=custom_script_reference_id
        )

        output_str = json.dumps(
            output,
            sort_keys=True,
            default=str
        )

        output_tool_call += output_str
        logger.info(f"Custom script response retrieved.")
        return output_tool_call

    def _handle_tool_execute_api(self, output_tool_call):

        logger.info("Executing the custom API process.")

        custom_api_reference_id = self.tool_usage_dict.get("parameters").get("custom_api_reference_id")
        endpoint_name = self.tool_usage_dict.get("parameters").get("endpoint_name")
        path_values = self.tool_usage_dict.get("parameters").get("path_values")
        query_values = self.tool_usage_dict.get("parameters").get("query_values")
        body_values = self.tool_usage_dict.get("parameters").get("body_values")

        output = run_execute_custom_api(
            ref_id=custom_api_reference_id,
            api_endpoint_str=endpoint_name,
            header_path_vals=path_values,
            header_query_vals=query_values,
            header_body_vals=body_values
        )

        output_str = json.dumps(
            output,
            sort_keys=True,
            default=str
        )

        output_tool_call += output_str
        logger.info(f"Custom API response retrieved.")
        return output_tool_call

    def _handle_tool_execute_function(self, output_tool_call):

        logger.info("Executing the custom function process.")
        custom_function_reference_id = self.tool_usage_dict.get("parameters").get("custom_function_reference_id")
        input_data = self.tool_usage_dict.get("parameters").get("input_data")

        output = run_execute_custom_code(
            ref_id=custom_function_reference_id,
            function_input_values=input_data
        )

        output_str = json.dumps(
            output,
            sort_keys=True,
            default=str
        )

        output_tool_call += output_str
        logger.info(f"Custom function response retrieved.")
        return output_tool_call

    def _handle_tool_reasoning(self, output_tool_call):

        logger.info("Executing the reasoning process.")
        query_string = self.tool_usage_dict.get("parameters").get("query")

        output = run_process_reasoning(
            agent_id=self.assistant.id,
            chat_id=self.chat.id,
            reasoning_query=query_string
        )

        output_str = json.dumps(
            output,
            sort_keys=True,
            default=str
        )

        output_tool_call += output_str
        logger.info(f"Reasoning response retrieved.")
        return output_tool_call

    def _handle_tool_analyze_code(self, f_uris, img_uris, output_tool_call):

        logger.info("Executing the analyze code process.")
        file_paths = self.tool_usage_dict.get("parameters").get("file_paths")
        query_string = self.tool_usage_dict.get("parameters").get("query")

        output, f_uris, img_uris = run_analyze_code(
            agent_id=self.assistant.id,
            chat_id=self.chat.id,
            f_uris=file_paths,
            query_content_str=query_string
        )

        output_str = json.dumps(
            output,
            sort_keys=True,
            default=str
        )

        output_tool_call += output_str
        logger.info(f"Analyze code response retrieved.")
        return f_uris, img_uris, output_tool_call

    def _handle_tool_infer_with_ml(self, output_tool_call):

        logger.info("Executing the infer with ML process.")

        ml_base_connection_id = self.tool_usage_dict.get("parameters").get("ml_base_connection_id")
        model_path = self.tool_usage_dict.get("parameters").get("model_path")
        input_data_paths = self.tool_usage_dict.get("parameters").get("input_data_paths")
        query = self.tool_usage_dict.get("parameters").get("query")

        output = run_predict_with_ml(
            c_id=ml_base_connection_id,
            chat_id=self.chat.id,
            model_item_url=model_path,
            input_data_uris=input_data_paths,
            inference_query=query
        )

        output_str = json.dumps(
            output,
            sort_keys=True,
            default=str
        )

        output_tool_call += output_str
        logger.info(f"Infer with ML response retrieved.")
        return output_tool_call

    def _handle_tool_http_client_retrieval(self, output_tool_call):

        logger.info("Executing the HTTP client retrieval process.")
        c_id = self.tool_usage_dict.get("parameters").get("media_storage_connection_id")

        download_url = self.tool_usage_dict.get("parameters").get("url")

        output = run_http_retrieval(
            connection_id=c_id,
            url=download_url
        )

        output_str = json.dumps(
            output,
            sort_keys=True,
            default=str
        )

        output_tool_call += output_str
        logger.info(f"HTTP client retrieval response retrieved.")
        return output_tool_call

    def _handle_tool_media_manager_query(
        self,
        f_uris,
        img_uris,
        output_tool_call
    ):

        from apps.core.tool_calls.core_services.core_service_query_media_manager import run_query_media_manager

        logger.info("Executing the media manager query process.")
        c_id = self.tool_usage_dict.get("parameters").get("media_storage_connection_id")
        chat_id = self.chat.id
        query = self.tool_usage_dict.get("parameters").get("query")
        type = self.tool_usage_dict.get("parameters").get("type")
        file_paths = self.tool_usage_dict.get("parameters").get("file_paths")

        output, f_uris, img_uris = run_query_media_manager(
            c_id=c_id,
            chat_id=chat_id,
            manager_file_type=type,
            f_uris=file_paths,
            manager_query=query
        )

        output_str = json.dumps(
            output,
            sort_keys=True,
            default=str
        )

        output_tool_call += output_str
        logger.info(f"Media manager query response retrieved.")
        return f_uris, img_uris, output_tool_call

    def _handle_tool_ssh_system(self, output_tool_call):

        logger.info("Executing the SSH system command process.")
        c_id = self.tool_usage_dict.get("parameters").get("file_system_connection_id")
        commands = self.tool_usage_dict.get("parameters").get("commands")

        output = run_execute_ssh_system_commands(
            c_id=c_id,
            bash_commands=commands
        )

        output_str = json.dumps(
            output,
            sort_keys=True,
            default=str
        )

        output_tool_call += output_str
        logger.info(f"SSH system command response retrieved.")
        return output_tool_call

    def _handle_tool_intra_memory_query(self, output_tool_call):

        logger.info("Executing the intra memory query process.")
        query = self.tool_usage_dict.get("parameters").get("query")

        output = run_query_intra_memory(
            assistant_chat_id=self.chat.id,
            intra_memory_query=query
        )

        output_str = json.dumps(
            output,
            sort_keys=True,
            default=str
        )

        output_tool_call += output_str
        logger.info(f"Intra memory query response retrieved.")
        return output_tool_call

    def _handle_tool_code_base_query(self, output_tool_call):

        logger.info("Executing the code base query process.")
        c_id = self.tool_usage_dict.get("parameters").get("code_base_storage_connection_id")
        query = self.tool_usage_dict.get("parameters").get("query")
        alpha = self.tool_usage_dict.get("parameters").get("alpha")

        output = run_query_code_base(
            c_id=c_id,
            query_content_str=query,
            semantic_alpha=alpha
        )

        output_str = json.dumps(
            output,
            sort_keys=True,
            default=str
        )

        output_tool_call += output_str
        logger.info(f"Code base query response retrieved.")
        return output_tool_call

    def _handle_tool_vector_base_query(self, output_tool_call):

        logger.info("Executing the vector store query process.")
        c_id = self.tool_usage_dict.get("parameters").get("knowledge_base_connection_id")
        query = self.tool_usage_dict.get("parameters").get("query")
        alpha = self.tool_usage_dict.get("parameters").get("alpha")

        output = run_query_vector_store(
            c_id=c_id,
            vector_store_query=query,
            semantic_alpha=alpha
        )

        output_str = json.dumps(
            output,
            sort_keys=True,
            default=str
        )

        output_tool_call += output_str
        logger.info(f"Vector store query response retrieved.")
        return output_tool_call

    def _handle_tool_sql_query(self, output_tool_call):

        logger.info("Executing the SQL query process.")
        c_id = self.tool_usage_dict.get("parameters").get("database_connection_id")
        query_type = self.tool_usage_dict.get("parameters").get("type")
        sql_query = self.tool_usage_dict.get("parameters").get("sql_query")

        output = run_sql_query(
            c_id=c_id,
            sql_query_type=query_type,
            query_content=sql_query
        )

        output_str = json.dumps(
            output,
            sort_keys=True,
            default=str
        )

        output_tool_call += output_str
        logger.info(f"SQL query response retrieved.")
        return output_tool_call

    def _handle_tool_nosql_query(self, output_tool_call):

        logger.info("Executing the NoSQL query process.")
        c_id = self.tool_usage_dict.get("parameters").get("database_connection_id")
        query_type = self.tool_usage_dict.get("parameters").get("type")
        nosql_query = self.tool_usage_dict.get("parameters").get("nosql_query")

        output = run_nosql_query(
            c_id=c_id,
            nosql_query_type=query_type,
            query_content=nosql_query
        )

        output_str = json.dumps(
            output,
            sort_keys=True,
            default=str
        )

        output_tool_call += output_str
        logger.info(f"NoSQL query response retrieved.")
        return output_tool_call

    def _handle_tool_dashboard_statistics_query(self, output_tool_call):

        logger.info("Executing the Dashboard Statistics query process.")
        user_id = self.chat.user.id

        output = run_query_dashboard_statistics(
            llm_core=self.assistant.llm_model,
            user_id=user_id
        )

        output_str = json.dumps(
            output,
            sort_keys=True,
            default=str
        )

        output_tool_call += output_str
        logger.info(f"Dashboard Statistics query response retrieved.")
        return output_tool_call

    def _handle_tool_metakanban_query(self, output_tool_call):

        logger.info("Executing the MetaKanban board query process.")
        c_id = self.tool_usage_dict.get("parameters").get("connection_id")
        query = self.tool_usage_dict.get("parameters").get("query")

        output = run_query_execute_metakanban(
            c_id=c_id,
            query=query
        )

        output_str = json.dumps(
            output,
            sort_keys=True,
            default=str
        )

        output_tool_call += output_str
        logger.info(f"Metakanban board query response retrieved.")
        return output_tool_call

    def _handle_tool_metatempo_query(self, output_tool_call):

        logger.info("Executing the MetaTempo tracker query process.")
        c_id = self.tool_usage_dict.get("parameters").get("connection_id")
        query = self.tool_usage_dict.get("parameters").get("query")
        action = self.tool_usage_dict.get("parameters").get("action")

        output = run_query_execute_metatempo(
            c_id=c_id,
            action=action,
            query=query
        )

        output_str = json.dumps(
            output,
            sort_keys=True,
            default=str
        )

        output_tool_call += output_str
        logger.info(f"MetaTempo tracker query response retrieved.")
        return output_tool_call

    def _handle_tool_orchestration_trigger(self, output_tool_call):

        logger.info("Executing the Orchestration trigger process.")
        user = self.chat.user
        c_id = self.tool_usage_dict.get("parameters").get("connection_id")
        query = self.tool_usage_dict.get("parameters").get("query")

        output = run_query_trigger_orchestration(
            user=user,
            c_id=c_id,
            user_query=query
        )

        output_str = json.dumps(
            output,
            sort_keys=True,
            default=str
        )

        output_tool_call += output_str
        logger.info(f"Orchestration trigger process response retrieved.")
        return output_tool_call

    def _handle_tool_scheduled_job_logs_query(self, output_tool_call):

        logger.info("Executing the Scheduled Job Logs query process.")

        output = run_query_execute_scheduled_job_logs(
            assistant=self.assistant
        )

        output_str = json.dumps(
            output,
            sort_keys=True,
            default=str
        )

        output_tool_call += output_str
        logger.info(f"Scheduled Job Logs query process response retrieved.")
        return output_tool_call

    def _handle_tool_triggered_job_logs_query(self, output_tool_call):
        logger.info("Executing the Triggered Job Logs query process.")

        output = run_query_execute_triggered_job_logs(
            assistant=self.assistant
        )

        output_str = json.dumps(
            output,
            sort_keys=True,
            default=str
        )

        output_tool_call += output_str
        logger.info(f"Triggered Job Logs query process response retrieved.")
        return output_tool_call

    def _handle_tool_smart_contract_gen_query(self, output_tool_call):
        logger.info("Executing the Smart Contract generation query process.")
        user = self.chat.user

        wallet_id = self.tool_usage_dict.get("parameters").get("wallet_id")
        nickname = self.tool_usage_dict.get("parameters").get("nickname")
        description = self.tool_usage_dict.get("parameters").get("description")
        category = self.tool_usage_dict.get("parameters").get("category")
        contract_template = self.tool_usage_dict.get("parameters").get("contract_template")
        creation_prompt = self.tool_usage_dict.get("parameters").get("creation_prompt")
        maximum_gas_limit = self.tool_usage_dict.get("parameters").get("maximum_gas_limit")
        gas_price_gwei = self.tool_usage_dict.get("parameters").get("gas_price_gwei")

        output = run_query_execute_smart_contract_generation_query(
            wallet_id=wallet_id,
            user=user,
            llm_model=self.assistant.llm_model,
            nickname=nickname,
            description=description,
            category=category,
            contract_template=contract_template,
            creation_prompt=creation_prompt,
            maximum_gas_limit=maximum_gas_limit,
            gas_price_gwei=gas_price_gwei
        )

        output_str = json.dumps(
            output,
            sort_keys=True,
            default=str
        )

        output_tool_call += output_str
        logger.info(f"Smart contract generation query process response retrieved.")
        return output_tool_call

    def _handle_tool_hadron_node_query(self, output_tool_call):

        logger.info("Executing the Hadron Node query process.")

        c_id = self.tool_usage_dict.get("parameters").get("connection_id")
        query = self.tool_usage_dict.get("parameters").get("query")

        output = run_query_execute_hadron_node(
            c_id=c_id,
            query=query
        )

        output_str = json.dumps(
            output,
            sort_keys=True,
            default=str
        )

        output_tool_call += output_str
        logger.info(f"Hadron Node query process response retrieved.")
        return output_tool_call

    def call_internal_tool_service_lean(self):

        logger.info("Calling the internal tool service.")

        try:

            if isinstance(self.tool_usage_dict_stringified, dict):
                logger.info("Tool usage dictionary is already a dictionary.")
                self.tool_usage_dict = self.tool_usage_dict_stringified

            else:
                logger.info("Tool usage dictionary is a string. Converting it to a dictionary.")
                self.tool_usage_dict = json.loads(self.tool_usage_dict_stringified)

        except Exception as e:
            logger.error(f"Error occurred while converting the tool usage dictionary to a dictionary: {e}")
            return get_json_decode_error_log(
                error_logs=str(e)
            ), None, None, None

        f_uris, img_uris = [], []

        error_msg = verify_main_call_or_query_content(
            content=self.tool_usage_dict
        )
        if error_msg:
            logger.error(f"Error occurred while verifying the main call or query content: {error_msg}")
            return error_msg, None, None, None

        defined_tool_descriptor = self.tool_usage_dict.get("tool")
        output_tool_call = f"""
                    Tool Response: {defined_tool_descriptor}

                    '''
                """

        if defined_tool_descriptor == ToolCallDescriptorNames.EXECUTE_EXPERT_NETWORK_QUERY:

            error_msg = verify_expert_network_query_content(
                content=self.tool_usage_dict
            )
            if error_msg:
                return error_msg, None, None, None

            assistant_id = self.tool_usage_dict.get("parameters").get("assistant_id")
            query = self.tool_usage_dict.get("parameters").get("query")
            image_urls = self.tool_usage_dict.get("parameters").get("image_urls")
            file_urls = self.tool_usage_dict.get("parameters").get("file_urls")

            expert_network_response = execute_expert_network_query(
                agent_id=assistant_id,
                xn_query=query,
                img_uris=image_urls,
                f_uris=file_urls
            )

            expert_network_response_raw_str = json.dumps(
                expert_network_response,
                sort_keys=True,
                default=str
            )

            output_tool_call += expert_network_response_raw_str
            logger.info(f"Expert network query response retrieved.")

        elif defined_tool_descriptor == ToolCallDescriptorNames.EXECUTE_SEMANTOR_SEARCH_QUERY:

            error_msg = verify_semantor_search_query_content(
                content=self.tool_usage_dict
            )
            if error_msg:
                return error_msg, None, None, None

            query = self.tool_usage_dict.get("parameters").get("query")

            semantor_response = execute_semantor_search_query(
                user=self.user,
                llm_model=self.assistant.llm_model,
                query=query
            )

            semantor_response_raw_str = json.dumps(
                semantor_response,
                sort_keys=True,
                default=str
            )

            output_tool_call += semantor_response_raw_str
            logger.info(f"Semantor query response retrieved.")

        elif defined_tool_descriptor == ToolCallDescriptorNames.EXECUTE_SEMANTOR_CONSULTATION_QUERY:

            error_msg = verify_semantor_consultation_query_content(
                content=self.tool_usage_dict
            )
            if error_msg:
                return error_msg, None, None, None

            is_local = self.tool_usage_dict.get("parameters").get("is_local")
            object_id = self.tool_usage_dict.get("parameters").get("object_id")
            query = self.tool_usage_dict.get("parameters").get("query")

            semantor_response = execute_semantor_consultation_query(
                user=self.user,
                llm_model=self.assistant.llm_model,
                is_local=is_local
                , object_id=object_id,
                query=query,
                image_urls=img_uris,
                file_urls=f_uris
            )

            semantor_consult_response_raw_str = json.dumps(
                semantor_response,
                sort_keys=True,
                default=str
            )

            output_tool_call += semantor_consult_response_raw_str
            logger.info(f"Semantor consultation response retrieved.")

        elif defined_tool_descriptor == ToolCallDescriptorNames.EXECUTE_INTRA_MEMORY_QUERY:
            error_msg = verify_leanmod_memory_query_content(
                content=self.tool_usage_dict
            )
            if error_msg:
                return error_msg, None, None, None

            query = self.tool_usage_dict.get("parameters").get("query")

            leanmod_memory_query_output = run_query_leanmod_memory(
                leanmod_chat_id=self.chat.id,
                leanmod_memory_query=query
            )

            leanmod_memory_query_output_raw_str = json.dumps(
                leanmod_memory_query_output,
                sort_keys=True,
                default=str
            )

            output_tool_call += leanmod_memory_query_output_raw_str
            logger.info(f"LeanMod Intra memory query response retrieved.")

        ##################################################

        # NO TOOL FOUND
        else:

            logger.error(f"No tool found with the descriptor: {defined_tool_descriptor}")

            return get_no_tool_found_error_log(
                query_name=defined_tool_descriptor
            ), defined_tool_descriptor, f_uris, img_uris

        ##################################################
        output_tool_call += f"""
                    '''
                """
        if f_uris:
            for i, uri in enumerate(f_uris):

                if not uri.startswith("http"):
                    uri = f"{MEDIA_URL}{uri}"

                f_uris[i] = uri

        if img_uris:
            for i, uri in enumerate(img_uris):

                if not uri.startswith("http"):
                    uri = f"{MEDIA_URL}{uri}"

                img_uris[i] = uri

        logger.info(f"Processed the files and images. Returning the output.")
        return output_tool_call, defined_tool_descriptor, f_uris, img_uris

    #####

    def call_internal_tool_service_voidforger(
        self,
        fermion__is_fermion_supervised=False,
        fermion__export_type=None,
        fermion__endpoint=None
    ):

        logger.info("Calling the internal tool service.")

        try:
            if isinstance(self.tool_usage_dict_stringified, dict):
                logger.info("Tool usage dictionary is already a dictionary.")
                self.tool_usage_dict = self.tool_usage_dict_stringified

            else:
                logger.info("Tool usage dictionary is a string. Converting it to a dictionary.")
                self.tool_usage_dict = json.loads(self.tool_usage_dict_stringified)

        except Exception as e:
            logger.error(f"Error occurred while converting the tool usage dictionary to a dictionary: {e}")
            return get_json_decode_error_log(
                error_logs=str(e)
            ), None, None, None

        f_uris, img_uris = [], []

        error_msg = verify_main_call_or_query_content(
            content=self.tool_usage_dict
        )
        if error_msg:
            logger.error(f"Error occurred while verifying the main call or query content: {error_msg}")
            return error_msg, None, None, None

        defined_tool_descriptor = self.tool_usage_dict.get("tool")
        output_tool_call = f"""
                    Tool Response: {defined_tool_descriptor}

                    '''
                """

        if defined_tool_descriptor == ToolCallDescriptorNames.EXECUTE_VOIDFORGER_OLD_MESSAGE_SEARCH_QUERY:

            transmit_websocket_log(
                f"""🧮 VoidForger is searching previous chat messages in his long term memory.""",
                chat_id=self.chat.id,
                fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                fermion__export_type=fermion__export_type,
                fermion__endpoint=fermion__endpoint
            )

            error_msg = verify_voidforger_old_message_search_query_content(
                content=self.tool_usage_dict
            )
            if error_msg:
                transmit_websocket_log(
                    f"""❌ VoidForger attempted to perform an execution of an invalid or unauthorized tool.""",
                    chat_id=self.chat.id,
                    fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                    fermion__export_type=fermion__export_type,
                    fermion__endpoint=fermion__endpoint
                )

                return error_msg, None, None, None

            transmit_websocket_log(
                f"""✅ VoidForger's request for long term memory search has been approved by the system.""",
                chat_id=self.chat.id,
                fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                fermion__export_type=fermion__export_type,
                fermion__endpoint=fermion__endpoint
            )

            query = self.tool_usage_dict.get("parameters").get("query")

            voidforger_old_message_query_response = execute_voidforger_old_message_search_query(
                user=self.user,
                voidforger_id=self.assistant.id,
                voidforger_chat_id=self.chat.id,
                query=query
            )

            transmit_websocket_log(
                f"""🧮 System provided VoidForger with the old messages based on the query attempt.""",
                chat_id=self.chat.id,
                fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                fermion__export_type=fermion__export_type,
                fermion__endpoint=fermion__endpoint
            )

            voidforger_old_message_query_response_raw_str = json.dumps(
                voidforger_old_message_query_response,
                sort_keys=True,
                default=str
            )

            output_tool_call += voidforger_old_message_query_response_raw_str

            transmit_websocket_log(
                f"""⛙ Organizing and reporting the outputs for delivering to VoidForger.""",
                chat_id=self.chat.id,
                fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                fermion__export_type=fermion__export_type,
                fermion__endpoint=fermion__endpoint
            )

            VoidForgerActionMemoryLog.objects.create(
                voidforger=self.assistant,
                action_type=VoidForgerActionTypesNames.OLD_CHAT_MESSAGES_SEARCH_ATTEMPT,
                action_order_raw_text=f"""
                    Tool Request:

                    {json.dumps(self.tool_usage_dict)}

                    Tool Response:

                    {voidforger_old_message_query_response_raw_str}
                """,
            )

            logger.info(f"Voidforger old message search query response retrieved.")

        elif defined_tool_descriptor == ToolCallDescriptorNames.EXECUTE_VOIDFORGER_ACTION_HISTORY_LOG_SEARCH_QUERY:

            transmit_websocket_log(
                f"""🧮 VoidForger is checking his previous actions to find relevant information.""",
                chat_id=self.chat.id,
                fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                fermion__export_type=fermion__export_type,
                fermion__endpoint=fermion__endpoint
            )

            error_msg = verify_voidforger_action_history_log_search_query_content(
                content=self.tool_usage_dict
            )
            if error_msg:
                transmit_websocket_log(
                    f"""❌ VoidForger attempted to perform an execution of an invalid or unauthorized tool.""",
                    chat_id=self.chat.id,
                    fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                    fermion__export_type=fermion__export_type,
                    fermion__endpoint=fermion__endpoint
                )

                return error_msg, None, None, None

            transmit_websocket_log(
                f"""✅ VoidForger's request for action history search has been approved by the system.""",
                chat_id=self.chat.id,
                fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                fermion__export_type=fermion__export_type,
                fermion__endpoint=fermion__endpoint
            )

            query = self.tool_usage_dict.get("parameters").get("query")

            voidforger_action_history_log_search_query_response = execute_voidforger_action_history_log_search_query(
                user=self.user,
                voidforger_id=self.assistant.id,
                query=query
            )

            transmit_websocket_log(
                f"""🧮 System provided VoidForger with the action history logs based on the query attempt.""",
                chat_id=self.chat.id,
                fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                fermion__export_type=fermion__export_type,
                fermion__endpoint=fermion__endpoint
            )

            voidforger_action_history_log_search_query_response_raw_str = json.dumps(
                voidforger_action_history_log_search_query_response,
                sort_keys=True,
                default=str
            )

            output_tool_call += voidforger_action_history_log_search_query_response_raw_str

            transmit_websocket_log(
                f"""⛙ Organizing and reporting the outputs for delivering to VoidForger.""",
                chat_id=self.chat.id,
                fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                fermion__export_type=fermion__export_type,
                fermion__endpoint=fermion__endpoint
            )

            VoidForgerActionMemoryLog.objects.create(
                voidforger=self.assistant,
                action_type=VoidForgerActionTypesNames.ACTION_LOG_SEARCH_ATTEMPT,
                action_order_raw_text=f"""
                    Tool Request:

                    {json.dumps(self.tool_usage_dict)}

                    Tool Response:

                    {voidforger_action_history_log_search_query_response}
                """,
            )

            logger.info(f"Voidforger action history log search query response retrieved.")

        elif defined_tool_descriptor == ToolCallDescriptorNames.EXECUTE_VOIDFORGER_AUTO_EXECUTION_LOG_SEARCH_QUERY:

            transmit_websocket_log(
                f"""🧮 VoidForger is searching his auto-execution logs to find relevant information.""",
                chat_id=self.chat.id,
                fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                fermion__export_type=fermion__export_type,
                fermion__endpoint=fermion__endpoint
            )

            error_msg = verify_voidforger_auto_execution_log_search_query_content(
                content=self.tool_usage_dict
            )
            if error_msg:
                transmit_websocket_log(
                    f"""❌ VoidForger attempted to perform an execution of an invalid or unauthorized tool.""",
                    chat_id=self.chat.id,
                    fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                    fermion__export_type=fermion__export_type,
                    fermion__endpoint=fermion__endpoint
                )

                return error_msg, None, None, None

            transmit_websocket_log(
                f"""✅ VoidForger's request for auto-execution memory search has been approved by the system.""",
                chat_id=self.chat.id,
                fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                fermion__export_type=fermion__export_type,
                fermion__endpoint=fermion__endpoint
            )

            query = self.tool_usage_dict.get("parameters").get("query")

            voidforger_auto_execution_log_search_query_response = execute_voidforger_auto_execution_log_search_query(
                user=self.user,
                voidforger_id=self.assistant.id,
                query=query
            )

            transmit_websocket_log(
                f"""🧮 System provided VoidForger with the auto-execution memory logs based on the query attempt.""",
                chat_id=self.chat.id,
                fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                fermion__export_type=fermion__export_type,
                fermion__endpoint=fermion__endpoint
            )

            voidforger_auto_execution_log_search_query_response_raw_str = json.dumps(
                voidforger_auto_execution_log_search_query_response,
                sort_keys=True,
                default=str
            )

            transmit_websocket_log(
                f"""⛙ Organizing and reporting the outputs for delivering to VoidForger.""",
                chat_id=self.chat.id,
                fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                fermion__export_type=fermion__export_type,
                fermion__endpoint=fermion__endpoint
            )

            output_tool_call += voidforger_auto_execution_log_search_query_response_raw_str

            VoidForgerActionMemoryLog.objects.create(
                voidforger=self.assistant,
                action_type=VoidForgerActionTypesNames.AUTO_EXECUTION_LOG_SEARCH_ATTEMPT,
                action_order_raw_text=f"""
                    Tool Request:

                    {json.dumps(self.tool_usage_dict)}

                    Tool Response:

                    {voidforger_auto_execution_log_search_query_response_raw_str}
                """,
            )

            logger.info(f"Voidforger auto execution log search query response retrieved.")

        elif defined_tool_descriptor == ToolCallDescriptorNames.EXECUTE_VOIDFORGER_LEANMOD_ORACLE_SEARCH_QUERY:

            transmit_websocket_log(
                f"""🧮 VoidForger is using Semantor network to find worker Oracle assistants.""",
                chat_id=self.chat.id,
                fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                fermion__export_type=fermion__export_type,
                fermion__endpoint=fermion__endpoint
            )

            error_msg = verify_voidforger_leanmod_oracle_search_query_content(
                content=self.tool_usage_dict
            )
            if error_msg:
                transmit_websocket_log(
                    f"""❌ VoidForger attempted to perform an execution of an invalid or unauthorized tool.""",
                    chat_id=self.chat.id,
                    fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                    fermion__export_type=fermion__export_type,
                    fermion__endpoint=fermion__endpoint
                )

                return error_msg, None, None, None

            transmit_websocket_log(
                f"""✅ VoidForger's request for Semantor Oracle assistant search has been approved by the system.""",
                chat_id=self.chat.id,
                fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                fermion__export_type=fermion__export_type,
                fermion__endpoint=fermion__endpoint
            )

            query = self.tool_usage_dict.get("parameters").get("query")

            voidforger_leanmod_oracle_search_query_response = execute_voidforger_leanmod_oracle_search_query(
                user=self.user,
                llm_model=self.assistant.llm_model,
                query=query
            )

            transmit_websocket_log(
                f"""🧮 System provided VoidForger with the Semantor network nodes based on the related Oracle search.""",
                chat_id=self.chat.id,
                fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                fermion__export_type=fermion__export_type,
                fermion__endpoint=fermion__endpoint
            )

            voidforger_leanmod_oracle_search_query_response_raw_str = json.dumps(
                voidforger_leanmod_oracle_search_query_response,
                sort_keys=True,
                default=str
            )

            output_tool_call += voidforger_leanmod_oracle_search_query_response_raw_str

            transmit_websocket_log(
                f"""⛙ Organizing and reporting the outputs for delivering to VoidForger.""",
                chat_id=self.chat.id,
                fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                fermion__export_type=fermion__export_type,
                fermion__endpoint=fermion__endpoint
            )

            VoidForgerActionMemoryLog.objects.create(
                voidforger=self.assistant,
                action_type=VoidForgerActionTypesNames.INTERMEDIARY_AGENT_SEARCH_ATTEMPT,
                action_order_raw_text=f"""
                    Tool Request:

                    {json.dumps(self.tool_usage_dict)}

                    Tool Response:

                    {voidforger_leanmod_oracle_search_query_response}
                """,
            )

            logger.info(f"Voidforger leanmod oracle search query response retrieved.")

        elif defined_tool_descriptor == ToolCallDescriptorNames.EXECUTE_VOIDFORGER_LEANMOD_ORACLE_COMMAND_ORDER:

            transmit_websocket_log(
                f"""🧮 VoidForger is ordering an Oracle assistant to perform a task.""",
                chat_id=self.chat.id,
                fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                fermion__export_type=fermion__export_type,
                fermion__endpoint=fermion__endpoint
            )

            error_msg = verify_voidforger_leanmod_oracle_command_order_content(
                content=self.tool_usage_dict
            )
            if error_msg:
                transmit_websocket_log(
                    f"""❌ VoidForger attempted to perform an execution of an invalid or unauthorized tool.""",
                    chat_id=self.chat.id,
                    fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                    fermion__export_type=fermion__export_type,
                    fermion__endpoint=fermion__endpoint
                )

                return error_msg, None, None, None

            transmit_websocket_log(
                f"""✅ VoidForger's request for ordering invocation of an Oracle assistant has been approved by the system.""",
                chat_id=self.chat.id,
                fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                fermion__export_type=fermion__export_type,
                fermion__endpoint=fermion__endpoint
            )

            object_id = self.tool_usage_dict.get("parameters").get("object_id")
            query = self.tool_usage_dict.get("parameters").get("query")
            image_urls = self.tool_usage_dict.get("parameters").get("image_urls")
            file_urls = self.tool_usage_dict.get("parameters").get("file_urls")

            voidforger_leanmod_oracle_command_order_response = execute_voidforger_leanmod_oracle_command_order(
                user=self.user,
                llm_model=self.assistant.llm_model,
                object_id=object_id,
                xn_query=query,
                img_uris=image_urls,
                f_uris=file_urls
            )

            transmit_websocket_log(
                f"""🧮 System delivered the order of VoidForger to Oracle assistant successfully through Semantor network.""",
                chat_id=self.chat.id,
                fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                fermion__export_type=fermion__export_type,
                fermion__endpoint=fermion__endpoint
            )

            voidforger_leanmod_oracle_command_order_response_raw_str = json.dumps(
                voidforger_leanmod_oracle_command_order_response,
                sort_keys=True,
                default=str
            )

            output_tool_call += voidforger_leanmod_oracle_command_order_response_raw_str

            transmit_websocket_log(
                f"""⛙ Organizing and reporting the outputs for delivering to VoidForger.""",
                chat_id=self.chat.id,
                fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                fermion__export_type=fermion__export_type,
                fermion__endpoint=fermion__endpoint
            )

            VoidForgerActionMemoryLog.objects.create(
                voidforger=self.assistant,
                action_type=VoidForgerActionTypesNames.INTERMEDIARY_AGENT_COMMAND,
                action_order_raw_text=f"""
                    Tool Request:

                    {json.dumps(self.tool_usage_dict)}

                    Tool Response:

                    {voidforger_leanmod_oracle_command_order_response_raw_str}
                """,
            )

            logger.info(f"Voidforger leanmod oracle command order response retrieved.")

        ##################################################

        # NO TOOL FOUND
        else:

            transmit_websocket_log(
                f"""❌ VoidForger attempted to perform an execution of an invalid or unauthorized tool.""",
                chat_id=self.chat.id,
                fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                fermion__export_type=fermion__export_type,
                fermion__endpoint=fermion__endpoint
            )

            logger.error(f"No tool found with the descriptor: {defined_tool_descriptor}")
            return (
                get_no_tool_found_error_log(
                    query_name=defined_tool_descriptor
                ),
                defined_tool_descriptor,
                f_uris,
                img_uris
            )

        ##################################################

        output_tool_call += f"""
                    '''
                """

        if f_uris:
            for i, uri in enumerate(f_uris):
                if not uri.startswith("http"):
                    uri = f"{MEDIA_URL}{uri}"
                f_uris[i] = uri

        if img_uris:
            for i, uri in enumerate(img_uris):
                if not uri.startswith("http"):
                    uri = f"{MEDIA_URL}{uri}"
                img_uris[i] = uri

        logger.info(f"Processed the files and images. Returning the output.")
        return output_tool_call, defined_tool_descriptor, f_uris, img_uris
