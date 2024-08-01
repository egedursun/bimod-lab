
from django.contrib.auth.models import User

from apps._services.prompts.datasource.build_browser_data_source_prompt import build_browsing_data_source_prompt, \
    build_lean_browsing_data_source_prompt
from apps._services.prompts.datasource.build_file_system_data_source_prompt import build_file_system_data_source_prompt, \
    build_lean_file_system_data_source_prompt
from apps._services.prompts.datasource.build_knowledge_base_data_source_prompt import \
    build_knowledge_base_data_source_prompt, build_lean_knowledge_base_data_source_prompt
from apps._services.prompts.datasource.build_ml_models_data_source_prompt import build_ml_models_data_source_prompt, \
    build_lean_ml_models_data_source_prompt
from apps._services.prompts.datasource.build_sql_data_source_prompt import build_sql_data_source_prompt, \
    build_lean_sql_data_source_prompt
from apps._services.prompts.datasource.build_storage_data_source_prompt import build_storage_data_source_prompt, \
    build_lean_storage_data_source_prompt
from apps._services.prompts.generic.build_audience_prompt import build_structured_audience_prompt
from apps._services.prompts.generic.build_context_overflow_prompt import build_structured_context_overflow_prompt
from apps._services.prompts.generic.build_glossary_prompt import build_structured_glossary_prompt
from apps._services.prompts.generic.build_instructions_prompt import build_structured_instructions_prompt
from apps._services.prompts.generic.build_memory_prompt import build_structured_memory_prompt
from apps._services.prompts.generic.build_name_prompt import build_structured_name_prompt
from apps._services.prompts.generic.build_place_and_time_prompt import build_structured_place_and_time_prompt
from apps._services.prompts.generic.build_primary_guidelines import build_structured_primary_guidelines
from apps._services.prompts.generic.build_response_language_prompt import build_structured_response_language_prompt
from apps._services.prompts.generic.build_response_template_prompt import build_structured_response_template_prompt
from apps._services.prompts.generic.build_tone_prompt import build_structured_tone_prompt
from apps._services.prompts.generic.build_user_information_prompt import build_structured_user_information_prompt
from apps._services.prompts.multimodality.build_apis_multimodality_prompt import build_apis_multi_modality_prompt, \
    build_lean_apis_multi_modality_prompt
from apps._services.prompts.multimodality.build_functions_multimodality_prompt import \
    build_functions_multi_modality_prompt, build_lean_functions_multi_modality_prompt
from apps._services.prompts.multimodality.build_scripts_multimodality_prompt import build_scripts_multi_modality_prompt, \
    build_lean_scripts_multi_modality_prompt
from apps._services.prompts.tools.build_tool_usage_instructions_prompt import \
    build_structured_tool_usage_instructions_prompt, build_lean_structured_tool_usage_instructions_prompt
from apps._services.prompts.tools.tool_prompts.build_browsing_executor_tool_prompt import \
    build_structured_tool_prompt__browsing_executor
from apps._services.prompts.tools.tool_prompts.build_code_interpreter_tool_prompt import \
    build_structured_tool_prompt__code_interpreter
from apps._services.prompts.tools.tool_prompts.build_custom_api_execution_tool_prompt import \
    build_structured_tool_prompt__custom_api_execution
from apps._services.prompts.tools.tool_prompts.build_custom_code_execution_tool_prompt import \
    build_structured_tool_prompt__custom_code_execution
from apps._services.prompts.tools.tool_prompts.build_custom_script_execution_tool_prompt import \
    build_structured_tool_prompt__custom_script_content_retrieval
from apps._services.prompts.tools.tool_prompts.build_file_system_command_execution_tool_prompt import \
    build_structured_tool_prompt__file_system_command_execution
from apps._services.prompts.tools.tool_prompts.build_image_generation_tool_prompt import \
    build_structured_tool_prompt__image_generator
from apps._services.prompts.tools.tool_prompts.build_image_modification_tool_prompt import \
    build_structured_tool_prompt__image_modification
from apps._services.prompts.tools.tool_prompts.build_image_variation_tool_prompt import \
    build_structured_tool_prompt__image_variation
from apps._services.prompts.tools.tool_prompts.build_knowledge_base_query_execution_tool_prompt import \
    build_structured_tool_prompt__knowledge_base_query_execution
from apps._services.prompts.tools.tool_prompts.build_nosql_query_execution_tool_prompt import \
    build_structured_tool_prompt__nosql_query_execution
from apps._services.prompts.tools.tool_prompts.build_predict_ml_models_execution_tool_prompt import \
    build_structured_tool_prompt__predict_with_ml_model_execution
from apps._services.prompts.tools.tool_prompts.build_sql_query_execution_tool_prompt import \
    build_structured_tool_prompt__sql_query_execution
from apps._services.prompts.tools.tool_prompts.build_storage_query_execution_tool_prompt import \
    build_structured_tool_prompt__media_storage_query_execution
from apps._services.prompts.tools.tool_prompts.build_url_file_downloader_tool_prompt import \
    build_structured_tool_prompt__url_file_downloader
from apps._services.prompts.tools.tool_prompts.build_vectorized_context_history_query_execution_tool_prompt import \
    build_structured_tool_prompt__vectorized_context_history__query_execution_tool_prompt
from apps.assistants.models import Assistant
from apps.llm_transaction.models import LLMTransaction
from apps.multimodal_chat.models import MultimodalChat


class PromptBuilder:

    @staticmethod
    def build(chat: MultimodalChat, assistant: Assistant, user: User, role: str):
        from apps._services.llms.openai import GPT_DEFAULT_ENCODING_ENGINE, ChatRoles
        name = assistant.name
        response_template = assistant.response_template
        audience = assistant.audience
        tone = assistant.tone
        response_language = assistant.response_language

        ##################################################
        # GENERIC PROMPTS
        primary_guidelines_prompt = build_structured_primary_guidelines()
        structured_name_prompt = build_structured_name_prompt(name, chat.chat_name)
        structured_instructions_prompt = build_structured_instructions_prompt(assistant)
        structured_response_template_prompt = build_structured_response_template_prompt(response_template)
        structured_audience_prompt = build_structured_audience_prompt(audience)
        structured_tone_prompt = build_structured_tone_prompt(tone)
        structured_response_language_prompt = build_structured_response_language_prompt(response_language)
        structured_user_information_prompt = build_structured_user_information_prompt(user)
        structured_memory_prompt = build_structured_memory_prompt(assistant, user)
        structured_glossary_prompt = build_structured_glossary_prompt(assistant.glossary)
        structured_place_and_time_prompt = ""
        if assistant.time_awareness and assistant.place_awareness:
            structured_place_and_time_prompt = build_structured_place_and_time_prompt(assistant, user)
        structured_context_overflow_prompt = build_structured_context_overflow_prompt(assistant)
        ##################################################
        # DATASOURCE PROMPTS
        structured_sql_datasource_prompt = build_sql_data_source_prompt(assistant)
        structured_knowledge_base_datasource_prompt = build_knowledge_base_data_source_prompt(assistant)
        structured_file_system_prompt = build_file_system_data_source_prompt(assistant)
        structured_media_storage_prompt = build_storage_data_source_prompt(assistant)
        structured_ml_model_prompt = build_ml_models_data_source_prompt(assistant)
        structured_browsing_datasource_prompt = build_browsing_data_source_prompt(assistant)
        ##################################################
        # MULTI MODALITY PROMPTS
        structured_functions_prompt = build_functions_multi_modality_prompt(assistant)
        structured_apis_prompt = build_apis_multi_modality_prompt(assistant)
        structured_scripts_prompt = build_scripts_multi_modality_prompt(assistant)
        ##################################################
        # TOOL PROMPTS
        structured_tool_usage_instructions_prompt = (build_structured_tool_usage_instructions_prompt(assistant))
        structured_sql_query_execution_tool_prompt = (build_structured_tool_prompt__sql_query_execution())
        _ = (build_structured_tool_prompt__nosql_query_execution())
        structured_knowledge_base_query_execution_tool_prompt = build_structured_tool_prompt__knowledge_base_query_execution()
        structured_vectorized_context_history_query_execution_tool_prompt = build_structured_tool_prompt__vectorized_context_history__query_execution_tool_prompt()
        structured_file_system_command_execution_tool_prompt = build_structured_tool_prompt__file_system_command_execution()
        structured_storage_query_execution_tool_prompt = build_structured_tool_prompt__media_storage_query_execution()
        structured_url_file_downloader_tool_prompt = build_structured_tool_prompt__url_file_downloader()
        structured_predict_with_ml_model_execution_tool_prompt = build_structured_tool_prompt__predict_with_ml_model_execution()
        structured_browsing_execution_tool_prompt = build_structured_tool_prompt__browsing_executor()
        structured_code_interpreter_tool_prompt = build_structured_tool_prompt__code_interpreter()
        structured_custom_function_execution_tool_prompt = build_structured_tool_prompt__custom_code_execution()
        structured_custom_api_execution_tool_prompt = build_structured_tool_prompt__custom_api_execution()
        structured_custom_script_content_retrieval_tool_prompt = build_structured_tool_prompt__custom_script_content_retrieval()
        structured_image_generation_tool_prompt = build_structured_tool_prompt__image_generator()
        structured_image_modification_tool_prompt = build_structured_tool_prompt__image_modification()
        structured_image_variation_tool_prompt = build_structured_tool_prompt__image_variation()
        ##################################################

        # Combine the prompts
        merged_prompt = primary_guidelines_prompt
        merged_prompt += structured_name_prompt
        merged_prompt += structured_instructions_prompt
        merged_prompt += structured_response_template_prompt
        merged_prompt += structured_audience_prompt
        merged_prompt += structured_tone_prompt
        merged_prompt += structured_response_language_prompt
        merged_prompt += structured_user_information_prompt
        merged_prompt += structured_memory_prompt
        merged_prompt += structured_glossary_prompt
        merged_prompt += structured_place_and_time_prompt
        merged_prompt += structured_context_overflow_prompt
        ##################################################
        # DATASOURCE PROMPTS
        merged_prompt += structured_sql_datasource_prompt
        merged_prompt += structured_knowledge_base_datasource_prompt
        merged_prompt += structured_file_system_prompt
        merged_prompt += structured_media_storage_prompt
        merged_prompt += structured_ml_model_prompt
        merged_prompt += structured_browsing_datasource_prompt
        ##################################################
        # MULTI MODALITY PROMPTS
        merged_prompt += structured_functions_prompt
        merged_prompt += structured_apis_prompt
        merged_prompt += structured_scripts_prompt
        ##################################################
        # GENERIC TOOL PROMPT
        merged_prompt += structured_tool_usage_instructions_prompt
        ##################################################
        # SPECIALIZED TOOL PROMPTS
        merged_prompt += structured_sql_query_execution_tool_prompt
        merged_prompt += structured_knowledge_base_query_execution_tool_prompt
        merged_prompt += structured_vectorized_context_history_query_execution_tool_prompt
        merged_prompt += structured_file_system_command_execution_tool_prompt
        merged_prompt += structured_storage_query_execution_tool_prompt
        merged_prompt += structured_url_file_downloader_tool_prompt
        merged_prompt += structured_predict_with_ml_model_execution_tool_prompt
        merged_prompt += structured_browsing_execution_tool_prompt
        merged_prompt += structured_code_interpreter_tool_prompt
        merged_prompt += structured_custom_function_execution_tool_prompt
        merged_prompt += structured_custom_api_execution_tool_prompt
        merged_prompt += structured_custom_script_content_retrieval_tool_prompt
        merged_prompt += structured_image_generation_tool_prompt
        merged_prompt += structured_image_modification_tool_prompt
        merged_prompt += structured_image_variation_tool_prompt
        ##################################################

        # Build the dictionary with the role
        prompt = {
            "role": role,
            "content": merged_prompt
        }

        # Create the transaction for the system prompt
        transaction = LLMTransaction.objects.create(
            organization=assistant.organization,
            model=assistant.llm_model,
            responsible_user=user,
            responsible_assistant=assistant,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            transaction_context_content=merged_prompt,
            llm_cost=0,
            internal_service_cost=0,
            tax_cost=0,
            total_cost=0,
            total_billable_cost=0,
            transaction_type=ChatRoles.SYSTEM,
            transaction_source=chat.chat_source
        )
        # Add the transaction to the chat
        chat.transactions.add(transaction)
        chat.save()

        return prompt

    @staticmethod
    def build_lean(assistant_name: str, instructions:str, audience:str = "standard", tone:str = "formal", language:str = "en",
                   chat_name: str = "Default"):
        name = assistant_name
        response_language = language

        ##################################################
        # GENERIC PROMPTS
        primary_guidelines_prompt = build_structured_primary_guidelines()
        structured_name_prompt = build_structured_name_prompt(name, chat_name)
        structured_instructions_prompt = instructions
        structured_audience_prompt = build_structured_audience_prompt(audience)
        structured_tone_prompt = build_structured_tone_prompt(tone)
        structured_response_language_prompt = build_structured_response_language_prompt(response_language)
        ##################################################
        # DATASOURCE PROMPTS
        structured_sql_datasource_prompt = build_lean_sql_data_source_prompt()
        structured_knowledge_base_datasource_prompt = build_lean_knowledge_base_data_source_prompt()
        structured_file_system_prompt = build_lean_file_system_data_source_prompt()
        structured_media_storage_prompt = build_lean_storage_data_source_prompt()
        structured_ml_model_prompt = build_lean_ml_models_data_source_prompt()
        structured_browsing_datasource_prompt = build_lean_browsing_data_source_prompt()
        ##################################################
        # MULTI MODALITY PROMPTS
        structured_functions_prompt = build_lean_functions_multi_modality_prompt()
        structured_apis_prompt = build_lean_apis_multi_modality_prompt()
        structured_scripts_prompt = build_lean_scripts_multi_modality_prompt()
        ##################################################
        # TOOL PROMPTS
        structured_tool_usage_instructions_prompt = (
            build_lean_structured_tool_usage_instructions_prompt()
        )
        structured_sql_query_execution_tool_prompt = (
            build_structured_tool_prompt__sql_query_execution()
        )
        _ = (
            build_structured_tool_prompt__nosql_query_execution()
        )
        structured_knowledge_base_query_execution_tool_prompt = build_structured_tool_prompt__knowledge_base_query_execution()
        structured_vectorized_context_history_query_execution_tool_prompt = build_structured_tool_prompt__vectorized_context_history__query_execution_tool_prompt()
        structured_file_system_command_execution_tool_prompt = build_structured_tool_prompt__file_system_command_execution()
        structured_storage_query_execution_tool_prompt = build_structured_tool_prompt__media_storage_query_execution()
        structured_url_file_downloader_tool_prompt = build_structured_tool_prompt__url_file_downloader()
        structured_predict_with_ml_model_execution_tool_prompt = build_structured_tool_prompt__predict_with_ml_model_execution()
        structured_browsing_execution_tool_prompt = build_structured_tool_prompt__browsing_executor()
        structured_code_interpreter_tool_prompt = build_structured_tool_prompt__code_interpreter()
        structured_custom_function_execution_tool_prompt = build_structured_tool_prompt__custom_code_execution()
        structured_custom_api_execution_tool_prompt = build_structured_tool_prompt__custom_api_execution()
        structured_custom_script_content_retrieval_tool_prompt = build_structured_tool_prompt__custom_script_content_retrieval()
        structured_image_generation_tool_prompt = build_structured_tool_prompt__image_generator()
        structured_image_modification_tool_prompt = build_structured_tool_prompt__image_modification()
        structured_image_variation_tool_prompt = build_structured_tool_prompt__image_variation()
        ##################################################

        # Combine the prompts
        merged_prompt = primary_guidelines_prompt
        merged_prompt += structured_name_prompt
        merged_prompt += structured_instructions_prompt
        merged_prompt += structured_audience_prompt
        merged_prompt += structured_tone_prompt
        merged_prompt += structured_response_language_prompt
        ##################################################
        # DATASOURCE PROMPTS
        merged_prompt += structured_sql_datasource_prompt
        merged_prompt += structured_knowledge_base_datasource_prompt
        merged_prompt += structured_file_system_prompt
        merged_prompt += structured_media_storage_prompt
        merged_prompt += structured_ml_model_prompt
        merged_prompt += structured_browsing_datasource_prompt
        ##################################################
        # MULTI MODALITY PROMPTS
        merged_prompt += structured_functions_prompt
        merged_prompt += structured_apis_prompt
        merged_prompt += structured_scripts_prompt
        ##################################################
        # GENERIC TOOL PROMPT
        merged_prompt += structured_tool_usage_instructions_prompt
        ##################################################
        # SPECIALIZED TOOL PROMPTS
        merged_prompt += structured_sql_query_execution_tool_prompt
        merged_prompt += structured_knowledge_base_query_execution_tool_prompt
        merged_prompt += structured_vectorized_context_history_query_execution_tool_prompt
        merged_prompt += structured_file_system_command_execution_tool_prompt
        merged_prompt += structured_storage_query_execution_tool_prompt
        merged_prompt += structured_url_file_downloader_tool_prompt
        merged_prompt += structured_predict_with_ml_model_execution_tool_prompt
        merged_prompt += structured_browsing_execution_tool_prompt
        merged_prompt += structured_code_interpreter_tool_prompt
        merged_prompt += structured_custom_function_execution_tool_prompt
        merged_prompt += structured_custom_api_execution_tool_prompt
        merged_prompt += structured_custom_script_content_retrieval_tool_prompt
        merged_prompt += structured_image_generation_tool_prompt
        merged_prompt += structured_image_modification_tool_prompt
        merged_prompt += structured_image_variation_tool_prompt
        ##################################################
        # Build the dictionary with the role
        prompt = {
            "role": "system",
            "content": merged_prompt
        }
        return prompt
