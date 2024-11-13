#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: function_utils.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:44
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

logger = logging.getLogger(__name__)


def get_permissions_grouped():
    logger.info("Getting permissions grouped")
    permissions_grouped = {
        "Organization Permissions": [
            ('add_organizations', 'Add Organizations'),
            ('update_organizations', 'Update Organizations'),
            ('list_organizations', 'List Organizations'),
            ('delete_organizations', 'Delete Organizations'),
            ('add_balance_to_organization', 'Add Balance to Organization'),
            ('transfer_balance_between_organizations', 'Transfer Balance Between Organizations'),
        ],
        "Project Permissions": [
            ('add_projects', 'Add Projects'),
            ('update_projects', 'Update Projects'),
            ('list_projects', 'List Projects'),
            ('delete_projects', 'Delete Projects'),
        ],
        "Team Permissions": [
            ('add_teams', 'Add Teams'),
            ('update_teams', 'Update Teams'),
            ('list_teams', 'List Teams'),
            ('delete_teams', 'Delete Teams'),
        ],
        "MetaKanban Board Permissions": [
            ('add_metakanban_board', 'Add MetaKanban Board'),
            ('update_metakanban_board', 'Update MetaKanban Board'),
            ('list_metakanban_board', 'List MetaKanban Board'),
            ('delete_metakanban_board', 'Delete MetaKanban Board'),
        ],
        "MetaKanban Task Label Permissions": [
            ('add_metakanban_task_label', 'Add MetaKanban Task Label'),
            ('update_metakanban_task_label', 'Update MetaKanban Task Label'),
            ('list_metakanban_task_label', 'List MetaKanban Task Label'),
            ('delete_metakanban_task_label', 'Delete MetaKanban Task Label'),
        ],
        "MetaKanban Column Permissions": [
            ('add_metakanban_column', 'Add MetaKanban Column'),
            ('update_metakanban_column', 'Update MetaKanban Column'),
            ('delete_metakanban_column', 'Delete MetaKanban Column'),
            ('move_metakanban_column', 'Move MetaKanban Column'),
        ],
        "MetaKanban Task Permissions": [
            ('add_metakanban_task', 'Add MetaKanban Task'),
            ('update_metakanban_task', 'Update MetaKanban Task'),
            ('delete_metakanban_task', 'Delete MetaKanban Task'),
            ('move_metakanban_task', 'Move MetaKanban Task'),
            ('assign_metakanban_task', 'Assign MetaKanban Task'),
        ],
        "MetaKanban AI Permissions": [
            ('use_metakanban_ai', 'Use MetaKanban AI'),
            ('connect_assistants_to_metakanban', 'Connect Assistants to MetaKanban'),
            ('disconnect_assistants_from_metakanban', 'Disconnect Assistants from MetaKanban'),
        ],
        "MetaKanban Meeting Transcription Permissions": [
            ("use_metakanban_meeting_transcription", "Use MetaKanban Meeting Transcription"),
            ("implement_meeting_transcription_with_ai", "Implement Meeting Transcription with AI"),
            ("delete_meeting_transcription", "Delete Meeting Transcription"),
        ],
        "MetaTempo Connection Permissions": [
            ('add_metatempo_connection', 'Add MetaTempo Connection'),
            ('update_metatempo_connection', 'Update MetaTempo Connection'),
            ('list_metatempo_connection', 'List MetaTempo Connection'),
            ('delete_metatempo_connection', 'Delete MetaTempo Connection'),
            ('use_meta_tempo_ai', 'Use MetaTempo AI'),
        ],
        "LLM Core Permissions": [
            ('add_llm_cores', 'Add LLM Cores'),
            ('update_llm_cores', 'Update LLM Cores'),
            ('list_llm_cores', 'List LLM Cores'),
            ('delete_llm_cores', 'Delete LLM Cores')
        ],
        "Fine-Tuning Model Permissions": [
            ('add_finetuning_model', 'Add Finetuning Model'),
            ('update_finetuning_model', 'Update Finetuning Model'),
            ('list_finetuning_model', 'List Finetuning Model'),
            ('delete_finetuning_model', 'Delete Finetuning Model'),
        ],
        "Transaction Permissions": [
            ('list_transactions', 'List Transactions')
        ],
        "Data Security Permissions": [
            ('add_data_security', 'Add Data Security'),
            ('update_data_security', 'Update Data Security'),
            ('list_data_security', 'List Data Security'),
            ('delete_data_security', 'Delete Data Security'),
        ],
        "Data Backups Permissions": [
            ('create_data_backups', 'Create Data Backups'),
            ('list_data_backups', 'List Data Backups'),
            ('delete_data_backups', 'Delete Data Backups'),
            ('restore_data_backups', 'Restore Data Backups'),
        ],
        "User Permissions": [
            ('add_users', 'Add Users'),
            ('update_users', 'Update Users'),
            ('list_users', 'List Users'),
            ('delete_users', 'Delete Users'),
            ('connect_user_to_organization', 'Connect User to Organization'),
            ('remove_user_from_organization', 'Remove User from Organization'),
        ],
        "Permission Management Permissions": [
            ('modify_user_permissions', 'Modify User Permissions'),
            ('list_user_permissions', 'List User Permissions')
        ],
        "User Role Management Permissions": [
            ('create_user_roles', 'Create User Roles'),
            ('list_user_roles', 'List User Roles'),
            ('update_user_roles', 'Update User Roles'),
            ('delete_user_roles', 'Delete User Roles'),
        ],
        "Harmoniq Assistant Permissions": [
            ('add_harmoniq_agents', 'Add Harmoniq Agents'),
            ('update_harmoniq_agents', 'Update Harmoniq Agents'),
            ('list_harmoniq_agents', 'List Harmoniq Agents'),
            ('delete_harmoniq_agents', 'Delete Harmoniq Agents'),
            ('chat_with_harmoniq_agents', 'Chat with Harmoniq Agents'),
        ],
        "Assistant Permissions": [
            ('add_assistants', 'Add Assistants'),
            ('update_assistants', 'Update Assistants'),
            ('list_assistants', 'List Assistants'),
            ('delete_assistants', 'Delete Assistants')
        ],
        "Plug & Play Agents": [
            ('integrate_plug_and_play_agents', 'Integrate Plug and Play Agents'),
            ('list_plug_and_play_agents', 'List Plug and Play Agents'),
        ],
        "Plug & Play Teams": [
            ('integrate_plug_and_play_teams', 'Integrate Plug and Play Teams'),
            ('list_plug_and_play_teams', 'List Plug and Play Teams'),
        ],
        "Assistant Exportation Permissions": [
            ('add_export_assistant', 'Add Export Assistants'),
            ('update_export_assistant', 'Update Export Assistants'),
            ('list_export_assistant', 'List Export Assistants'),
            ('delete_export_assistant', 'Delete Export Assistants')
        ],
        "LeanMod Assistant Permissions": [
            ('add_lean_assistant', 'Add Lean Assistant'),
            ('update_lean_assistant', 'Update Lean Assistant'),
            ('list_lean_assistant', 'List Lean Assistant'),
            ('delete_lean_assistant', 'Delete Lean Assistant'),
        ],
        "Expert Networks Permissions": [
            ('add_expert_networks', 'Add Expert Networks'),
            ('update_expert_networks', 'Update Expert Networks'),
            ('list_expert_networks', 'List Expert Networks'),
            ('delete_expert_networks', 'Delete Expert Networks'),
        ],
        "LeanMod Assistant Export Permissions": [
            ('add_export_leanmod', 'Add Export LeanMod'),
            ('update_export_leanmod', 'Update Export LeanMod'),
            ('list_export_leanmod', 'List Export LeanMod'),
            ('delete_export_leanmod', 'Delete Export LeanMod'),
        ],
        "Chat Permissions": [
            ('create_and_use_chats', 'Create and Use Chats'),
            ('remove_chats', 'Remove Chats'),
            ('archive_chats', 'Archive Chats'),
            ('unarchive_chats', 'Unarchive Chats'),
        ],
        "LeanMod Chat Permissions": [
            ('create_and_use_lean_chats', 'Create and Use Lean Chats'),
            ('remove_lean_chats', 'Remove Lean Chats'),
            ('archive_lean_chats', 'Archive Lean Chats'),
            ('unarchive_lean_chats', 'Unarchive Lean Chats'),
        ],
        "Starred Messages Permissions": [
            ('add_starred_messages', 'Add Starred Messages'),
            ('list_starred_messages', 'List Starred Messages'),
            ('remove_starred_messages', 'Remove Starred Messages'),
        ],
        "Message Templates Permissions": [
            ('add_template_messages', 'Add Message Templates'),
            ('update_template_messages', 'Update Message Templates'),
            ('list_template_messages', 'List Message Templates'),
            ('remove_template_messages', 'Remove Message Templates'),
        ],
        "Memory Permissions": [
            ('add_assistant_memories', 'Add Assistant Memories'),
            ('list_assistant_memories', 'List Assistant Memories'),
            ('delete_assistant_memories', 'Delete Assistant Memories')
        ],
        "eLLMa Scripts": [
            ('create_ellma_scripts', 'Create Ellma Scripts'),
            ('list_ellma_scripts', 'List Ellma Scripts'),
            ('update_ellma_scripts', 'Update Ellma Scripts'),
            ('delete_ellma_scripts', 'Delete Ellma Scripts'),
        ],
        "Drafting Folder Permissions": [
            ('add_drafting_folders', 'Add Drafting Folders'),
            ('update_drafting_folders', 'Update Drafting Folders'),
            ('list_drafting_folders', 'List Drafting Folders'),
            ('delete_drafting_folders', 'Delete Drafting Folders'),
        ],
        "Drafting Document Permissions": [
            ('add_drafting_documents', 'Add Drafting Documents'),
            ('update_drafting_documents', 'Update Drafting Documents'),
            ('list_drafting_documents', 'List Drafting Documents'),
            ('delete_drafting_documents', 'Delete Drafting Documents'),
        ],
        "Drafting Google Apps Permissions": [
            ('add_drafting_google_apps_connections', 'Add Drafting Google Apps Connections'),
            ('list_drafting_google_apps_connections', 'List Drafting Google Apps Connections'),
            ('update_drafting_google_apps_connections', 'Update Drafting Google Apps Connections'),
            ('delete_drafting_google_apps_connections', 'Delete Drafting Google Apps Connections'),
        ],
        "Sheetos Folder Permissions": [
            ('add_sheetos_folders', 'Add Sheetos Folders'),
            ('update_sheetos_folders', 'Update Sheetos Folders'),
            ('list_sheetos_folders', 'List Sheetos Folders'),
            ('delete_sheetos_folders', 'Delete Sheetos Folders'),
        ],
        "Sheetos Document Permissions": [
            ('add_sheetos_documents', 'Add Sheetos Documents'),
            ('update_sheetos_documents', 'Update Sheetos Documents'),
            ('list_sheetos_documents', 'List Sheetos Documents'),
            ('delete_sheetos_documents', 'Delete Sheetos Documents'),
        ],
        "Sheetos Google Apps Permissions": [
            ('add_sheetos_google_apps_connections', 'Add Sheetos Google Apps Connections'),
            ('update_sheetos_google_apps_connections', 'Update Sheetos Google Apps Connections'),
            ('list_sheetos_google_apps_connections', 'List Sheetos Google Apps Connections'),
            ('delete_sheetos_google_apps_connections', 'Delete Sheetos Google Apps Connections'),
        ],
        "Slider Folder Permissions": [
            ('add_slider_folders', 'Add Slider Folders'),
            ('update_slider_folders', 'Update Slider Folders'),
            ('list_slider_folders', 'List Slider Folders'),
            ('delete_slider_folders', 'Delete Slider Folders'),
        ],
        "Slider Document Permissions": [
            ('add_slider_documents', 'Add Slider Documents'),
            ('update_slider_documents', 'Update Slider Documents'),
            ('list_slider_documents', 'List Slider Documents'),
            ('delete_slider_documents', 'Delete Slider Documents'),
        ],
        "Slider Google Apps Permissions": [
            ('add_slider_google_apps_connections', 'Add Slider Google Apps Connections'),
            ('update_slider_google_apps_connections', 'Update Slider Google Apps Connections'),
            ('list_slider_google_apps_connections', 'List Slider Google Apps Connections'),
            ('delete_slider_google_apps_connections', 'Delete Slider Google Apps Connections'),
        ],
        "Formica Google Apps Permissions": [
            ('add_formica_google_apps_connections', 'Add Formica Google Apps Connections'),
            ('update_formica_google_apps_connections', 'Update Formica Google Apps Connections'),
            ('list_formica_google_apps_connections', 'List Formica Google Apps Connections'),
            ('delete_formica_google_apps_connections', 'Delete Formica Google Apps Connections'),
        ],
        "Brainstorming Permissions": [
            ('create_brainstorming_sessions', 'Create Brainstorming Sessions'),
            ('list_brainstorming_sessions', 'List Brainstorming Sessions'),
            ('update_brainstorming_sessions', 'Update Brainstorming Sessions'),
            ('delete_brainstorming_sessions', 'Delete Brainstorming Sessions'),
            ('create_brainstorming_ideas', 'Create Brainstorming Ideas'),
            ('delete_brainstorming_ideas', 'Delete Brainstorming Ideas'),
            ('create_brainstorming_syntheses', 'Create Brainstorming Syntheses'),
            ('bookmark_brainstorming_ideas', 'Bookmark Brainstorming Ideas'),
        ],
        "Orchestration Permissions": [
            ('add_orchestrations', 'Add Orchestrations'),
            ('update_orchestrations', 'Update Orchestrations'),
            ('list_orchestrations', 'List Orchestrations'),
            ('delete_orchestrations', 'Delete Orchestrations')
        ],
        "Orchestration Export Permissions": [
            ('add_export_orchestration', 'Add Export Orchestration'),
            ('update_export_orchestration', 'Update Export Orchestration'),
            ('list_export_orchestration', 'List Export Orchestration'),
            ('delete_export_orchestration', 'Delete Export Orchestration'),
        ],
        "Orchestration Chat Permissions": [
            ('create_and_use_orchestration_chats', 'Create and Use Orchestration Chats'),
            ('remove_orchestration_chats', 'Remove Orchestration Chats'),
        ],
        "Hadron System Permissions": [
            ('create_hadron_systems', 'Create Hadron Systems'),
            ('list_hadron_systems', 'List Hadron Systems'),
            ('update_hadron_systems', 'Update Hadron Systems'),
            ('delete_hadron_systems', 'Delete Hadron Systems'),
        ],
        "Hadron Node Permissions": [
            ('create_hadron_nodes', 'Create Hadron Nodes'),
            ('list_hadron_nodes', 'List Hadron Nodes'),
            ('update_hadron_nodes', 'Update Hadron Nodes'),
            ('delete_hadron_nodes', 'Delete Hadron Nodes'),
        ],
        "Hadron Topic Permissions": [
            ('create_hadron_topics', 'Create Hadron Topics'),
            ('list_hadron_topics', 'List Hadron Topics'),
            ('update_hadron_topics', 'Update Hadron Topics'),
            ('delete_hadron_topics', 'Delete Hadron Topics'),
        ],
        "Hadron Logs Permissions": [
            ('delete_hadron_node_execution_logs', 'Delete Hadron Node Execution Logs'),
            ('delete_hadron_node_sase_logs', 'Delete Hadron Node SASE Logs'),
            ('delete_hadron_node_publish_history_logs', 'Delete Hadron Node Publish History Logs'),
            ('delete_hadron_topic_message_history_logs', 'Delete Hadron Topic Message History Logs'),
            ('delete_hadron_node_speech_logs', 'Delete Hadron Node Speech Logs'),
        ],
        "Binexus Processes": [
            ('create_binexus_processes', 'Create Binexus Processes'),
            ('list_binexus_processes', 'List Binexus Processes'),
            ('update_binexus_processes', 'Update Binexus Processes'),
            ('delete_binexus_processes', 'Delete Binexus Processes'),
            ('execute_binexus_processes', 'Execute Binexus Processes'),
        ],
        "Binexus Elite Agents": [
            ('list_binexus_elites', 'List Binexus Elites'),
            ('delete_binexus_elites', 'Delete Binexus Elites'),
        ],
        "Blockchain Wallet Permissions": [
            ('create_blockchain_wallet_connections', 'Create Blockchain Wallet Connections'),
            ('list_blockchain_wallet_connections', 'List Blockchain Wallet Connections'),
            ('update_blockchain_wallet_connections', 'Update Blockchain Wallet Connections'),
            ('delete_blockchain_wallet_connections', 'Delete Blockchain Wallet Connections'),
        ],
        "Smart Contract Permissions": [
            ('create_smart_contracts', 'Create Smart Contracts'),
            ('list_smart_contracts', 'List Smart Contracts'),
            ('soft_delete_smart_contracts', 'Soft Delete Smart Contracts'),
        ],
        "File System Permissions": [
            ('add_file_systems', 'Add File Systems'),
            ('update_file_systems', 'Update File Systems'),
            ('list_file_systems', 'List File Systems'),
            ('delete_file_systems', 'Delete File Systems')
        ],
        "Web Browser Permissions": [
            ('add_web_browsers', 'Add Web Browsers'),
            ('update_web_browsers', 'Update Web Browsers'),
            ('list_web_browsers', 'List Web Browsers'),
            ('delete_web_browsers', 'Delete Web Browsers')
        ],
        "SQL Database Permissions": [
            ('add_sql_databases', 'Add SQL Databases'),
            ('update_sql_databases', 'Update SQL Databases'),
            ('list_sql_databases', 'List SQL Databases'),
            ('delete_sql_databases', 'Delete SQL Databases')
        ],
        "Custom SQL Queries Permissions": [
            ('add_custom_sql_queries', 'Add Custom SQL Queries'),
            ('update_custom_sql_queries', 'Update Custom SQL Queries'),
            ('list_custom_sql_queries', 'List Custom SQL Queries'),
            ('delete_custom_sql_queries', 'Delete Custom SQL Queries'),
        ],
        "NoSQL Database Permissions": [
            ('add_nosql_databases', 'Add NoSQL Databases'),
            ('update_nosql_databases', 'Update NoSQL Databases'),
            ('list_nosql_databases', 'List NoSQL Databases'),
            ('delete_nosql_databases', 'Delete NoSQL Databases')
        ],
        "Custom NoSQL Queries Permissions": [
            ('add_custom_nosql_queries', 'Add Custom NoSQL Queries'),
            ('update_custom_nosql_queries', 'Update Custom NoSQL Queries'),
            ('list_custom_nosql_queries', 'List Custom NoSQL Queries'),
            ('delete_custom_nosql_queries', 'Delete Custom NoSQL Queries'),
        ],
        "Knowledge Base Permissions": [
            ('add_knowledge_bases', 'Add Knowledge Bases'),
            ('update_knowledge_bases', 'Update Knowledge Bases'),
            ('list_knowledge_bases', 'List Knowledge Bases'),
            ('delete_knowledge_bases', 'Delete Knowledge Bases')
        ],
        "Knowledge Base Documents Permissions": [
            ('add_knowledge_base_docs', 'Add Knowledge Base Docs'),
            ('update_knowledge_base_docs', 'Update Knowledge Base Docs'),
            ('list_knowledge_base_docs', 'List Knowledge Base Docs'),
            ('delete_knowledge_base_docs', 'Delete Knowledge Base Docs'),
        ],
        "Code Base Permissions": [
            ('add_code_base', 'Add Code Base'),
            ('update_code_base', 'Update Code Base'),
            ('list_code_base', 'List Code Base'),
            ('delete_code_base', 'Delete Code Base'),
        ],
        "Code Repository Permissions": [
            ('add_code_repository', 'Add Code Repository'),
            ('update_code_repository', 'Update Code Repository'),
            ('list_code_repository', 'List Code Repository'),
            ('delete_code_repository', 'Delete Code Repository'),
        ],
        "Media Storage Permissions": [
            ('add_media_storages', 'Add Media Storages'),
            ('update_media_storages', 'Update Media Storages'),
            ('list_media_storages', 'List Media Storages'),
            ('delete_media_storages', 'Delete Media Storages')
        ],
        "Media Storage Documents Permissions": [
            ('add_storage_files', 'Add Storage Files'),
            ('update_storage_files', 'Update Storage Files'),
            ('list_storage_files', 'List Storage Files'),
            ('delete_storage_files', 'Delete Storage Files'),
        ],
        "ML Model Permissions": [
            ('add_ml_model_connections', 'Add ML Model Connections'),
            ('update_ml_model_connections', 'Update ML Model Connections'),
            ('list_ml_model_connections', 'List ML Model Connections'),
            ('delete_ml_model_connections', 'Delete ML Model Connections'),
        ],
        "ML Model Items Permissions": [
            ('add_ml_model_files', 'Add ML Model Files'),
            ('update_ml_model_files', 'Update ML Model Files'),
            ('list_ml_model_files', 'List ML Model Files'),
            ('delete_ml_model_files', 'Delete ML Model Files'),
        ],
        "ML Model Integrations Permissions": [
            ('integrate_ml_model_files', 'Integrate ML Model Files'),
            ('list_ml_model_integrations', 'List ML Model Integrations'),
        ],
        "Function Permissions": [
            ('add_functions', 'Add Functions'),
            ('update_functions', 'Update Functions'),
            ('list_functions', 'List Functions'),
            ('delete_functions', 'Delete Functions')
        ],
        "API Permissions": [
            ('add_apis', 'Add APIs'),
            ('update_apis', 'Update APIs'),
            ('list_apis', 'List APIs'),
            ('delete_apis', 'Delete APIs')
        ],
        "Script Permissions": [
            ('add_scripts', 'Add Scripts'),
            ('update_scripts', 'Update Scripts'),
            ('list_scripts', 'List Scripts'),
            ('delete_scripts', 'Delete Scripts')
        ],
        "Scheduled Job Permissions": [
            ('add_scheduled_jobs', 'Add Scheduled Jobs'),
            ('update_scheduled_jobs', 'Update Scheduled Jobs'),
            ('list_scheduled_jobs', 'List Scheduled Jobs'),
            ('delete_scheduled_jobs', 'Delete Scheduled Jobs')
        ],
        "Trigger Permissions": [
            ('add_triggers', 'Add Triggers'),
            ('update_triggers', 'Update Triggers'),
            ('list_triggers', 'List Triggers'),
            ('delete_triggers', 'Delete Triggers')
        ],
        "Image Generation Permissions": [
            ('can_generate_images', 'Can Generate Images')
        ],
        "Audio Generation Permissions": [
            ('can_generate_audio', 'Can Generate Audio')
        ],
        "Video Generator Connections": [
            ('create_video_generator_connections', 'Create Video Generator Connections'),
            ('list_video_generator_connections', 'List Video Generator Connections'),
            ('update_video_generator_connections', 'Update Video Generator Connections'),
            ('delete_video_generator_connections', 'Delete Video Generator Connections'),
        ],
        "Integration Permissions": [
            ('add_integrations', 'Add Integrations'),
            ('update_integrations', 'Update Integrations'),
            ('list_integrations', 'List Integrations'),
            ('delete_integrations', 'Delete Integrations')
        ],
        "Meta Integration Permissions": [
            ('add_meta_integrations', 'Add Meta Integrations'),
            ('update_meta_integrations', 'Update Meta Integrations'),
            ('list_meta_integrations', 'List Meta Integrations'),
            ('delete_meta_integrations', 'Delete Meta Integrations')
        ],
        "Support Ticket Permissions": [
            ('create_support_tickets', 'Create Support Tickets'),
            ('list_support_tickets', 'List Support Tickets'),
            ('update_support_tickets', 'Update Support Tickets'),
        ],
        "Internal Notifications": [
            ('create_internal_notifications', 'Create Internal Notifications'),
            ('delete_internal_notifications', 'Delete Internal Notifications'),
        ],
    }
    return permissions_grouped
