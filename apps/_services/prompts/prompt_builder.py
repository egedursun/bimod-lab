
from django.contrib.auth.models import User

from apps._services.prompts.datasource.build_file_system_datasource_prompt import build_file_system_datasource_prompt
from apps._services.prompts.datasource.build_knowledge_base_datasource_prompt import \
    build_knowledge_base_datasource_prompt
from apps._services.prompts.datasource.build_ml_models_datasource_prompt import build_ml_models_datasource_prompt
from apps._services.prompts.datasource.build_sql_datasource_prompt import build_sql_datasource_prompt
from apps._services.prompts.datasource.build_storage_datasource_prompt import build_storage_datasource_prompt
from apps._services.prompts.generic.build_audience_prompt import get_structured_audience_prompt
from apps._services.prompts.generic.build_context_overflow_prompt import get_structured_context_overflow_prompt
from apps._services.prompts.generic.build_glossary_prompt import build_structured_glossary_prompt
from apps._services.prompts.generic.build_instructions_prompt import get_structured_instructions_prompt
from apps._services.prompts.generic.build_memory_prompt import build_structured_memory_prompt
from apps._services.prompts.generic.build_name_prompt import get_structured_name_prompt
from apps._services.prompts.generic.build_place_and_time_prompt import build_structured_place_and_time_prompt
from apps._services.prompts.generic.build_primary_guidelines import build_structured_primary_guidelines
from apps._services.prompts.generic.build_response_language_prompt import get_structured_response_language_prompt
from apps._services.prompts.generic.build_response_template_prompt import get_structured_response_template_prompt
from apps._services.prompts.generic.build_tone_prompt import get_structured_tone_prompt
from apps._services.prompts.generic.build_user_information_prompt import build_structured_user_information_prompt
from apps._services.prompts.tools.build_tool_usage_instructions_prompt import \
    build_structured_tool_usage_instructions_prompt
from apps._services.prompts.tools.tool_prompts.build_file_system_command_execution_tool_prompt import \
    build_structured_tool_prompt__file_system_command_execution
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
        name = assistant.name
        response_template = assistant.response_template
        audience = assistant.audience
        tone = assistant.tone
        response_language = assistant.response_language

        ##################################################
        # GENERIC PROMPTS
        primary_guidelines_prompt = build_structured_primary_guidelines()
        structured_name_prompt = get_structured_name_prompt(name, chat.chat_name)
        structured_instructions_prompt = get_structured_instructions_prompt(assistant)
        structured_response_template_prompt = get_structured_response_template_prompt(response_template)
        structured_audience_prompt = get_structured_audience_prompt(audience)
        structured_tone_prompt = get_structured_tone_prompt(tone)
        structured_response_language_prompt = get_structured_response_language_prompt(response_language)
        structured_user_information_prompt = build_structured_user_information_prompt(user)
        structured_memory_prompt = build_structured_memory_prompt(assistant, user)
        structured_glossary_prompt = build_structured_glossary_prompt(assistant.glossary)
        structured_place_and_time_prompt = ""
        if assistant.time_awareness and assistant.place_awareness:
            structured_place_and_time_prompt = build_structured_place_and_time_prompt(assistant, user)
        structured_context_overflow_prompt = get_structured_context_overflow_prompt(assistant)
        ##################################################
        # DATASOURCE PROMPTS
        structured_sql_datasource_prompt = build_sql_datasource_prompt(assistant, user)
        structured_knowledge_base_datasource_prompt = build_knowledge_base_datasource_prompt(assistant, user)
        structured_file_system_prompt = build_file_system_datasource_prompt(assistant, user)
        structured_media_storage_prompt = build_storage_datasource_prompt(assistant, user)
        structured_ml_model_prompt = build_ml_models_datasource_prompt(assistant, user)
        ##################################################
        # TOOL PROMPTS
        structured_tool_usage_instructions_prompt = (
            build_structured_tool_usage_instructions_prompt(assistant, user)
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
        merged_prompt += structured_sql_datasource_prompt
        merged_prompt += structured_knowledge_base_datasource_prompt
        merged_prompt += structured_file_system_prompt
        merged_prompt += structured_media_storage_prompt
        merged_prompt += structured_ml_model_prompt
        ##################################################
        merged_prompt += structured_tool_usage_instructions_prompt
        ##################################################
        # add the tool usage prompts
        merged_prompt += structured_sql_query_execution_tool_prompt
        merged_prompt += structured_knowledge_base_query_execution_tool_prompt
        merged_prompt += structured_vectorized_context_history_query_execution_tool_prompt
        merged_prompt += structured_file_system_command_execution_tool_prompt
        merged_prompt += structured_storage_query_execution_tool_prompt
        merged_prompt += structured_url_file_downloader_tool_prompt
        merged_prompt += structured_predict_with_ml_model_execution_tool_prompt
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
            encoding_engine="cl100k_base",
            transaction_context_content=merged_prompt,
            llm_cost=0,
            internal_service_cost=0,
            tax_cost=0,
            total_cost=0,
            total_billable_cost=0,
            transaction_type="system",
            transaction_source=chat.chat_source
        )
        # Add the transaction to the chat
        chat.transactions.add(transaction)
        chat.save()

        return prompt
