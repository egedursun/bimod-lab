#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: system_prompt_factory_builder.py
#  Last Modified: 2024-10-05 02:25:59
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

from apps.core.system_prompts.agent_configuration.agent_related_project_items_prompt_manager import \
    build_agent_related_project_items_prompt
from apps.core.system_prompts.agent_configuration.target_audience_prompt_manager import build_target_audience_prompt
from apps.core.system_prompts.agent_configuration.intra_context_memory_prompt_manager import \
    build_intra_context_memory_prompt
from apps.core.system_prompts.agent_configuration.technical_dictionary_prompt_manager import \
    build_technical_dictionary_prompt
from apps.core.system_prompts.agent_configuration.system_internal_instructions_prompt_manager import \
    build_system_internal_instructions_prompt
from apps.core.system_prompts.agent_configuration.standard_memory_prompt_manager import build_standard_memory_prompt
from apps.core.system_prompts.agent_configuration.agent_nickname_prompt_manager import build_agent_nickname_prompt
from apps.core.system_prompts.agent_configuration.spatial_awareness_prompt_manager import \
    build_spatial_awareness_prompt
from apps.core.system_prompts.agent_configuration.internal_principles_prompt_manager import \
    build_internal_principles_prompt
from apps.core.system_prompts.agent_configuration.communication_language_prompt_manager import \
    build_communication_language_prompt
from apps.core.system_prompts.agent_configuration.templated_response_prompt_manager import \
    build_templated_response_prompt
from apps.core.system_prompts.agent_configuration.agent_personality_prompt_manager import \
    build_agent_personality_prompt
from apps.core.system_prompts.agent_configuration.communication_user_tenant_prompt_manager import \
    build_user_tenant_prompt
from apps.core.system_prompts.information_feeds.browser.build_browser_data_source_prompt import \
    build_browsing_data_source_prompt, build_lean_browsing_data_source_prompt, \
    build_semantor_browsing_data_source_prompt
from apps.core.system_prompts.information_feeds.code_base.build_code_base_data_source_prompt import \
    build_code_base_data_source_prompt, build_lean_code_base_data_source_prompt, \
    build_semantor_code_base_data_source_prompt
from apps.core.system_prompts.information_feeds.hadron_prime_node_to_assistant.build_hadron_prime_node_to_assistant_data_source_prompt import \
    build_hadron_prime_node_to_assistant_data_source_prompt, \
    build_lean_hadron_prime_node_to_assistant_data_source_prompt, \
    build_semantor_hadron_prime_node_to_assistant_data_source_prompt
from apps.core.system_prompts.information_feeds.media_manager.build_media_manager_data_source_prompt import \
    build_media_manager_data_source_prompt, build_lean_media_manager_data_source_prompt, \
    build_semantor_media_manager_data_source_prompt
from apps.core.system_prompts.information_feeds.metakanban_to_assistant.build_metakanban_to_assistant_data_source_prompt import \
    build_metakanban_to_assistant_data_source_prompt, build_lean_metakanban_to_assistant_data_source_prompt, \
    build_semantor_metakanban_to_assistant_data_source_prompt
from apps.core.system_prompts.information_feeds.metatempo_to_asisstant.build_metatempo_to_assistant_data_source_prompt import \
    build_metatempo_to_assistant_data_source_prompt, build_lean_metatempo_to_assistant_data_source_prompt, \
    build_semantor_metatempo_to_assistant_data_source_prompt
from apps.core.system_prompts.information_feeds.ml_manager.build_ml_models_data_source_prompt import \
    build_ml_models_data_source_prompt, build_lean_ml_models_data_source_prompt, \
    build_semantor_ml_models_data_source_prompt
from apps.core.system_prompts.information_feeds.nosql.build_nosql_data_source_prompt import \
    build_nosql_data_source_prompt, build_lean_nosql_data_source_prompt, build_semantor_nosql_data_source_prompt
from apps.core.system_prompts.information_feeds.orchestration_to_assistant.build_orchestration_to_assistant_data_source_prompt import \
    build_orchestration_to_assistant_data_source_prompt, build_lean_orchestration_to_assistant_data_source_prompt, \
    build_semantor_orchestration_to_assistant_data_source_prompt
from apps.core.system_prompts.information_feeds.smart_contracts.build_smart_contracts_data_source_prompt import \
    build_lean_smart_contracts_data_source_prompt, build_smart_contracts_data_source_prompt
from apps.core.system_prompts.information_feeds.sql.build_sql_data_source_prompt import build_sql_data_source_prompt, \
    build_lean_sql_data_source_prompt, build_semantor_sql_data_source_prompt
from apps.core.system_prompts.information_feeds.ssh_file_system.build_file_system_data_source_prompt import \
    build_file_system_data_source_prompt, build_lean_file_system_data_source_prompt, \
    build_semantor_file_system_data_source_prompt
from apps.core.system_prompts.information_feeds.vector_store.build_vector_store_data_source_prompt import \
    build_vector_store_data_source_prompt, build_lean_vector_store_data_source_prompt, \
    build_semantor_vector_store_data_source_prompt
from apps.core.system_prompts.leanmod.leanmod_guidelines_prompt import build_structured_primary_guidelines_leanmod
from apps.core.system_prompts.leanmod.leanmod_instructions_prompt import build_structured_instructions_prompt_leanmod
from apps.core.system_prompts.leanmod.leanmod_name_prompt import build_structured_name_prompt_leanmod
from apps.core.system_prompts.leanmod.leanmod_place_and_time_prompt import \
    build_structured_place_and_time_prompt_leanmod
from apps.core.system_prompts.leanmod.leanmod_user_information_prompt import \
    build_structured_user_information_prompt_leanmod
from apps.core.system_prompts.leanmod.multimodality.leanmod_multimodality_expert_network_prompt import \
    build_expert_networks_multi_modality_prompt_leanmod
from apps.core.system_prompts.leanmod.tools.execute_query_leanmod_context_memory_tool_prompt import \
    build_tool_prompt__leanmod_context_memory
from apps.core.system_prompts.leanmod.tools.leanmod_semantor_execution_prompt import \
    build_structured_tool_prompt__semantor_consultation_execution_leanmod
from apps.core.system_prompts.leanmod.tools.leanmod_semantor_query_search_prompt import \
    build_structured_tool_prompt__semantor_search_execution_leanmod
from apps.core.system_prompts.leanmod.tools.leanmod_tools_expert_networks_query_prompt import \
    build_structured_tool_prompt__expert_network_query_execution_leanmod
from apps.core.system_prompts.leanmod.tools.leanmod_tools_instructions_prompt import \
    build_structured_tool_usage_instructions_prompt_leanmod
from apps.core.system_prompts.flexible_modalities.restful_api_modality_instructions import \
    build_apis_multi_modality_prompt, \
    build_lean_apis_multi_modality_prompt, build_semantor_apis_multi_modality_prompt
from apps.core.system_prompts.flexible_modalities.py_function_modality_instructions import \
    build_functions_multi_modality_prompt, build_lean_functions_multi_modality_prompt, \
    build_semantor_functions_multi_modality_prompt
from apps.core.system_prompts.flexible_modalities.bash_script_modality_instructions import \
    build_scripts_multi_modality_prompt, \
    build_lean_scripts_multi_modality_prompt, build_semantor_scripts_multi_modality_prompt
from apps.core.system_prompts.tool_call_prompts.generic_instructions_tool_call import \
    build_generic_instructions_tool_call_prompt, build_lean_structured_tool_usage_instructions_prompt
from apps.core.system_prompts.tool_call_prompts.per_tool.execute_audio_tool_prompt import \
    build_tool_prompt__execute_audio
from apps.core.system_prompts.tool_call_prompts.per_tool.execute_browsing_tool_prompt import \
    build_tool_prompt__browsing
from apps.core.system_prompts.tool_call_prompts.per_tool.execute_codebase_query_tool_prompt import \
    build_tool_prompt__execute_codebase_query
from apps.core.system_prompts.tool_call_prompts.per_tool.execute_code_analysis_tool_prompt import \
    build_tool_prompt__analyze_code
from apps.core.system_prompts.tool_call_prompts.per_tool.execute_dashboard_statistics_query_tool_prompt import \
    build_tool_prompt__execute_dashboard_statistics_query
from apps.core.system_prompts.tool_call_prompts.per_tool.execute_hadron_prime_node_query_tool_prompt import \
    build_tool_prompt__execute_hadron_prime_node_query
from apps.core.system_prompts.tool_call_prompts.per_tool.execute_metakanban_query_tool_prompt import \
    build_tool_prompt__execute_metakanban_query
from apps.core.system_prompts.tool_call_prompts.per_tool.execute_metatempo_query_tool_prompt import \
    build_tool_prompt__execute_metatempo_query
from apps.core.system_prompts.tool_call_prompts.per_tool.execute_nosql_query_tool_prompt import \
    build_tool_prompt__execute_nosql_query
from apps.core.system_prompts.tool_call_prompts.per_tool.execute_orchestration_trigger_tool_prompt import \
    build_tool_prompt__execute_orchestration_trigger
from apps.core.system_prompts.tool_call_prompts.per_tool.execute_restful_api_tool_prompt import \
    build_tool_prompt__execute_restful_api
from apps.core.system_prompts.tool_call_prompts.per_tool.execute_code_tool_prompt import \
    build_tool_prompt__execute_code
from apps.core.system_prompts.tool_call_prompts.per_tool.execute_bash_script_tool_prompt import \
    build_tool_prompt__execute_bash_script
from apps.core.system_prompts.tool_call_prompts.per_tool.execute_scheduled_job_logs_query_tool_prompt import \
    build_tool_prompt__execute_scheduled_job_logs_query
from apps.core.system_prompts.tool_call_prompts.per_tool.execute_smart_contract_function_call_prompt import \
    build_tool_prompt__smart_contract_function_call
from apps.core.system_prompts.tool_call_prompts.per_tool.execute_smart_contract_query_tool_prompt import \
    build_tool_prompt__execute_smart_contract_generation_query
from apps.core.system_prompts.tool_call_prompts.per_tool.execute_ssh_file_system_command_tool_prompt import \
    build_tool_prompt__execute_ssh_file_system_command
from apps.core.system_prompts.tool_call_prompts.per_tool.execute_triggered_job_logs_query_tool_prompt import \
    build_tool_prompt__execute_triggered_job_logs_query
from apps.core.system_prompts.tool_call_prompts.per_tool.generate_image_tool_prompt import \
    build_tool_prompt__generate_image
from apps.core.system_prompts.tool_call_prompts.per_tool.edit_image_tool_prompt import \
    build_tool_prompt__edit_image
from apps.core.system_prompts.tool_call_prompts.per_tool.dream_image_tool_prompt import \
    build_tool_prompt__dream_image
from apps.core.system_prompts.tool_call_prompts.per_tool.execute_vector_store_query_tool_prompt import \
    build_tool_prompt__query_vector_store
from apps.core.system_prompts.tool_call_prompts.per_tool.infer_with_machine_learning_tool_prompt import \
    build_tool_prompt__infer_with_machine_learning
from apps.core.system_prompts.tool_call_prompts.per_tool.reasoning_tool_prompt import \
    build_tool_prompt__reasoning
from apps.core.system_prompts.tool_call_prompts.per_tool.execute_sql_query_tool_prompt import \
    build_tool_prompt__execute_sql_query
from apps.core.system_prompts.tool_call_prompts.per_tool.execute_media_manager_query_tool_prompt import \
    build_tool_prompt__media_manager_query
from apps.core.system_prompts.tool_call_prompts.per_tool.retrieval_via_http_client_tool_prompt import \
    build_tool_prompt__retrieval_via_http_client
from apps.core.system_prompts.tool_call_prompts.per_tool.execute_query_intra_context_memory_tool_prompt import \
    build_tool_prompt__intra_context_memory
from apps.core.system_prompts.tool_call_prompts.per_tool.generate_video_tool_prompt import \
    build_tool_prompt__generate_video, build_lean_tool_prompt__generate_video
from apps.assistants.models import Assistant
from apps.core.system_prompts.voidforger.build_voidforger_communication_language_prompt import \
    build_communication_language_prompt_voidforger
from apps.core.system_prompts.voidforger.tools.voidforger_action_history_log_search_prompt import \
    build_structured_tool_prompt__action_history_log_search_voidforger
from apps.core.system_prompts.voidforger.tools.voidforger_auto_execution_log_search_prompt import \
    build_structured_tool_prompt__auto_execution_log_search_voidforger
from apps.core.system_prompts.voidforger.tools.voidforger_leanmod_oracle_command_order_prompt import \
    build_structured_tool_prompt__leanmod_oracle_command_order_voidforger
from apps.core.system_prompts.voidforger.tools.voidforger_leanmod_oracle_search_prompt import \
    build_structured_tool_prompt__leanmod_oracle_search_voidforger
from apps.core.system_prompts.voidforger.tools.voidforger_old_message_search_prompt import \
    build_structured_tool_prompt__old_message_search_execution_voidforger
from apps.core.system_prompts.voidforger.tools.voidforger_tools_instructions_prompt import \
    build_structured_tool_usage_instructions_prompt_voidforger
from apps.core.system_prompts.voidforger.voidforger_agent_personality_prompt import \
    build_agent_personality_prompt_voidforger
from apps.core.system_prompts.voidforger.voidforger_guidelines_prompt import \
    build_structured_primary_guidelines_voidforger
from apps.core.system_prompts.voidforger.voidforger_instructions_prompt import \
    build_structured_instructions_prompt_voidforger
from apps.core.system_prompts.voidforger.voidforger_place_and_time_prompt import \
    build_structured_place_and_time_prompt_voidforger
from apps.core.system_prompts.voidforger.voidforger_user_information_prompt import \
    build_structured_user_information_prompt_voidforger
from apps.leanmod.models import LeanAssistant
from apps.llm_transaction.models import LLMTransaction
from apps.multimodal_chat.models import MultimodalChat, MultimodalLeanChat
from apps.multimodal_chat.utils import transmit_websocket_log
from apps.voidforger.models import VoidForger

logger = logging.getLogger(__name__)


class SystemPromptFactoryBuilder:

    @staticmethod
    def build_system_prompts(
        chat: MultimodalChat,
        assistant: Assistant,
        user: User,
        role: str
    ):

        from apps.core.generative_ai.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps.core.generative_ai.utils import ChatRoles

        agent_nickname = assistant.name
        templated_response = assistant.response_template
        target_audience = assistant.audience
        agent_personality_tone = assistant.tone
        output_language = assistant.response_language

        (
            base_prompt,
            target_audience,
            intra_memory,
            technical_dict,
            main_instructions,
            standard_memory,
            agent_nickname,
            spatial_awareness,
            projects_teams,
            communication_lang,
            templated_response,
            tone,
            comm_user_info
        ) = (
            SystemPromptFactoryBuilder._build_foundation_prompts(
                agent_nickname=agent_nickname,
                agent_personality_tone=agent_personality_tone,
                assistant=assistant,
                chat=chat, output_language=output_language,
                target_audience=target_audience,
                templated_response=templated_response,
                user=user
            )
        )

        (
            browsing_feed,
            codebase_feed,
            ssh_system_feed,
            vector_store_feed,
            media_manager_feed,
            ml_manager_feed,
            sql_feed,
            nosql_feed,
            smart_contract_feed,
            hadron_prime_node_feed,
            metakanban_feed,
            metatempo_feed,
            orchestration_trigger_feed
        ) = (
            SystemPromptFactoryBuilder._build_information_feeds_prompt(
                assistant=assistant
            )
        )

        restful_apis, custom_functions, bash_scripts = (
            SystemPromptFactoryBuilder._build_flexible_modalities_prompts(
                assistant=assistant
            )
        )

        (
            process_audio,
            execute_browsing,
            execute_codebase,
            analyze_code,
            execute_api,
            execute_function,
            execute_script,
            execute_ssh_command,
            generate_image,
            edit_image,
            dream_image,
            query_vector_store,
            predict_with_ml,
            execute_reasoning,
            execute_sql_query,
            execute_nosql_query,
            execute_media_manager,
            generic_tool_calls,
            execute_http_retrieval,
            execute_intra_memory_retrieval,
            generate_video,
            smart_contract_func_call,
            dashboard_statistics,
            hadron_node_query,
            metakanban_query,
            metatempo_query,
            orchestration_trigger,
            scheduled_job_logs,
            triggered_job_logs,
            smart_contract_gen
        ) = (
            SystemPromptFactoryBuilder._build_tool_call_instructions_prompts(
                assistant=assistant
            )
        )

        #
        # MERGE
        #

        merged_prompt = SystemPromptFactoryBuilder._merge_system_prompts(
            foundation=base_prompt,
            apis_feed=restful_apis,
            target_audience=target_audience,
            do_audio=process_audio,
            browsing_feed=browsing_feed,
            do_browsing=execute_browsing,
            codebase_feed=codebase_feed,
            do_codebase=execute_codebase,
            do_analyze_code=analyze_code,
            intra_memory=intra_memory,
            do_api=execute_api,
            do_function=execute_function,
            do_script=execute_script,
            do_ssh_command=execute_ssh_command,
            file_systems=ssh_system_feed,
            functions_feed=custom_functions,
            technical_dictionary=technical_dict,
            do_generate_image=generate_image,
            do_edit_image=edit_image,
            do_dream_image=dream_image,
            generic_instructions=main_instructions,
            vector_store_feed=vector_store_feed,
            do_vector_store=query_vector_store,
            media_store_feed=media_manager_feed,
            standard_memory=standard_memory,
            ml_model_feed=ml_manager_feed,
            agent_nickname=agent_nickname,
            spatial_awareness=spatial_awareness,
            do_ml_model=predict_with_ml,
            do_reasoning=execute_reasoning,
            projects_teams=projects_teams,
            comm_language=communication_lang,
            templated_response=templated_response,
            scripts_feed=bash_scripts,
            sql_feed=sql_feed,
            do_sql_query=execute_sql_query,
            nosql_feed=nosql_feed,
            do_nosql_query=execute_nosql_query,
            do_media_manager=execute_media_manager,
            tone=tone,
            do_instructions=generic_tool_calls,
            do_http_retrieval=execute_http_retrieval,
            user_info=comm_user_info,
            do_intra_memory=execute_intra_memory_retrieval,
            do_generate_video=generate_video,
            smart_contract_feed=smart_contract_feed,
            smart_contract_func_call=smart_contract_func_call,
            dashboard_statistics=dashboard_statistics,
            hadron_node_query=hadron_node_query,
            metakanban_query=metakanban_query,
            metatempo_query=metatempo_query,
            orchestration_trigger=orchestration_trigger,
            scheduled_job_logs=scheduled_job_logs,
            triggered_job_logs=triggered_job_logs,
            smart_contract_gen=smart_contract_gen,
            hadron_prime_node_feed=hadron_prime_node_feed,
            metakanban_feed=metakanban_feed,
            metatempo_feed=metatempo_feed,
            orchestration_trigger_feed=orchestration_trigger_feed
        )

        prompt = {
            "role": role,
            "content": merged_prompt
        }

        tx = LLMTransaction.objects.create(
            organization=assistant.organization,
            model=assistant.llm_model,
            responsible_user=user,
            responsible_assistant=assistant,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            transaction_context_content=merged_prompt,
            llm_cost=0, internal_service_cost=0,
            tax_cost=0,
            total_cost=0,
            total_billable_cost=0,
            transaction_type=ChatRoles.SYSTEM,
            transaction_source=chat.chat_source
        )

        chat.transactions.add(tx)
        chat.save()
        return prompt

    @staticmethod
    def _merge_system_prompts(
        foundation,
        apis_feed,
        target_audience,
        do_audio,
        browsing_feed,
        do_browsing,
        codebase_feed,
        do_codebase,
        do_analyze_code,
        intra_memory,
        do_api,
        do_function,
        do_script,
        do_ssh_command,
        file_systems,
        functions_feed,
        technical_dictionary,
        do_generate_image,
        do_edit_image,
        do_dream_image,
        generic_instructions,
        vector_store_feed,
        do_vector_store,
        media_store_feed,
        standard_memory,
        ml_model_feed,
        agent_nickname,
        spatial_awareness,
        do_ml_model,
        do_reasoning,
        projects_teams,
        comm_language,
        templated_response,
        scripts_feed,
        sql_feed,
        do_sql_query,
        nosql_feed,
        do_nosql_query,
        do_media_manager,
        tone,
        do_instructions,
        do_http_retrieval,
        user_info,
        do_intra_memory,
        do_generate_video,
        smart_contract_feed,
        smart_contract_func_call,
        dashboard_statistics,
        hadron_node_query,
        metakanban_query,
        metatempo_query,
        orchestration_trigger,
        scheduled_job_logs,
        triggered_job_logs,
        smart_contract_gen,
        hadron_prime_node_feed,
        metakanban_feed,
        metatempo_feed,
        orchestration_trigger_feed
    ):
        combined_system_instructions = foundation
        combined_system_instructions += agent_nickname
        combined_system_instructions += generic_instructions
        combined_system_instructions += templated_response
        combined_system_instructions += target_audience
        combined_system_instructions += tone
        combined_system_instructions += projects_teams
        combined_system_instructions += comm_language
        combined_system_instructions += user_info
        combined_system_instructions += standard_memory
        combined_system_instructions += technical_dictionary
        combined_system_instructions += spatial_awareness
        combined_system_instructions += intra_memory

        combined_system_instructions += sql_feed
        combined_system_instructions += nosql_feed
        combined_system_instructions += vector_store_feed
        combined_system_instructions += codebase_feed
        combined_system_instructions += file_systems
        combined_system_instructions += media_store_feed
        combined_system_instructions += ml_model_feed
        combined_system_instructions += browsing_feed
        combined_system_instructions += functions_feed
        combined_system_instructions += apis_feed
        combined_system_instructions += scripts_feed
        combined_system_instructions += smart_contract_feed
        combined_system_instructions += hadron_prime_node_feed
        combined_system_instructions += metakanban_feed
        combined_system_instructions += metatempo_feed
        combined_system_instructions += orchestration_trigger_feed

        combined_system_instructions += do_instructions
        combined_system_instructions += do_sql_query
        combined_system_instructions += do_nosql_query
        combined_system_instructions += do_vector_store
        combined_system_instructions += do_codebase
        combined_system_instructions += do_intra_memory
        combined_system_instructions += do_ssh_command
        combined_system_instructions += do_media_manager
        combined_system_instructions += do_http_retrieval
        combined_system_instructions += do_ml_model
        combined_system_instructions += do_browsing
        combined_system_instructions += do_analyze_code
        combined_system_instructions += do_reasoning
        combined_system_instructions += do_function
        combined_system_instructions += do_api
        combined_system_instructions += do_script
        combined_system_instructions += do_generate_image
        combined_system_instructions += do_edit_image
        combined_system_instructions += do_dream_image
        combined_system_instructions += do_audio
        combined_system_instructions += do_generate_video
        combined_system_instructions += smart_contract_func_call
        combined_system_instructions += dashboard_statistics
        combined_system_instructions += hadron_node_query
        combined_system_instructions += metakanban_query
        combined_system_instructions += metatempo_query
        combined_system_instructions += orchestration_trigger
        combined_system_instructions += scheduled_job_logs
        combined_system_instructions += triggered_job_logs
        combined_system_instructions += smart_contract_gen

        return combined_system_instructions

    @staticmethod
    def _build_tool_call_instructions_prompts(assistant):

        instructions = (
            build_generic_instructions_tool_call_prompt(
                assistant
            )
        )

        sql = (build_tool_prompt__execute_sql_query())
        nosql = (build_tool_prompt__execute_nosql_query())
        vector_store = build_tool_prompt__query_vector_store()
        codebase = build_tool_prompt__execute_codebase_query()
        intra_memory = build_tool_prompt__intra_context_memory()
        ssh_file_system = build_tool_prompt__execute_ssh_file_system_command()
        media_manager = build_tool_prompt__media_manager_query()
        http_retrieval = build_tool_prompt__retrieval_via_http_client()
        infer_ml = build_tool_prompt__infer_with_machine_learning()
        browsing = build_tool_prompt__browsing()
        analyze_code = build_tool_prompt__analyze_code()
        reasoning = build_tool_prompt__reasoning()
        functions = build_tool_prompt__execute_code()
        apis = build_tool_prompt__execute_restful_api()
        scripts = build_tool_prompt__execute_bash_script()
        generate_image = build_tool_prompt__generate_image()
        edit_image = build_tool_prompt__edit_image()
        dream_image = build_tool_prompt__dream_image()
        process_audio = build_tool_prompt__execute_audio()
        generate_video = build_tool_prompt__generate_video(
            assistant_id=assistant.id
        )
        smart_contract_func_call = build_tool_prompt__smart_contract_function_call()
        dashboard_statistics = build_tool_prompt__execute_dashboard_statistics_query()
        hadron_node_query = build_tool_prompt__execute_hadron_prime_node_query()
        metakanban_query = build_tool_prompt__execute_metakanban_query()
        metatempo_query = build_tool_prompt__execute_metatempo_query()
        orchestration_trigger = build_tool_prompt__execute_orchestration_trigger()
        scheduled_job_logs = build_tool_prompt__execute_scheduled_job_logs_query()
        triggered_job_logs = build_tool_prompt__execute_triggered_job_logs_query()
        smart_contract_gen = build_tool_prompt__execute_smart_contract_generation_query()

        return (
            process_audio,
            browsing,
            codebase,
            analyze_code,
            apis,
            functions,
            scripts,
            ssh_file_system,
            generate_image,
            edit_image,
            dream_image,
            vector_store,
            infer_ml,
            reasoning,
            sql,
            nosql,
            media_manager,
            instructions,
            http_retrieval,
            intra_memory,
            generate_video,
            smart_contract_func_call,
            dashboard_statistics,
            hadron_node_query,
            metakanban_query,
            metatempo_query,
            orchestration_trigger,
            scheduled_job_logs,
            triggered_job_logs,
            smart_contract_gen
        )

    @staticmethod
    def _build_flexible_modalities_prompts(assistant):

        functions = build_functions_multi_modality_prompt(assistant)
        apis = build_apis_multi_modality_prompt(assistant)
        scripts = build_scripts_multi_modality_prompt(assistant)

        return apis, functions, scripts

    @staticmethod
    def _build_information_feeds_prompt(assistant):

        sql_feed = build_sql_data_source_prompt(assistant)
        nosql_feed = build_nosql_data_source_prompt(assistant)
        vector_store_feed = build_vector_store_data_source_prompt(assistant)
        codebase_feed = build_code_base_data_source_prompt(assistant)
        ssh_system_feed = build_file_system_data_source_prompt(assistant)
        media_manager_feed = build_media_manager_data_source_prompt(assistant)
        ml_feed = build_ml_models_data_source_prompt(assistant)
        browsing_feed = build_browsing_data_source_prompt(assistant)
        smart_contract_feed = build_smart_contracts_data_source_prompt(assistant)
        hadron_prime_node_feed = build_hadron_prime_node_to_assistant_data_source_prompt(assistant)
        metakanban_feed = build_metakanban_to_assistant_data_source_prompt(assistant)
        metatempo_feed = build_metatempo_to_assistant_data_source_prompt(assistant)
        orchestration_trigger_feed = build_orchestration_to_assistant_data_source_prompt(assistant)

        return (
            browsing_feed,
            codebase_feed,
            ssh_system_feed,
            vector_store_feed,
            media_manager_feed,
            ml_feed,
            sql_feed,
            nosql_feed,
            smart_contract_feed,
            hadron_prime_node_feed,
            metakanban_feed,
            metatempo_feed,
            orchestration_trigger_feed
        )

    @staticmethod
    def _build_foundation_prompts(
        agent_nickname,
        agent_personality_tone,
        assistant,
        chat,
        output_language,
        target_audience,
        templated_response, user
    ):

        generic = build_internal_principles_prompt()
        agent_nickname = build_agent_nickname_prompt(
            name=agent_nickname,
            chat_name=chat.chat_name
        )
        main_instructions = build_system_internal_instructions_prompt(
            assistant=assistant
        )
        templated_response = build_templated_response_prompt(
            response_template=templated_response
        )
        target_audience = build_target_audience_prompt(
            audience=target_audience
        )
        tone = build_agent_personality_prompt(
            tone=agent_personality_tone
        )
        projects_teams_prompt = build_agent_related_project_items_prompt(
            agent=assistant
        )
        comm_language = build_communication_language_prompt(
            response_language=output_language
        )
        user_info = build_user_tenant_prompt(
            user=user
        )
        standard_memory = build_standard_memory_prompt(
            assistant=assistant, user=user
        )
        technical_dict = build_technical_dictionary_prompt(
            glossary=assistant.glossary
        )
        spatial_awareness = ""

        if assistant.time_awareness and assistant.place_awareness:
            spatial_awareness = build_spatial_awareness_prompt(
                user=user
            )

        intra_memory = build_intra_context_memory_prompt(
            assistant=assistant
        )

        return (
            generic,
            target_audience,
            intra_memory,
            technical_dict,
            main_instructions,
            standard_memory,
            agent_nickname,
            spatial_awareness,
            projects_teams_prompt,
            comm_language,
            templated_response,
            tone,
            user_info
        )

    @staticmethod
    def build_lean(
        assistant_name: str,
        instructions: str,
        audience: str = "standard",
        tone: str = "formal",
        language: str = "en",
        chat_name: str = "Default"
    ):

        ##############################################################################################################
        # DASHBOARD: STATISTICS ASSISTANT (THIS ASSISTANT HAS NO OTHER PURPOSE THAN DASHBOARD ANALYSIS)
        ##############################################################################################################

        agent_nickname = assistant_name
        comm_language = language
        generic = build_internal_principles_prompt()
        agent_nickname_prompt = build_agent_nickname_prompt(
            name=agent_nickname,
            chat_name=chat_name
        )

        main_instructions = instructions
        audience_prompt = build_target_audience_prompt(
            audience=audience
        )
        tone_prompt = build_agent_personality_prompt(
            tone=tone
        )
        output_language = build_communication_language_prompt(
            response_language=comm_language
        )

        sql_feed = build_lean_sql_data_source_prompt()
        nosql_feed = build_lean_nosql_data_source_prompt()
        vector_store_feed = build_lean_vector_store_data_source_prompt()
        codebase_feed = build_lean_code_base_data_source_prompt()
        ssh_feed = build_lean_file_system_data_source_prompt()
        media_manager_feed = build_lean_media_manager_data_source_prompt()
        ml_feed = build_lean_ml_models_data_source_prompt()
        browsing_feed = build_lean_browsing_data_source_prompt()
        smart_contract_feed = build_lean_smart_contracts_data_source_prompt()
        hadron_prime_node_feed = build_lean_hadron_prime_node_to_assistant_data_source_prompt()
        metakanban_feed = build_lean_metakanban_to_assistant_data_source_prompt()
        metatempo_feed = build_lean_metatempo_to_assistant_data_source_prompt()
        orchestration_trigger_feed = build_lean_orchestration_to_assistant_data_source_prompt()

        function_modality = build_lean_functions_multi_modality_prompt()
        api_modality = build_lean_apis_multi_modality_prompt()
        script_modality = build_lean_scripts_multi_modality_prompt()

        do_instructions = (build_lean_structured_tool_usage_instructions_prompt())
        do_sql_query = (build_tool_prompt__execute_sql_query())
        do_vector_store = build_tool_prompt__query_vector_store()
        do_codebase = build_tool_prompt__execute_codebase_query()
        do_intra_memory = build_tool_prompt__intra_context_memory()
        do_ssh_system = build_tool_prompt__execute_ssh_file_system_command()
        do_media_manager = build_tool_prompt__media_manager_query()
        do_http_retrieval = build_tool_prompt__retrieval_via_http_client()
        do_ml = build_tool_prompt__infer_with_machine_learning()
        do_browsing = build_tool_prompt__browsing()
        do_analyze_code = build_tool_prompt__analyze_code()
        do_function = build_tool_prompt__execute_code()
        do_api = build_tool_prompt__execute_restful_api()
        do_script = build_tool_prompt__execute_bash_script()
        do_generate_image = build_tool_prompt__generate_image()
        do_edit_image = build_tool_prompt__edit_image()
        do_dream_image = build_tool_prompt__dream_image()
        do_audio = build_tool_prompt__execute_audio()
        do_generate_video = build_lean_tool_prompt__generate_video()
        do_smart_contract = build_tool_prompt__smart_contract_function_call()
        do_dashboard_statistics = build_tool_prompt__execute_dashboard_statistics_query()
        do_hadron_node_query = build_tool_prompt__execute_hadron_prime_node_query()
        do_metakanban_query = build_tool_prompt__execute_metakanban_query()
        do_metatempo_query = build_tool_prompt__execute_metatempo_query()
        do_orchestration_trigger = build_tool_prompt__execute_orchestration_trigger()
        do_scheduled_job_logs = build_tool_prompt__execute_scheduled_job_logs_query()
        do_triggered_job_logs = build_tool_prompt__execute_triggered_job_logs_query()
        do_smart_contract_gen = build_tool_prompt__execute_smart_contract_generation_query()

        # Core Instructions
        merged_prompt = generic
        merged_prompt += agent_nickname_prompt
        merged_prompt += main_instructions
        merged_prompt += audience_prompt
        merged_prompt += tone_prompt
        merged_prompt += output_language

        # Data Feeds
        merged_prompt += sql_feed
        merged_prompt += nosql_feed
        merged_prompt += vector_store_feed
        merged_prompt += codebase_feed
        merged_prompt += ssh_feed
        merged_prompt += media_manager_feed
        merged_prompt += ml_feed
        merged_prompt += browsing_feed
        merged_prompt += smart_contract_feed
        merged_prompt += hadron_prime_node_feed
        merged_prompt += metakanban_feed
        merged_prompt += metatempo_feed
        merged_prompt += orchestration_trigger_feed

        # Executors
        merged_prompt += function_modality
        merged_prompt += api_modality
        merged_prompt += script_modality
        merged_prompt += do_instructions
        merged_prompt += do_sql_query
        merged_prompt += do_vector_store
        merged_prompt += do_codebase
        merged_prompt += do_intra_memory
        merged_prompt += do_ssh_system
        merged_prompt += do_media_manager
        merged_prompt += do_http_retrieval
        merged_prompt += do_ml
        merged_prompt += do_browsing
        merged_prompt += do_analyze_code
        merged_prompt += do_function
        merged_prompt += do_api
        merged_prompt += do_script
        merged_prompt += do_generate_image
        merged_prompt += do_edit_image
        merged_prompt += do_dream_image
        merged_prompt += do_audio
        merged_prompt += do_generate_video
        merged_prompt += do_smart_contract
        merged_prompt += do_dashboard_statistics
        merged_prompt += do_hadron_node_query
        merged_prompt += do_metakanban_query
        merged_prompt += do_metatempo_query
        merged_prompt += do_orchestration_trigger
        merged_prompt += do_scheduled_job_logs
        merged_prompt += do_triggered_job_logs
        merged_prompt += do_smart_contract_gen
        prompt = {"role": "system", "content": merged_prompt}
        return prompt

    @staticmethod
    def build_semantor(
        assistant_name: str,
        instructions: str,
        temporary_sources: dict,
        audience: str = "standard",
        tone: str = "formal",
        language: str = "en",
        chat_name: str = "Default",
    ):
        ##############################################################################################################
        # SEMANTOR ASSISTANT
        ##############################################################################################################
        agent_nickname = assistant_name
        comm_language = language
        generic = build_internal_principles_prompt()
        agent_nickname_prompt = build_agent_nickname_prompt(
            name=agent_nickname,
            chat_name=chat_name
        )
        main_instructions = instructions
        audience_prompt = build_target_audience_prompt(
            audience=audience
        )
        tone_prompt = build_agent_personality_prompt(
            tone=tone
        )
        output_language = build_communication_language_prompt(
            response_language=comm_language
        )

        sql_feed = build_semantor_sql_data_source_prompt(
            temporary_sources=temporary_sources
        )
        nosql_feed = build_semantor_nosql_data_source_prompt(
            temporary_sources=temporary_sources
        )
        vector_store_feed = build_semantor_vector_store_data_source_prompt(
            temporary_sources=temporary_sources
        )
        codebase_feed = build_semantor_code_base_data_source_prompt(
            temporary_sources=temporary_sources
        )
        ssh_feed = build_semantor_file_system_data_source_prompt(
            temporary_sources=temporary_sources
        )
        media_manager_feed = build_semantor_media_manager_data_source_prompt(
            temporary_sources=temporary_sources
        )
        ml_feed = build_semantor_ml_models_data_source_prompt(
            temporary_sources=temporary_sources
        )
        browsing_feed = build_semantor_browsing_data_source_prompt(
            temporary_sources=temporary_sources
        )
        hadron_prime_node_feed = build_semantor_hadron_prime_node_to_assistant_data_source_prompt(
            temporary_sources=temporary_sources
        )
        metakanban_feed = build_semantor_metakanban_to_assistant_data_source_prompt(
            temporary_sources=temporary_sources
        )
        metatempo_feed = build_semantor_metatempo_to_assistant_data_source_prompt(
            temporary_sources=temporary_sources
        )
        orchestration_trigger_feed = build_semantor_orchestration_to_assistant_data_source_prompt(
            temporary_sources=temporary_sources
        )

        ##############################

        function_modality = build_semantor_functions_multi_modality_prompt(
            temporary_sources=temporary_sources
        )
        api_modality = build_semantor_apis_multi_modality_prompt(
            temporary_sources=temporary_sources
        )
        script_modality = build_semantor_scripts_multi_modality_prompt(
            temporary_sources=temporary_sources
        )

        do_instructions = (build_lean_structured_tool_usage_instructions_prompt())
        do_sql_query = (build_tool_prompt__execute_sql_query())
        do_vector_store = build_tool_prompt__query_vector_store()
        do_codebase = build_tool_prompt__execute_codebase_query()
        do_intra_memory = build_tool_prompt__intra_context_memory()
        do_ssh_system = build_tool_prompt__execute_ssh_file_system_command()
        do_media_manager = build_tool_prompt__media_manager_query()
        do_http_retrieval = build_tool_prompt__retrieval_via_http_client()
        do_ml = build_tool_prompt__infer_with_machine_learning()
        do_browsing = build_tool_prompt__browsing()
        do_analyze_code = build_tool_prompt__analyze_code()
        do_function = build_tool_prompt__execute_code()
        do_api = build_tool_prompt__execute_restful_api()
        do_script = build_tool_prompt__execute_bash_script()
        do_generate_image = build_tool_prompt__generate_image()
        do_edit_image = build_tool_prompt__edit_image()
        do_dream_image = build_tool_prompt__dream_image()
        do_audio = build_tool_prompt__execute_audio()
        do_generate_video = build_lean_tool_prompt__generate_video()
        do_smart_contract = build_tool_prompt__smart_contract_function_call()
        do_dashboard_statistics = build_tool_prompt__execute_dashboard_statistics_query()
        do_hadron_node_query = build_tool_prompt__execute_hadron_prime_node_query()
        do_metakanban_query = build_tool_prompt__execute_metakanban_query()
        do_metatempo_query = build_tool_prompt__execute_metatempo_query()
        do_orchestration_trigger = build_tool_prompt__execute_orchestration_trigger()
        do_scheduled_job_logs = build_tool_prompt__execute_scheduled_job_logs_query()
        do_triggered_job_logs = build_tool_prompt__execute_triggered_job_logs_query()
        do_smart_contract_gen = build_tool_prompt__execute_smart_contract_generation_query()

        # Core Instructions
        merged_prompt = generic
        merged_prompt += agent_nickname_prompt
        merged_prompt += main_instructions
        merged_prompt += audience_prompt
        merged_prompt += tone_prompt
        merged_prompt += output_language

        # Data Feeds
        merged_prompt += sql_feed
        merged_prompt += nosql_feed
        merged_prompt += vector_store_feed
        merged_prompt += codebase_feed
        merged_prompt += ssh_feed
        merged_prompt += media_manager_feed
        merged_prompt += ml_feed
        merged_prompt += browsing_feed
        merged_prompt += hadron_prime_node_feed
        merged_prompt += metakanban_feed
        merged_prompt += metatempo_feed
        merged_prompt += orchestration_trigger_feed

        # Executors
        merged_prompt += function_modality
        merged_prompt += api_modality
        merged_prompt += script_modality
        merged_prompt += do_instructions
        merged_prompt += do_sql_query
        merged_prompt += do_vector_store
        merged_prompt += do_codebase
        merged_prompt += do_intra_memory
        merged_prompt += do_ssh_system
        merged_prompt += do_media_manager
        merged_prompt += do_http_retrieval
        merged_prompt += do_ml
        merged_prompt += do_browsing
        merged_prompt += do_analyze_code
        merged_prompt += do_function
        merged_prompt += do_api
        merged_prompt += do_script
        merged_prompt += do_generate_image
        merged_prompt += do_edit_image
        merged_prompt += do_dream_image
        merged_prompt += do_audio
        merged_prompt += do_generate_video
        merged_prompt += do_smart_contract
        merged_prompt += do_dashboard_statistics
        merged_prompt += do_hadron_node_query
        merged_prompt += do_metakanban_query
        merged_prompt += do_metatempo_query
        merged_prompt += do_orchestration_trigger
        merged_prompt += do_scheduled_job_logs
        merged_prompt += do_triggered_job_logs
        merged_prompt += do_smart_contract_gen
        prompt = {"role": "system", "content": merged_prompt}
        return prompt

    @staticmethod
    def build_leanmod_system_prompts(
        chat: MultimodalLeanChat,
        lean_assistant: LeanAssistant,
        user: User,
        role: str,
        fermion__is_fermion_supervised=False,
        fermion__export_type=None,
        fermion__endpoint=None
    ):

        from apps.core.generative_ai.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps.core.generative_ai.utils import ChatRoles

        try:
            combined_system_instructions = SystemPromptFactoryBuilder.prepare_leanmod_system_prompts(
                chat,
                lean_assistant,
                user,
                fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                fermion__export_type=fermion__export_type,
                fermion__endpoint=fermion__endpoint
            )

            prompt = {
                "role": role,
                "content": combined_system_instructions
            }

            try:

                tx = LLMTransaction.objects.create(
                    organization=lean_assistant.organization,
                    model=lean_assistant.llm_model,
                    responsible_user=user,
                    responsible_assistant=None,
                    encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                    transaction_context_content=json.dumps(combined_system_instructions),
                    llm_cost=0,
                    internal_service_cost=0,
                    tax_cost=0,
                    total_cost=0,
                    total_billable_cost=0,
                    transaction_type=ChatRoles.SYSTEM,
                    transaction_source=chat.chat_source
                )

                chat.transactions.add(tx)
                chat.save()
            except Exception as e:
                print("Error saving Leanmod system prompts transaction: %s" % e)

        except Exception as e:
            print("Error building Leanmod system prompts: %s" % e)
            return {"role": role, "content": "Unexpected error building Leanmod system prompts: %s" % e}

        return prompt

    @staticmethod
    def prepare_leanmod_system_prompts(
        chat,
        lean_assistant,
        user,
        fermion__is_fermion_supervised=False,
        fermion__export_type=None,
        fermion__endpoint=None
    ):

        agent_nickname = lean_assistant.name
        generic = build_structured_primary_guidelines_leanmod()

        transmit_websocket_log(
            f"""📜 Gathered primary instructions for operations.""",
            chat_id=chat.id,
            fermion__is_fermion_supervised=fermion__is_fermion_supervised,
            fermion__export_type=fermion__export_type,
            fermion__endpoint=fermion__endpoint
        )

        agent_nickname = build_structured_name_prompt_leanmod(
            assistant_name=agent_nickname,
            chat_name=chat.chat_name
        )
        instructions = build_structured_instructions_prompt_leanmod(
            assistant=lean_assistant
        )
        user_info = build_structured_user_information_prompt_leanmod(
            user=user
        )

        transmit_websocket_log(
            f"""👤 Analyzed user requirements and expectations.""",
            chat_id=chat.id,
            fermion__is_fermion_supervised=fermion__is_fermion_supervised,
            fermion__export_type=fermion__export_type,
            fermion__endpoint=fermion__endpoint
        )

        spatial_awareness = build_structured_place_and_time_prompt_leanmod(
            user=user
        )

        transmit_websocket_log(
            f"""🌌 Understanding the current spatial configuration and time.""",
            chat_id=chat.id,
            fermion__is_fermion_supervised=fermion__is_fermion_supervised,
            fermion__export_type=fermion__export_type,
            fermion__endpoint=fermion__endpoint
        )

        expert_network = build_expert_networks_multi_modality_prompt_leanmod(
            lean_assistant=lean_assistant
        )

        transmit_websocket_log(
            f"""🌐 Analyzing Semantor network to find information about other assistants.""",
            chat_id=chat.id,
            fermion__is_fermion_supervised=fermion__is_fermion_supervised,
            fermion__export_type=fermion__export_type,
            fermion__endpoint=fermion__endpoint
        )

        tool_instructions = build_structured_tool_usage_instructions_prompt_leanmod()
        do_expert_network = build_structured_tool_prompt__expert_network_query_execution_leanmod()
        search_semantor = build_structured_tool_prompt__semantor_search_execution_leanmod()
        do_semantor = build_structured_tool_prompt__semantor_consultation_execution_leanmod()
        do_intra_memory_search = build_tool_prompt__leanmod_context_memory()

        transmit_websocket_log(
            f"""⚒️ Thinking for communication strategies for the available tools.""",
            chat_id=chat.id,
            fermion__is_fermion_supervised=fermion__is_fermion_supervised,
            fermion__export_type=fermion__export_type,
            fermion__endpoint=fermion__endpoint
        )

        combined_system_instructions = generic
        combined_system_instructions += agent_nickname
        combined_system_instructions += instructions
        combined_system_instructions += user_info
        combined_system_instructions += spatial_awareness
        combined_system_instructions += expert_network
        combined_system_instructions += tool_instructions
        combined_system_instructions += do_expert_network
        combined_system_instructions += search_semantor
        combined_system_instructions += do_semantor
        combined_system_instructions += do_intra_memory_search

        transmit_websocket_log(
            f"""🔀 Merging and organizing knowledge and capabilities.""",
            chat_id=chat.id,
            fermion__is_fermion_supervised=fermion__is_fermion_supervised,
            fermion__export_type=fermion__export_type,
            fermion__endpoint=fermion__endpoint
        )

        return combined_system_instructions

    @staticmethod
    def build_voidforger_system_prompts(
        chat: MultimodalLeanChat,
        voidforger: VoidForger,
        user: User,
        role: str,
        current_mode: str,
        fermion__is_fermion_supervised=False,
        fermion__export_type=None,
        fermion__endpoint=None
    ):

        from apps.core.generative_ai.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps.core.generative_ai.utils import ChatRoles

        combined_system_instructions = SystemPromptFactoryBuilder._prepare_voidforger_system_prompts(
            chat,
            voidforger,
            user,
            current_mode,
            fermion__is_fermion_supervised=fermion__is_fermion_supervised,
            fermion__export_type=fermion__export_type,
            fermion__endpoint=fermion__endpoint
        )

        prompt = {
            "role": role,
            "content": combined_system_instructions
        }

        tx = LLMTransaction.objects.create(
            organization=voidforger.llm_model.organization,
            model=voidforger.llm_model,
            responsible_user=user,
            responsible_assistant=None,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            transaction_context_content=combined_system_instructions,
            llm_cost=0,
            internal_service_cost=0,
            tax_cost=0,
            total_cost=0,
            total_billable_cost=0,
            transaction_type=ChatRoles.SYSTEM,
            transaction_source=chat.chat_source
        )

        chat.transactions.add(tx)
        chat.save()
        return prompt

    @staticmethod
    def _prepare_voidforger_system_prompts(
        chat,
        voidforger,
        user,
        current_mode,
        fermion__is_fermion_supervised=False,
        fermion__export_type=None,
        fermion__endpoint=None
    ):

        generic = build_structured_primary_guidelines_voidforger(
            voidforger=voidforger,
            current_mode=current_mode
        )

        transmit_websocket_log(
            f"""📜 Gathered primary instructions for operations.""",
            chat_id=chat.id,
            fermion__is_fermion_supervised=fermion__is_fermion_supervised,
            fermion__export_type=fermion__export_type,
            fermion__endpoint=fermion__endpoint
        )

        instructions = build_structured_instructions_prompt_voidforger(
            voidforger=voidforger
        )

        user_info = build_structured_user_information_prompt_voidforger(
            user=user
        )

        transmit_websocket_log(
            f"""👤 Analyzed user requirements and expectations.""",
            chat_id=chat.id,
            fermion__is_fermion_supervised=fermion__is_fermion_supervised,
            fermion__export_type=fermion__export_type,
            fermion__endpoint=fermion__endpoint
        )

        spatial_awareness = build_structured_place_and_time_prompt_voidforger(
            user=user
        )

        transmit_websocket_log(
            f"""🌌 Understanding the current spatial configuration and time.""",
            chat_id=chat.id,
            fermion__is_fermion_supervised=fermion__is_fermion_supervised,
            fermion__export_type=fermion__export_type,
            fermion__endpoint=fermion__endpoint
        )

        tone_prompt = build_agent_personality_prompt_voidforger(
            tone=voidforger.tone
        )

        transmit_websocket_log(
            f"""🫱🏿‍🫲🏻 Meditating about his own character and personality.""",
            chat_id=chat.id,
            fermion__is_fermion_supervised=fermion__is_fermion_supervised,
            fermion__export_type=fermion__export_type,
            fermion__endpoint=fermion__endpoint
        )

        output_language = build_communication_language_prompt_voidforger(
            response_language=voidforger.response_language
        )

        transmit_websocket_log(
            f"""🌐 Adjusting the language and communication parameters.""",
            chat_id=chat.id,
            fermion__is_fermion_supervised=fermion__is_fermion_supervised,
            fermion__export_type=fermion__export_type,
            fermion__endpoint=fermion__endpoint
        )

        tool_instructions = build_structured_tool_usage_instructions_prompt_voidforger()

        transmit_websocket_log(
            f"""⚒️ Checking available tools and multi-modal capabilities.""",
            chat_id=chat.id,
            fermion__is_fermion_supervised=fermion__is_fermion_supervised,
            fermion__export_type=fermion__export_type,
            fermion__endpoint=fermion__endpoint
        )

        do_old_message_search = build_structured_tool_prompt__old_message_search_execution_voidforger()

        do_action_history_log_search = build_structured_tool_prompt__action_history_log_search_voidforger()
        do_auto_execution_log_search = build_structured_tool_prompt__auto_execution_log_search_voidforger()
        do_leanmod_oracle_search = build_structured_tool_prompt__leanmod_oracle_search_voidforger()
        do_leanmod_oracle_command_order = build_structured_tool_prompt__leanmod_oracle_command_order_voidforger()

        transmit_websocket_log(
            f"""⚒️ Thinking for communication strategies for the available tools.""",
            chat_id=chat.id,
            fermion__is_fermion_supervised=fermion__is_fermion_supervised,
            fermion__export_type=fermion__export_type,
            fermion__endpoint=fermion__endpoint
        )

        combined_system_instructions = generic
        combined_system_instructions += instructions
        combined_system_instructions += user_info
        combined_system_instructions += spatial_awareness
        combined_system_instructions += tone_prompt
        combined_system_instructions += output_language

        combined_system_instructions += tool_instructions
        combined_system_instructions += do_old_message_search
        combined_system_instructions += do_action_history_log_search
        combined_system_instructions += do_auto_execution_log_search
        combined_system_instructions += do_leanmod_oracle_search
        combined_system_instructions += do_leanmod_oracle_command_order

        transmit_websocket_log(
            f"""🔀 Merging and organizing knowledge and capabilities.""",
            chat_id=chat.id,
            fermion__is_fermion_supervised=fermion__is_fermion_supervised,
            fermion__export_type=fermion__export_type,
            fermion__endpoint=fermion__endpoint
        )

        return combined_system_instructions
