#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: function_utils.py
#  Last Modified: 2024-09-26 19:20:31
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:27:13
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

def prepare_data_for_charts(statistics, context):
    # costs
    costs_per_organizations = statistics.get("costs", {}).get("costs_per_organizations", {})
    costs_per_assistants = statistics.get("costs", {}).get("costs_per_assistants", {})
    costs_per_users = statistics.get("costs", {}).get("costs_per_users", {})
    costs_per_sources = statistics.get("costs", {}).get("costs_per_sources", {})
    cost_per_sources_main = costs_per_sources.get("main", {})
    cost_per_sources_tools = costs_per_sources.get("tool", {})
    # skip balance snapshots for now
    # ...
    # tokens
    tokens_per_organizations = statistics.get("tokens", {}).get("tokens_per_organizations", {})
    tokens_per_assistants = statistics.get("tokens", {}).get("tokens_per_assistants", {})
    tokens_per_users = statistics.get("tokens", {}).get("tokens_per_users", {})
    tokens_per_sources = statistics.get("tokens", {}).get("tokens_per_sources", {})
    tokens_per_sources_main = tokens_per_sources.get("main", {})
    tokens_per_sources_tools = tokens_per_sources.get("tool", {})
    # assistant communication
    total_chats_per_organizations = statistics.get("communication").get("total_chats_per_organizations", {})
    total_messages_per_organizations = statistics.get("communication").get("total_messages_per_organizations", {})
    total_request_count_per_exported_assistants = statistics.get("exports").get(
        "total_request_count_per_exported_assistants", {})
    # sql database usage
    total_sql_read_queries_per_assistants = statistics.get("sql").get("total_sql_read_queries_per_assistants", {})
    total_sql_write_queries_per_assistants = statistics.get("sql").get("total_sql_write_queries_per_assistants", {})
    total_sql_queries_per_assistants = statistics.get("sql").get("total_sql_queries_per_assistants", {})
    # file systems
    total_ssh_file_system_access_per_assistants = statistics.get("file_system").get(
        "total_ssh_file_system_access_per_assistants", {})
    # web browsing
    total_web_queries_per_assistants = statistics.get("browsing").get("total_web_queries_per_assistants", {})
    # ml model predictions
    total_ml_predictions_per_assistants = statistics.get("ml").get("total_ml_predictions_per_assistants", {})
    # multimedia management
    total_documents_interpretations_per_assistants = statistics.get("knowledge_base").get(
        "total_documents_interpretations_per_assistants", {})
    total_image_interpretations_per_assistants = statistics.get("knowledge_base").get(
        "total_image_interpretations_per_assistants", {})
    total_code_interpretations_per_assistants = statistics.get("knowledge_base").get(
        "total_code_interpretations_per_assistants", {})
    total_file_downloads_per_assistants = statistics.get("knowledge_base").get("total_file_downloads_per_assistants",
                                                                               {})
    total_multimedia_generations_per_assistants = statistics.get("knowledge_base").get(
        "total_multimedia_generations_per_assistants", {})
    # knowledge base searches
    total_knowledge_base_searches_per_assistants = statistics.get("knowledge_base").get(
        "total_knowledge_base_searches_per_assistants", {})
    # memory management
    total_memory_saves_per_assistants = statistics.get("knowledge_base").get("total_memory_saves_per_assistants", {})
    total_memory_retrievals_per_assistants = statistics.get("knowledge_base").get(
        "total_memory_retrievals_per_assistants", {})
    # function execution
    total_internal_function_calls_per_assistants = statistics.get("functions").get(
        "total_internal_function_calls_per_assistants", {})
    total_external_function_calls_per_assistants = statistics.get("functions").get(
        "total_external_function_calls_per_assistants", {})
    total_function_calls_per_assistants = statistics.get("functions").get("total_function_calls_per_assistants", {})
    # api execution
    total_internal_third_party_api_calls_per_assistants = statistics.get("apis").get(
        "total_internal_third_party_api_calls_per_assistants", {})
    total_external_third_party_api_calls_per_assistants = statistics.get("apis").get(
        "total_external_third_party_api_calls_per_assistants", {})
    total_third_party_api_calls_per_assistants = statistics.get("apis").get(
        "total_third_party_api_calls_per_assistants", {})
    # script execution
    total_internal_script_executions_per_assistants = statistics.get("scripts").get(
        "total_internal_script_executions_per_assistants", {})
    total_external_script_executions_per_assistants = statistics.get("scripts").get(
        "total_external_script_executions_per_assistants", {})
    total_script_executions_per_assistants = statistics.get("scripts").get("total_script_executions_per_assistants",
                                                                           {})
    # cron and trigger jobs
    total_scheduled_task_executions_per_assistants = statistics.get("crons").get(
        "total_scheduled_task_executions_per_assistants", {})
    total_triggered_task_executions_per_assistants = statistics.get("triggers").get(
        "total_triggered_task_executions_per_assistants", {})
    # users
    total_users_per_organizations = statistics.get("users").get("total_users_per_organizations", {})
    latest_registered_users_per_organizations = statistics.get("users").get(
        "latest_registered_users_per_organizations", {})

    # Prepare data for Chart.js / costs / labels
    context["costs_per_organizations_labels"] = list(costs_per_organizations.keys())
    context["costs_per_assistants_labels"] = list(costs_per_assistants.keys())
    context["costs_per_users_labels"] = list(costs_per_users.keys())
    context["costs_per_sources_main_labels"] = list(cost_per_sources_main.keys())
    context["costs_per_sources_tools_labels"] = list(cost_per_sources_tools.keys())
    # Prepare data for Chart.js / costs / values
    context["costs_per_organizations_values"] = list(costs_per_organizations.values())
    context["costs_per_assistants_values"] = list(costs_per_assistants.values())
    context["costs_per_users_values"] = list(costs_per_users.values())
    context["costs_per_sources_main_values"] = list(cost_per_sources_main.values())
    context["costs_per_sources_tools_values"] = list(cost_per_sources_tools.values())

    # Prepare data for Chart.js / tokens / labels
    context["tokens_per_organizations_labels"] = list(tokens_per_organizations.keys())
    context["tokens_per_assistants_labels"] = list(tokens_per_assistants.keys())
    context["tokens_per_users_labels"] = list(tokens_per_users.keys())
    context["tokens_per_sources_main_labels"] = list(tokens_per_sources_main.keys())
    context["tokens_per_sources_tools_labels"] = list(tokens_per_sources_tools.keys())
    # Prepare data for Chart.js / tokens / values
    context["tokens_per_organizations_values"] = list(tokens_per_organizations.values())
    context["tokens_per_assistants_values"] = list(tokens_per_assistants.values())
    context["tokens_per_users_values"] = list(tokens_per_users.values())
    context["tokens_per_sources_main_values"] = list(tokens_per_sources_main.values())
    context["tokens_per_sources_tools_values"] = list(tokens_per_sources_tools.values())

    # Prepare data for Chart.js / assistant communication / labels
    context["total_chats_per_organizations_labels"] = list(total_chats_per_organizations.keys())
    context["total_chat_messages_per_organizations_labels"] = list(total_messages_per_organizations.keys())
    context["total_request_count_per_exported_assistants_labels"] = list(
        total_request_count_per_exported_assistants.keys())
    # Prepare data for Chart.js / assistant communication / values
    context["total_chats_per_organizations_values"] = list(total_chats_per_organizations.values())
    context["total_chat_messages_per_organizations_values"] = list(total_messages_per_organizations.values())
    context["total_request_count_per_exported_assistants_values"] = list(
        total_request_count_per_exported_assistants.values())

    # Prepare data for Chart.js / sql database usage / labels
    context["total_sql_read_queries_per_assistants_labels"] = list(total_sql_read_queries_per_assistants.keys())
    context["total_sql_write_queries_per_assistants_labels"] = list(total_sql_write_queries_per_assistants.keys())
    context["total_sql_queries_per_assistants_labels"] = list(total_sql_queries_per_assistants.keys())
    # Prepare data for Chart.js / sql database usage / values
    context["total_sql_read_queries_per_assistants_values"] = list(total_sql_read_queries_per_assistants.values())
    context["total_sql_write_queries_per_assistants_values"] = list(total_sql_write_queries_per_assistants.values())
    context["total_sql_queries_per_assistants_values"] = list(total_sql_queries_per_assistants.values())

    # Prepare data for Chart.js / file systems / labels
    context["total_ssh_file_system_access_per_assistants_labels"] = list(
        total_ssh_file_system_access_per_assistants.keys())
    # Prepare data for Chart.js / file systems / values
    context["total_ssh_file_system_access_per_assistants_values"] = list(
        total_ssh_file_system_access_per_assistants.values())

    # Prepare data for Chart.js / web browsing / labels
    context["total_web_queries_per_assistants_labels"] = list(total_web_queries_per_assistants.keys())
    # Prepare data for Chart.js / web browsing / values
    context["total_web_queries_per_assistants_values"] = list(total_web_queries_per_assistants.values())

    # Prepare data for Chart.js / ml model predictions / labels
    context["total_ml_predictions_per_assistants_labels"] = list(total_ml_predictions_per_assistants.keys())
    # Prepare data for Chart.js / ml model predictions / values
    context["total_ml_predictions_per_assistants_values"] = list(total_ml_predictions_per_assistants.values())

    # Prepare data for Chart.js / multimedia management / labels
    context["total_documents_interpretations_per_assistants_labels"] = list(
        total_documents_interpretations_per_assistants.keys())
    context["total_image_interpretations_per_assistants_labels"] = list(
        total_image_interpretations_per_assistants.keys())
    context["total_code_interpretations_per_assistants_labels"] = list(
        total_code_interpretations_per_assistants.keys())
    context["total_file_downloads_per_assistants_labels"] = list(total_file_downloads_per_assistants.keys())
    context["total_multimedia_generations_per_assistants_labels"] = list(
        total_multimedia_generations_per_assistants.keys())
    # Prepare data for Chart.js / multimedia management / values
    context["total_documents_interpretations_per_assistants_values"] = list(
        total_documents_interpretations_per_assistants.values())
    context["total_image_interpretations_per_assistants_values"] = list(
        total_image_interpretations_per_assistants.values())
    context["total_code_interpretations_per_assistants_values"] = list(
        total_code_interpretations_per_assistants.values())
    context["total_file_downloads_per_assistants_values"] = list(total_file_downloads_per_assistants.values())
    context["total_multimedia_generations_per_assistants_values"] = list(
        total_multimedia_generations_per_assistants.values())

    # Prepare data for Chart.js / knowledge base searches / labels
    context["total_knowledge_base_searches_per_assistants_labels"] = list(
        total_knowledge_base_searches_per_assistants.keys())
    # Prepare data for Chart.js / knowledge base searches / values
    context["total_knowledge_base_searches_per_assistants_values"] = list(
        total_knowledge_base_searches_per_assistants.values())

    # Prepare data for Chart.js / memory management / labels
    context["total_memory_saves_per_assistants_labels"] = list(total_memory_saves_per_assistants.keys())
    context["total_memory_retrievals_per_assistants_labels"] = list(total_memory_retrievals_per_assistants.keys())
    # Prepare data for Chart.js / memory management / values
    context["total_memory_saves_per_assistants_values"] = list(total_memory_saves_per_assistants.values())
    context["total_memory_retrievals_per_assistants_values"] = list(total_memory_retrievals_per_assistants.values())

    # Prepare data for Chart.js / function execution / labels
    context["total_internal_function_calls_per_assistants_labels"] = list(
        total_internal_function_calls_per_assistants.keys())
    context["total_external_function_calls_per_assistants_labels"] = list(
        total_external_function_calls_per_assistants.keys())
    context["total_function_calls_per_assistants_labels"] = list(total_function_calls_per_assistants.keys())
    # Prepare data for Chart.js / function execution / values
    context["total_internal_function_calls_per_assistants_values"] = list(
        total_internal_function_calls_per_assistants.values())
    context["total_external_function_calls_per_assistants_values"] = list(
        total_external_function_calls_per_assistants.values())
    context["total_function_calls_per_assistants_values"] = list(total_function_calls_per_assistants.values())

    # Prepare data for Chart.js / api execution / labels
    context["total_internal_third_party_api_calls_per_assistants_labels"] = list(
        total_internal_third_party_api_calls_per_assistants.keys())
    context["total_external_third_party_api_calls_per_assistants_labels"] = list(
        total_external_third_party_api_calls_per_assistants.keys())
    context["total_third_party_api_calls_per_assistants_labels"] = list(
        total_third_party_api_calls_per_assistants.keys())
    # Prepare data for Chart.js / api execution / values
    context["total_internal_third_party_api_calls_per_assistants_values"] = list(
        total_internal_third_party_api_calls_per_assistants.values())
    context["total_external_third_party_api_calls_per_assistants_values"] = list(
        total_external_third_party_api_calls_per_assistants.values())
    context["total_third_party_api_calls_per_assistants_values"] = list(
        total_third_party_api_calls_per_assistants.values())

    # Prepare data for Chart.js / script execution / labels
    context["total_internal_script_executions_per_assistants_labels"] = list(
        total_internal_script_executions_per_assistants.keys())
    context["total_external_script_executions_per_assistants_labels"] = list(
        total_external_script_executions_per_assistants.keys())
    context["total_script_executions_per_assistants_labels"] = list(total_script_executions_per_assistants.keys())
    # Prepare data for Chart.js / script execution / values
    context["total_internal_script_executions_per_assistants_values"] = list(
        total_internal_script_executions_per_assistants.values())
    context["total_external_script_executions_per_assistants_values"] = list(
        total_external_script_executions_per_assistants.values())
    context["total_script_executions_per_assistants_values"] = list(total_script_executions_per_assistants.values())

    # Prepare data for Chart.js / cron and trigger jobs / labels
    context["total_scheduled_task_executions_per_assistants_labels"] = list(
        total_scheduled_task_executions_per_assistants.keys())
    context["total_triggered_task_executions_per_assistants_labels"] = list(
        total_triggered_task_executions_per_assistants.keys())
    # Prepare data for Chart.js / cron and trigger jobs / values
    context["total_scheduled_task_executions_per_assistants_values"] = list(
        total_scheduled_task_executions_per_assistants.values())
    context["total_triggered_task_executions_per_assistants_values"] = list(
        total_triggered_task_executions_per_assistants.values())

    # Prepare data for Chart.js / users / labels
    context["total_users_per_organizations_labels"] = list(total_users_per_organizations.keys())
    context["latest_registered_users_per_organizations_labels"] = list(
        latest_registered_users_per_organizations.keys())
    # Prepare data for Chart.js / users / values
    context["total_users_per_organizations_values"] = list(total_users_per_organizations.values())
    context["latest_registered_users_per_organizations_values"] = list(
        latest_registered_users_per_organizations.values())

    return context
