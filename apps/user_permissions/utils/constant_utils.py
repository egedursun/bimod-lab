#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
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

class PermissionNames:
    ADD_LLM_CORES = 'add_llm_cores'
    UPDATE_LLM_CORES = 'update_llm_cores'
    LIST_LLM_CORES = 'list_llm_cores'
    DELETE_LLM_CORES = 'delete_llm_cores'

    ADD_ORGANIZATIONS = 'add_organizations'
    UPDATE_ORGANIZATIONS = 'update_organizations'
    LIST_ORGANIZATIONS = 'list_organizations'
    DELETE_ORGANIZATIONS = 'delete_organizations'
    ADD_BALANCE_TO_ORGANIZATION = 'add_balance_to_organization'
    TRANSFER_BALANCE_BETWEEN_ORGANIZATIONS = 'transfer_balance_between_organizations'

    ADD_PROJECTS = 'add_projects'
    UPDATE_PROJECTS = 'update_projects'
    LIST_PROJECTS = 'list_projects'
    DELETE_PROJECTS = 'delete_projects'

    ADD_TEAMS = 'add_teams'
    UPDATE_TEAMS = 'update_teams'
    LIST_TEAMS = 'list_teams'
    DELETE_TEAMS = 'delete_teams'

    ADD_METAKANBAN_BOARD = 'add_metakanban_board'
    UPDATE_METAKANBAN_BOARD = 'update_metakanban_board'
    LIST_METAKANBAN_BOARD = 'list_metakanban_board'
    DELETE_METAKANBAN_BOARD = 'delete_metakanban_board'

    ADD_METAKANBAN_TASK_LABEL = 'add_metakanban_task_label'
    UPDATE_METAKANBAN_TASK_LABEL = 'update_metakanban_task_label'
    LIST_METAKANBAN_TASK_LABEL = 'list_metakanban_task_label'
    DELETE_METAKANBAN_TASK_LABEL = 'delete_metakanban_task_label'

    ADD_METAKANBAN_COLUMN = 'add_metakanban_column'
    UPDATE_METAKANBAN_COLUMN = 'update_metakanban_column'
    DELETE_METAKANBAN_COLUMN = 'delete_metakanban_column'
    MOVE_METAKANBAN_COLUMN = 'move_metakanban_column'

    ADD_METAKANBAN_TASK = 'add_metakanban_task'
    UPDATE_METAKANBAN_TASK = 'update_metakanban_task'
    DELETE_METAKANBAN_TASK = 'delete_metakanban_task'
    MOVE_METAKANBAN_TASK = 'move_metakanban_task'
    ASSIGN_METAKANBAN_TASK = 'assign_metakanban_task'

    USE_METAKANBAN_AI = 'use_metakanban_ai'

    LIST_TRANSACTIONS = 'list_transactions'

    ADD_USERS = 'add_users'
    UPDATE_USERS = 'update_users'
    LIST_USERS = 'list_users'
    DELETE_USERS = 'delete_users'
    CONNECT_USER_TO_ORGANIZATION = 'connect_user_to_organization'
    REMOVE_USER_FROM_ORGANIZATION = 'remove_user_from_organization'

    MODIFY_USER_PERMISSIONS = 'modify_user_permissions'
    LIST_USER_PERMISSIONS = 'list_user_permissions'

    ADD_ASSISTANTS = 'add_assistants'
    UPDATE_ASSISTANTS = 'update_assistants'
    LIST_ASSISTANTS = 'list_assistants'
    DELETE_ASSISTANTS = 'delete_assistants'

    ADD_HARMONIQ_AGENTS = 'add_harmoniq_agents'
    UPDATE_HARMONIQ_AGENTS = 'update_harmoniq_agents'
    LIST_HARMONIQ_AGENTS = 'list_harmoniq_agents'
    DELETE_HARMONIQ_AGENTS = 'delete_harmoniq_agents'
    CHAT_WITH_HARMONIQ_AGENTS = 'chat_with_harmoniq_agents'

    CREATE_AND_USE_CHATS = 'create_and_use_chats'
    REMOVE_CHATS = 'remove_chats'

    ADD_ASSISTANT_MEMORIES = 'add_assistant_memories'
    UPDATE_ASSISTANT_MEMORIES = 'update_assistant_memories'
    LIST_ASSISTANT_MEMORIES = 'list_assistant_memories'
    DELETE_ASSISTANT_MEMORIES = 'delete_assistant_memories'

    ADD_EXPORT_ASSISTANT = 'add_export_assistant'
    UPDATE_EXPORT_ASSIST = 'update_export_assistant'
    LIST_EXPORT_ASSISTANT = 'list_export_assistant'
    DELETE_EXPORT_ASSISTANT = 'delete_export_assistant'

    ADD_ORCHESTRATIONS = 'add_orchestrations'
    UPDATE_ORCHESTRATIONS = 'update_orchestrations'
    LIST_ORCHESTRATIONS = 'list_orchestrations'
    DELETE_ORCHESTRATIONS = 'delete_orchestrations'

    ADD_FILE_SYSTEMS = 'add_file_systems'
    UPDATE_FILE_SYSTEMS = 'update_file_systems'
    LIST_FILE_SYSTEMS = 'list_file_systems'
    DELETE_FILE_SYSTEMS = 'delete_file_systems'

    ADD_WEB_BROWSERS = 'add_web_browsers'
    UPDATE_WEB_BROWSERS = 'update_web_browsers'
    LIST_WEB_BROWSERS = 'list_web_browsers'
    DELETE_WEB_BROWSERS = 'delete_web_browsers'

    ADD_SQL_DATABASES = 'add_sql_databases'
    UPDATE_SQL_DATABASES = 'update_sql_databases'
    LIST_SQL_DATABASES = 'list_sql_databases'
    DELETE_SQL_DATABASES = 'delete_sql_databases'

    ADD_NOSQL_DATABASES = 'add_nosql_databases'
    UPDATE_NOSQL_DATABASES = 'update_nosql_databases'
    LIST_NOSQL_DATABASES = 'list_nosql_databases'
    DELETE_NOSQL_DATABASES = 'delete_nosql_databases'

    ADD_CUSTOM_NOSQL_QUERIES = 'add_custom_nosql_queries'
    UPDATE_CUSTOM_NOSQL_QUERIES = 'update_custom_nosql_queries'
    LIST_CUSTOM_NOSQL_QUERIES = 'list_custom_nosql_queries'
    DELETE_CUSTOM_NOSQL_QUERIES = 'delete_custom_nosql_queries'

    ADD_KNOWLEDGE_BASES = 'add_knowledge_bases'
    UPDATE_KNOWLEDGE_BASES = 'update_knowledge_bases'
    LIST_KNOWLEDGE_BASES = 'list_knowledge_bases'
    DELETE_KNOWLEDGE_BASES = 'delete_knowledge_bases'

    ADD_MEDIA_STORAGES = 'add_media_storages'
    UPDATE_MEDIA_STORAGES = 'update_media_storages'
    LIST_MEDIA_STORAGES = 'list_media_storages'
    DELETE_MEDIA_STORAGES = 'delete_media_storages'

    ADD_ML_MODEL_CONNECTIONS = 'add_ml_model_connections'
    UPDATE_ML_MODEL_CONNECTIONS = 'update_ml_model_connections'
    LIST_ML_MODEL_CONNECTIONS = 'list_ml_model_connections'
    DELETE_ML_MODEL_CONNECTIONS = 'delete_ml_model_connections'

    ADD_FUNCTIONS = 'add_functions'
    UPDATE_FUNCTIONS = 'update_functions'
    LIST_FUNCTIONS = 'list_functions'
    DELETE_FUNCTIONS = 'delete_functions'

    ADD_APIS = 'add_apis'
    UPDATE_APIS = 'update_apis'
    LIST_APIS = 'list_apis'
    DELETE_APIS = 'delete_apis'

    ADD_SCRIPTS = 'add_scripts'
    UPDATE_SCRIPTS = 'update_scripts'
    LIST_SCRIPTS = 'list_scripts'
    DELETE_SCRIPTS = 'delete_scripts'

    ADD_SCHEDULED_JOBS = 'add_scheduled_jobs'
    UPDATE_SCHEDULED_JOBS = 'update_scheduled_jobs'
    LIST_SCHEDULED_JOBS = 'list_scheduled_jobs'
    DELETE_SCHEDULED_JOBS = 'delete_scheduled_jobs'

    ADD_TRIGGERS = 'add_triggers'
    UPDATE_TRIGGERS = 'update_triggers'
    LIST_TRIGGERS = 'list_triggers'
    DELETE_TRIGGERS = 'delete_triggers'

    CAN_GENERATE_IMAGES = 'can_generate_images'

    CAN_GENERATE_AUDIO = 'can_generate_audio'

    ADD_INTEGRATIONS = 'add_integrations'
    UPDATE_INTEGRATIONS = 'update_integrations'
    LIST_INTEGRATIONS = 'list_integrations'
    DELETE_INTEGRATIONS = 'delete_integrations'

    ADD_META_INTEGRATIONS = 'add_meta_integrations'
    UPDATE_META_INTEGRATIONS = 'update_meta_integrations'
    LIST_META_INTEGRATIONS = 'list_meta_integrations'
    DELETE_META_INTEGRATIONS = 'delete_meta_integrations'

    ADD_STARRED_MESSAGES = 'add_starred_messages'
    LIST_STARRED_MESSAGES = 'list_starred_messages'
    REMOVE_STARRED_MESSAGES = 'remove_starred_messages'

    ADD_TEMPLATE_MESSAGES = 'add_template_messages'
    LIST_TEMPLATE_MESSAGES = 'list_template_messages'
    UPDATE_TEMPLATE_MESSAGES = 'update_template_messages'
    REMOVE_TEMPLATE_MESSAGES = 'remove_template_messages'

    ADD_DATA_SECURITY = 'add_data_security'
    UPDATE_DATA_SECURITY = 'update_data_security'
    LIST_DATA_SECURITY = 'list_data_security'
    DELETE_DATA_SECURITY = 'delete_data_security'

    ADD_CODE_BASE = 'add_code_base'
    UPDATE_CODE_BASE = 'update_code_base'
    LIST_CODE_BASE = 'list_code_base'
    DELETE_CODE_BASE = 'delete_code_base'

    ADD_CODE_REPOSITORY = 'add_code_repository'
    UPDATE_CODE_REPOSITORY = 'update_code_repository'
    LIST_CODE_REPOSITORY = 'list_code_repository'
    DELETE_CODE_REPOSITORY = 'delete_code_repository'

    ADD_KNOWLEDGE_BASE_DOCS = 'add_knowledge_base_docs'
    UPDATE_KNOWLEDGE_BASE_DOCS = 'update_knowledge_base_docs'
    LIST_KNOWLEDGE_BASE_DOCS = 'list_knowledge_base_docs'
    DELETE_KNOWLEDGE_BASE_DOCS = 'delete_knowledge_base_docs'

    ADD_STORAGE_FILES = 'add_storage_files'
    UPDATE_STORAGE_FILES = 'update_storage_files'
    LIST_STORAGE_FILES = 'list_storage_files'
    DELETE_STORAGE_FILES = 'delete_storage_files'

    ADD_ML_MODEL_FILES = 'add_ml_model_files'
    UPDATE_ML_MODEL_FILES = 'update_ml_model_files'
    LIST_ML_MODEL_FILES = 'list_ml_model_files'
    DELETE_ML_MODEL_FILES = 'delete_ml_model_files'

    ADD_CUSTOM_SQL_QUERIES = 'add_custom_sql_queries'
    UPDATE_CUSTOM_SQL_QUERIES = 'update_custom_sql_queries'
    LIST_CUSTOM_SQL_QUERIES = 'list_custom_sql_queries'
    DELETE_CUSTOM_SQL_QUERIES = 'delete_custom_sql_queries'

    ADD_EXPORT_LEANMOD = 'add_export_leanmod'
    UPDATE_EXPORT_LEANMOD = 'update_export_leanmod'
    LIST_EXPORT_LEANMOD = 'list_export_leanmod'
    DELETE_EXPORT_LEANMOD = 'delete_export_leanmod'

    ADD_EXPERT_NETWORKS = 'add_expert_networks'
    UPDATE_EXPERT_NETWORKS = 'update_expert_networks'
    LIST_EXPERT_NETWORKS = 'list_expert_networks'
    DELETE_EXPERT_NETWORKS = 'delete_expert_networks'

    ADD_EXPORT_ORCHESTRATION = 'add_export_orchestration'
    UPDATE_EXPORT_ORCHESTRATION = 'update_export_orchestration'
    LIST_EXPORT_ORCHESTRATION = 'list_export_orchestration'
    DELETE_EXPORT_ORCHESTRATION = 'delete_export_orchestration'

    ADD_FINETUNING_MODEL = 'add_finetuning_model'
    UPDATE_FINETUNING_MODEL = 'update_finetuning_model'
    LIST_FINETUNING_MODEL = 'list_finetuning_model'
    DELETE_FINETUNING_MODEL = 'delete_finetuning_model'

    ADD_LEAN_ASSISTANT = 'add_lean_assistant'
    UPDATE_LEAN_ASSISTANT = 'update_lean_assistant'
    LIST_LEAN_ASSISTANT = 'list_lean_assistant'
    DELETE_LEAN_ASSISTANT = 'delete_lean_assistant'

    ARCHIVE_CHATS = 'archive_chats'
    UNARCHIVE_CHATS = 'unarchive_chats'

    CREATE_AND_USE_LEAN_CHATS = 'create_and_use_lean_chats'
    REMOVE_LEAN_CHATS = 'remove_lean_chats'
    ARCHIVE_LEAN_CHATS = 'archive_lean_chats'
    UNARCHIVE_LEAN_CHATS = 'unarchive_lean_chats'

    CREATE_AND_USE_ORCHESTRATION_CHATS = 'create_and_use_orchestration_chats'
    REMOVE_ORCHESTRATION_CHATS = 'remove_orchestration_chats'

    CREATE_SUPPORT_TICKETS = 'create_support_tickets'
    LIST_SUPPORT_TICKETS = 'list_support_tickets'
    UPDATE_SUPPORT_TICKETS = 'update_support_tickets'

    CREATE_USER_ROLES = 'create_user_roles'
    LIST_USER_ROLES = 'list_user_roles'
    UPDATE_USER_ROLES = 'update_user_roles'
    DELETE_USER_ROLES = 'delete_user_roles'

    CREATE_DATA_BACKUPS = 'create_data_backups'
    LIST_DATA_BACKUPS = 'list_data_backups'
    DELETE_DATA_BACKUPS = 'delete_data_backups'
    RESTORE_DATA_BACKUPS = 'restore_data_backups'

    CREATE_BRAINSTORMING_SESSIONS = 'create_brainstorming_sessions'
    LIST_BRAINSTORMING_SESSIONS = 'list_brainstorming_sessions'
    UPDATE_BRAINSTORMING_SESSIONS = 'update_brainstorming_sessions'
    DELETE_BRAINSTORMING_SESSIONS = 'delete_brainstorming_sessions'
    CREATE_BRAINSTORMING_IDEAS = 'create_brainstorming_ideas'
    DELETE_BRAINSTORMING_IDEAS = 'delete_brainstorming_ideas'
    CREATE_BRAINSTORMING_SYNTHESES = 'create_brainstorming_syntheses'
    BOOKMARK_BRAINSTORMING_IDEAS = 'bookmark_brainstorming_ideas'

    CREATE_VIDEO_GENERATOR_CONNECTIONS = 'create_video_generator_connections'
    LIST_VIDEO_GENERATOR_CONNECTIONS = 'list_video_generator_connections'
    UPDATE_VIDEO_GENERATOR_CONNECTIONS = 'update_video_generator_connections'
    DELETE_VIDEO_GENERATOR_CONNECTIONS = 'delete_video_generator_connections'

    ADD_DRAFTING_FOLDERS = 'add_drafting_folders'
    UPDATE_DRAFTING_FOLDERS = 'update_drafting_folders'
    LIST_DRAFTING_FOLDERS = 'list_drafting_folders'
    DELETE_DRAFTING_FOLDERS = 'delete_drafting_folders'

    ADD_DRAFTING_DOCUMENTS = 'add_drafting_documents'
    UPDATE_DRAFTING_DOCUMENTS = 'update_drafting_documents'
    LIST_DRAFTING_DOCUMENTS = 'list_drafting_documents'
    DELETE_DRAFTING_DOCUMENTS = 'delete_drafting_documents'

    CREATE_HADRON_SYSTEMS = 'create_hadron_systems'
    LIST_HADRON_SYSTEMS = 'list_hadron_systems'
    UPDATE_HADRON_SYSTEMS = 'update_hadron_systems'
    DELETE_HADRON_SYSTEMS = 'delete_hadron_systems'

    CREATE_HADRON_NODES = 'create_hadron_nodes'
    LIST_HADRON_NODES = 'list_hadron_nodes'
    UPDATE_HADRON_NODES = 'update_hadron_nodes'
    DELETE_HADRON_NODES = 'delete_hadron_nodes'

    CREATE_HADRON_TOPICS = 'create_hadron_topics'
    LIST_HADRON_TOPICS = 'list_hadron_topics'
    UPDATE_HADRON_TOPICS = 'update_hadron_topics'
    DELETE_HADRON_TOPICS = 'delete_hadron_topics'

    DELETE_HADRON_NODE_EXECUTION_LOGS = 'delete_hadron_node_execution_logs'
    DELETE_HADRON_NODE_SASE_LOGS = 'delete_hadron_node_sase_logs'
    DELETE_HADRON_NODE_PUBLISH_HISTORY_LOGS = 'delete_hadron_node_publish_history_logs'
    DELETE_HADRON_TOPIC_MESSAGE_HISTORY_LOGS = 'delete_hadron_topic_message_history_logs'
    DELETE_HADRON_NODE_SPEECH_LOGS = 'delete_hadron_node_speech_logs'

    CREATE_BLOCKCHAIN_WALLET_CONNECTIONS = 'create_blockchain_wallet_connections'
    LIST_BLOCKCHAIN_WALLET_CONNECTIONS = 'list_blockchain_wallet_connections'
    UPDATE_BLOCKCHAIN_WALLET_CONNECTIONS = 'update_blockchain_wallet_connections'
    DELETE_BLOCKCHAIN_WALLET_CONNECTIONS = 'delete_blockchain_wallet_connections'

    CREATE_SMART_CONTRACTS = 'create_smart_contracts'
    LIST_SMART_CONTRACTS = 'list_smart_contracts'
    SOFT_DELETE_SMART_CONTRACTS = 'soft_delete_smart_contracts'

    CREATE_INTERNAL_NOTIFICATIONS = 'create_internal_notifications'
    DELETE_INTERNAL_NOTIFICATIONS = 'delete_internal_notifications'

    CREATE_BINEXUS_PROCESSES = 'create_binexus_processes'
    LIST_BINEXUS_PROCESSES = 'list_binexus_processes'
    UPDATE_BINEXUS_PROCESSES = 'update_binexus_processes'
    DELETE_BINEXUS_PROCESSES = 'delete_binexus_processes'
    EXECUTE_BINEXUS_PROCESSES = 'execute_binexus_processes'

    DELETE_BINEXUS_ELITES = 'delete_binexus_elites'
    LIST_BINEXUS_ELITES = 'list_binexus_elites'


PERMISSION_TYPES = [
    ('add_organizations', 'Add Organizations'),
    ('update_organizations', 'Update Organizations'),
    ('list_organizations', 'List Organizations'),
    ('delete_organizations', 'Delete Organizations'),
    ('add_balance_to_organization', 'Add Balance to Organization'),
    ('transfer_balance_between_organizations', 'Transfer Balance Between Organizations'),

    ('add_projects', 'Add Projects'),
    ('update_projects', 'Update Projects'),
    ('list_projects', 'List Projects'),
    ('delete_projects', 'Delete Projects'),

    ('add_teams', 'Add Teams'),
    ('update_teams', 'Update Teams'),
    ('list_teams', 'List Teams'),
    ('delete_teams', 'Delete Teams'),

    ('add_metakanban_board', 'Add MetaKanban Board'),
    ('update_metakanban_board', 'Update MetaKanban Board'),
    ('list_metakanban_board', 'List MetaKanban Board'),
    ('delete_metakanban_board', 'Delete MetaKanban Board'),

    ('add_metakanban_task_label', 'Add MetaKanban Task Label'),
    ('update_metakanban_task_label', 'Update MetaKanban Task Label'),
    ('list_metakanban_task_label', 'List MetaKanban Task Label'),
    ('delete_metakanban_task_label', 'Delete MetaKanban Task Label'),

    ('add_metakanban_column', 'Add MetaKanban Column'),
    ('update_metakanban_column', 'Update MetaKanban Column'),
    ('delete_metakanban_column', 'Delete MetaKanban Column'),
    ('move_metakanban_column', 'Move MetaKanban Column'),

    ('add_metakanban_task', 'Add MetaKanban Task'),
    ('update_metakanban_task', 'Update MetaKanban Task'),
    ('delete_metakanban_task', 'Delete MetaKanban Task'),
    ('move_metakanban_task', 'Move MetaKanban Task'),
    ('assign_metakanban_task', 'Assign MetaKanban Task'),

    ('use_metakanban_ai', 'Use MetaKanban AI'),

    ('add_llm_cores', 'Add LLM Cores'),
    ('update_llm_cores', 'Update LLM Cores'),
    ('list_llm_cores', 'List LLM Cores'),
    ('delete_llm_cores', 'Delete LLM Cores'),

    ('list_transactions', 'List Transactions'),

    ('add_users', 'Add Users'),
    ('update_users', 'Update Users'),
    ('list_users', 'List Users'),
    ('delete_users', 'Delete Users'),
    ('connect_user_to_organization', 'Connect User to Organization'),
    ('remove_user_from_organization', 'Remove User from Organization'),

    ('modify_user_permissions', 'Modify User Permissions'),
    ('list_user_permissions', 'List User Permissions'),

    ('add_assistants', 'Add Assistants'),
    ('update_assistants', 'Update Assistants'),
    ('list_assistants', 'List Assistants'),
    ('delete_assistants', 'Delete Assistants'),

    ('add_harmoniq_agents', 'Add Harmoniq Agents'),
    ('update_harmoniq_agents', 'Update Harmoniq Agents'),
    ('list_harmoniq_agents', 'List Harmoniq Agents'),
    ('delete_harmoniq_agents', 'Delete Harmoniq Agents'),
    ('chat_with_harmoniq_agents', 'Chat with Harmoniq Agents'),

    ('create_and_use_chats', 'Create and Use Chats'),
    ('remove_chats', 'Remove Chats'),

    ('add_assistant_memories', 'Add Assistant Memories'),
    ('update_assistant_memories', 'Update Assistant Memories'),
    ('list_assistant_memories', 'List Assistant Memories'),
    ('delete_assistant_memories', 'Delete Assistant Memories'),

    ('add_export_assistant', 'Add Export Assistant'),
    ('update_export_assistant', 'Update Export Assistant'),
    ('list_export_assistant', 'List Export Assistant'),
    ('delete_export_assistant', 'Delete Export Assistant'),

    ('add_orchestrations', 'Add Orchestrations'),
    ('update_orchestrations', 'Update Orchestrations'),
    ('list_orchestrations', 'List Orchestrations'),
    ('delete_orchestrations', 'Delete Orchestrations'),

    ('add_file_systems', 'Add File Systems'),
    ('update_file_systems', 'Update File Systems'),
    ('list_file_systems', 'List File Systems'),
    ('delete_file_systems', 'Delete File Systems'),

    ('add_web_browsers', 'Add Web Browsers'),
    ('update_web_browsers', 'Update Web Browsers'),
    ('list_web_browsers', 'List Web Browsers'),
    ('delete_web_browsers', 'Delete Web Browsers'),

    ('add_sql_databases', 'Add SQL Databases'),
    ('update_sql_databases', 'Update SQL Databases'),
    ('list_sql_databases', 'List SQL Databases'),
    ('delete_sql_databases', 'Delete SQL Databases'),

    ('add_nosql_databases', 'Add NoSQL Databases'),
    ('update_nosql_databases', 'Update NoSQL Databases'),
    ('list_nosql_databases', 'List NoSQL Databases'),
    ('delete_nosql_databases', 'Delete NoSQL Databases'),

    ('add_custom_nosql_queries', 'Add Custom NoSQL Queries'),
    ('update_custom_nosql_queries', 'Update Custom NoSQL Queries'),
    ('list_custom_nosql_queries', 'List Custom NoSQL Queries'),
    ('delete_custom_nosql_queries', 'Delete Custom NoSQL Queries'),

    ('add_knowledge_bases', 'Add Knowledge Bases'),
    ('update_knowledge_bases', 'Update Knowledge Bases'),
    ('list_knowledge_bases', 'List Knowledge Bases'),
    ('delete_knowledge_bases', 'Delete Knowledge Bases'),

    ('add_media_storages', 'Add Media Storages'),
    ('update_media_storages', 'Update Media Storages'),
    ('list_media_storages', 'List Media Storages'),
    ('delete_media_storages', 'Delete Media Storages'),

    ('add_ml_model_connections', 'Add ML Model Connections'),
    ('update_ml_model_connections', 'Update ML Model Connections'),
    ('list_ml_model_connections', 'List ML Model Connections'),
    ('delete_ml_model_connections', 'Delete ML Model Connections'),

    ('add_functions', 'Add Functions'),
    ('update_functions', 'Update Functions'),
    ('list_functions', 'List Functions'),
    ('delete_functions', 'Delete Functions'),

    ('add_apis', 'Add APIs'),
    ('update_apis', 'Update APIs'),
    ('list_apis', 'List APIs'),
    ('delete_apis', 'Delete APIs'),

    ('add_scripts', 'Add Scripts'),
    ('update_scripts', 'Update Scripts'),
    ('list_scripts', 'List Scripts'),
    ('delete_scripts', 'Delete Scripts'),

    ('add_scheduled_jobs', 'Add Scheduled Jobs'),
    ('update_scheduled_jobs', 'Update Scheduled Jobs'),
    ('list_scheduled_jobs', 'List Scheduled Jobs'),
    ('delete_scheduled_jobs', 'Delete Scheduled Jobs'),

    ('add_triggers', 'Add Triggers'),
    ('update_triggers', 'Update Triggers'),
    ('list_triggers', 'List Triggers'),
    ('delete_triggers', 'Delete Triggers'),

    ('can_generate_images', 'Can Generate Images'),

    ('can_generate_audio', 'Can Generate Audio'),

    ('add_integrations', 'Add Integrations'),
    ('update_integrations', 'Update Integrations'),
    ('list_integrations', 'List Integrations'),
    ('delete_integrations', 'Delete Integrations'),

    ('add_meta_integrations', 'Add Meta Integrations'),
    ('update_meta_integrations', 'Update Meta Integrations'),
    ('list_meta_integrations', 'List Meta Integrations'),
    ('delete_meta_integrations', 'Delete Meta Integrations'),

    ('add_starred_messages', 'Add Starred Messages'),
    ('list_starred_messages', 'List Starred Messages'),
    ('remove_starred_messages', 'Remove Starred Messages'),

    ('add_template_messages', 'Add Template Messages'),
    ('list_template_messages', 'List Template Messages'),
    ('update_template_messages', 'Update Template Messages'),
    ('remove_template_messages', 'Remove Template Messages'),

    ('add_data_security', 'Add Data Security'),
    ('update_data_security', 'Update Data Security'),
    ('list_data_security', 'List Data Security'),
    ('delete_data_security', 'Delete Data Security'),

    ('add_code_base', 'Add Code Base'),
    ('update_code_base', 'Update Code Base'),
    ('list_code_base', 'List Code Base'),
    ('delete_code_base', 'Delete Code Base'),

    ('add_code_repository', 'Add Code Repository'),
    ('update_code_repository', 'Update Code Repository'),
    ('list_code_repository', 'List Code Repository'),
    ('delete_code_repository', 'Delete Code Repository'),

    ('add_knowledge_base_docs', 'Add Knowledge Base Docs'),
    ('update_knowledge_base_docs', 'Update Knowledge Base Docs'),
    ('list_knowledge_base_docs', 'List Knowledge Base Docs'),
    ('delete_knowledge_base_docs', 'Delete Knowledge Base Docs'),

    ('add_storage_files', 'Add Storage Files'),
    ('update_storage_files', 'Update Storage Files'),
    ('list_storage_files', 'List Storage Files'),
    ('delete_storage_files', 'Delete Storage Files'),

    ('add_ml_model_files', 'Add ML Model Files'),
    ('update_ml_model_files', 'Update ML Model Files'),
    ('list_ml_model_files', 'List ML Model Files'),
    ('delete_ml_model_files', 'Delete ML Model Files'),

    ('add_custom_sql_queries', 'Add Custom SQL Queries'),
    ('update_custom_sql_queries', 'Update Custom SQL Queries'),
    ('list_custom_sql_queries', 'List Custom SQL Queries'),
    ('delete_custom_sql_queries', 'Delete Custom SQL Queries'),

    ('add_export_leanmod', 'Add Export LeanMod'),
    ('update_export_leanmod', 'Update Export LeanMod'),
    ('list_export_leanmod', 'List Export LeanMod'),
    ('delete_export_leanmod', 'Delete Export LeanMod'),

    ('add_expert_networks', 'Add Expert Networks'),
    ('update_expert_networks', 'Update Expert Networks'),
    ('list_expert_networks', 'List Expert Networks'),
    ('delete_expert_networks', 'Delete Expert Networks'),

    ('add_export_orchestration', 'Add Export Orchestration'),
    ('update_export_orchestration', 'Update Export Orchestration'),
    ('list_export_orchestration', 'List Export Orchestration'),
    ('delete_export_orchestration', 'Delete Export Orchestration'),

    ('add_finetuning_model', 'Add Finetuning Model'),
    ('update_finetuning_model', 'Update Finetuning Model'),
    ('list_finetuning_model', 'List Finetuning Model'),
    ('delete_finetuning_model', 'Delete Finetuning Model'),

    ('add_lean_assistant', 'Add Lean Assistant'),
    ('update_lean_assistant', 'Update Lean Assistant'),
    ('list_lean_assistant', 'List Lean Assistant'),
    ('delete_lean_assistant', 'Delete Lean Assistant'),

    ('archive_chats', 'Archive Chats'),
    ('unarchive_chats', 'Unarchive Chats'),

    ('create_and_use_lean_chats', 'Create and Use Lean Chats'),
    ('remove_lean_chats', 'Remove Lean Chats'),
    ('archive_lean_chats', 'Archive Lean Chats'),
    ('unarchive_lean_chats', 'Unarchive Lean Chats'),

    ('create_and_use_orchestration_chats', 'Create and Use Orchestration Chats'),
    ('remove_orchestration_chats', 'Remove Orchestration Chats'),

    ('create_support_tickets', 'Create Support Tickets'),
    ('list_support_tickets', 'List Support Tickets'),
    ('update_support_tickets', 'Update Support Tickets'),

    ('create_user_roles', 'Create User Roles'),
    ('list_user_roles', 'List User Roles'),
    ('update_user_roles', 'Update User Roles'),
    ('delete_user_roles', 'Delete User Roles'),

    ('create_data_backups', 'Create Data Backups'),
    ('list_data_backups', 'List Data Backups'),
    ('delete_data_backups', 'Delete Data Backups'),
    ('restore_data_backups', 'Restore Data Backups'),

    ('create_brainstorming_sessions', 'Create Brainstorming Sessions'),
    ('list_brainstorming_sessions', 'List Brainstorming Sessions'),
    ('update_brainstorming_sessions', 'Update Brainstorming Sessions'),
    ('delete_brainstorming_sessions', 'Delete Brainstorming Sessions'),
    ('create_brainstorming_ideas', 'Create Brainstorming Ideas'),
    ('delete_brainstorming_ideas', 'Delete Brainstorming Ideas'),
    ('create_brainstorming_syntheses', 'Create Brainstorming Syntheses'),
    ('bookmark_brainstorming_ideas', 'Bookmark Brainstorming Ideas'),

    ('create_video_generator_connections', 'Create Video Generator Connections'),
    ('list_video_generator_connections', 'List Video Generator Connections'),
    ('update_video_generator_connections', 'Update Video Generator Connections'),
    ('delete_video_generator_connections', 'Delete Video Generator Connections'),

    ('add_drafting_folders', 'Add Drafting Folders'),
    ('update_drafting_folders', 'Update Drafting Folders'),
    ('list_drafting_folders', 'List Drafting Folders'),
    ('delete_drafting_folders', 'Delete Drafting Folders'),

    ('add_drafting_documents', 'Add Drafting Documents'),
    ('update_drafting_documents', 'Update Drafting Documents'),
    ('list_drafting_documents', 'List Drafting Documents'),
    ('delete_drafting_documents', 'Delete Drafting Documents'),

    ('create_hadron_systems', 'Create Hadron Systems'),
    ('list_hadron_systems', 'List Hadron Systems'),
    ('update_hadron_systems', 'Update Hadron Systems'),
    ('delete_hadron_systems', 'Delete Hadron Systems'),

    ('create_hadron_nodes', 'Create Hadron Nodes'),
    ('list_hadron_nodes', 'List Hadron Nodes'),
    ('update_hadron_nodes', 'Update Hadron Nodes'),
    ('delete_hadron_nodes', 'Delete Hadron Nodes'),

    ('create_hadron_topics', 'Create Hadron Topics'),
    ('list_hadron_topics', 'List Hadron Topics'),
    ('update_hadron_topics', 'Update Hadron Topics'),
    ('delete_hadron_topics', 'Delete Hadron Topics'),

    ('delete_hadron_node_execution_logs', 'Delete Hadron Node Execution Logs'),
    ('delete_hadron_node_sase_logs', 'Delete Hadron Node SASE Logs'),
    ('delete_hadron_node_publish_history_logs', 'Delete Hadron Node Publish History Logs'),
    ('delete_hadron_topic_message_history_logs', 'Delete Hadron Topic Message History Logs'),
    ('delete_hadron_node_speech_logs', 'Delete Hadron Node Speech Logs'),

    ('create_blockchain_wallet_connections', 'Create Blockchain Wallet Connections'),
    ('list_blockchain_wallet_connections', 'List Blockchain Wallet Connections'),
    ('update_blockchain_wallet_connections', 'Update Blockchain Wallet Connections'),
    ('delete_blockchain_wallet_connections', 'Delete Blockchain Wallet Connections'),

    ('create_smart_contracts', 'Create Smart Contracts'),
    ('list_smart_contracts', 'List Smart Contracts'),
    ('soft_delete_smart_contracts', 'Soft Delete Smart Contracts'),

    ('create_internal_notifications', 'Create Internal Notifications'),
    ('delete_internal_notifications', 'Delete Internal Notifications'),

    ('create_binexus_processes', 'Create Binexus Processes'),
    ('list_binexus_processes', 'List Binexus Processes'),
    ('update_binexus_processes', 'Update Binexus Processes'),
    ('delete_binexus_processes', 'Delete Binexus Processes'),
    ('execute_binexus_processes', 'Execute Binexus Processes'),

    ('delete_binexus_elites', 'Delete Binexus Elites'),
    ('list_binexus_elites', 'List Binexus Elites'),
]


class PredefinedRolePackages:
    ADMIN_ALL_PACKAGE = PERMISSION_TYPES

    READ_ALL_PACKAGE = [
        ('list_organizations', 'List Organizations'),
        ('list_llm_cores', 'List LLM Cores'),
        ('list_transactions', 'List Transactions'),
        ('list_users', 'List Users'),
        ('list_user_permissions', 'List User Permissions'),
        ('list_assistants', 'List Assistants'),
        ('list_assistant_memories', 'List Assistant Memories'),
        ('list_export_assistant', 'List Export Assistant'),
        ('list_orchestrations', 'List Orchestrations'),
        ('list_file_systems', 'List File Systems'),
        ('list_web_browsers', 'List Web Browsers'),
        ('list_sql_databases', 'List SQL Databases'),
        ('list_nosql_databases', 'List NoSQL Databases'),
        ('list_knowledge_bases', 'List Knowledge Bases'),
        ('list_media_storages', 'List Media Storages'),
        ('list_ml_model_connections', 'List ML Model Connections'),
        ('list_functions', 'List Functions'),
        ('list_apis', 'List APIs'),
        ('list_scripts', 'List Scripts'),
        ('list_scheduled_jobs', 'List Scheduled Jobs'),
        ('list_triggers', 'List Triggers'),
        ('list_integrations', 'List Integrations'),
        ('list_meta_integrations', 'List Meta Integrations'),
        ('list_starred_messages', 'List Starred Messages'),
        ('list_template_messages', 'List Template Messages'),
        ('list_data_security', 'List Data Security'),
        ('list_code_base', 'List Code Base'),
        ('list_code_repository', 'List Code Repository'),
        ('list_knowledge_base_docs', 'List Knowledge Base Docs'),
        ('list_storage_files', 'List Storage Files'),
        ('list_ml_model_files', 'List ML Model Files'),
        ('list_custom_sql_queries', 'List Custom SQL Queries'),
        ('list_export_leanmod', 'List Export LeanMod'),
        ('list_expert_networks', 'List Expert Networks'),
        ('list_export_orchestration', 'List Export Orchestration'),
        ('list_finetuning_model', 'List Finetuning Model'),
        ('list_lean_assistant', 'List Lean Assistant'),
        ('list_support_tickets', 'List Support Tickets'),
        ('list_user_roles', 'List User Roles'),
    ]

    CHAT_PACKAGE = [
        ('create_and_use_chats', 'Create and Use Chats'),
        ('remove_chats', 'Remove Chats'),
        ('archive_chats', 'Archive Chats'),
        ('unarchive_chats', 'Unarchive Chats'),
        ('create_and_use_lean_chats', 'Create and Use Lean Chats'),
        ('remove_lean_chats', 'Remove Lean Chats'),
        ('archive_lean_chats', 'Archive Lean Chats'),
        ('unarchive_lean_chats', 'Unarchive Lean Chats'),
        ('create_and_use_orchestration_chats', 'Create and Use Orchestration Chats'),
        ('remove_orchestration_chats', 'Remove Orchestration Chats'),
    ]

    SUPPORT_TICKET_PACKAGE = [
        ('create_support_tickets', 'Create Support Tickets'),
        ('list_support_tickets', 'List Support Tickets'),
        ('update_support_tickets', 'Update Support Tickets'),
    ]

    ADMIN_ORGANIZATION_PACKAGE = [
        ('add_organizations', 'Add Organizations'),
        ('update_organizations', 'Update Organizations'),
        ('list_organizations', 'List Organizations'),
        ('delete_organizations', 'Delete Organizations'),
        ('add_balance_to_organization', 'Add Balance to Organization'),
        ('transfer_balance_between_organizations', 'Transfer Balance Between Organizations'),
    ]

    MODERATOR_ORGANIZATION_PACKAGE = [
        ('update_organizations', 'Update Organizations'),
        ('list_organizations', 'List Organizations'),
        ('add_balance_to_organization', 'Add Balance to Organization'),
        ('transfer_balance_between_organizations', 'Transfer Balance Between Organizations'),
    ]

    ADMIN_LLM_CORE_PACKAGE = [
        ('add_llm_cores', 'Add LLM Cores'),
        ('update_llm_cores', 'Update LLM Cores'),
        ('list_llm_cores', 'List LLM Cores'),
        ('delete_llm_cores', 'Delete LLM Cores'),
    ]

    MODERATOR_LLM_CORE_PACKAGE = [
        ('update_llm_cores', 'Update LLM Cores'),
        ('list_llm_cores', 'List LLM Cores'),
    ]

    ADMIN_TRANSACTION_PACKAGE = [
        ('list_transactions', 'List Transactions'),
    ]

    ADMIN_USER_PACKAGE = [
        ('add_users', 'Add Users'),
        ('update_users', 'Update Users'),
        ('list_users', 'List Users'),
        ('delete_users', 'Delete Users'),
        ('connect_user_to_organization', 'Connect User to Organization'),
        ('remove_user_from_organization', 'Remove User from Organization'),
    ]

    MODERATOR_USER_PACKAGE = [
        ('update_users', 'Update Users'),
        ('list_users', 'List Users'),
        ('connect_user_to_organization', 'Connect User to Organization'),
        ('remove_user_from_organization', 'Remove User from Organization'),
    ]

    ADMIN_USER_PERMISSIONS_PACKAGE = [
        ('modify_user_permissions', 'Modify User Permissions'),
        ('list_user_permissions', 'List User Permissions'),
    ]

    ADMIN_USER_ROLES_PACKAGE = [
        ('create_user_roles', 'Create User Roles'),
        ('list_user_roles', 'List User Roles'),
        ('update_user_roles', 'Update User Roles'),
        ('delete_user_roles', 'Delete User Roles'),
    ]

    MODERATOR_USER_ROLES_PACKAGE = [
        ('list_user_roles', 'List User Roles'),
        ('update_user_roles', 'Update User Roles'),
    ]

    ADMIN_ASSISTANT_PACKAGE = [
        ('add_assistants', 'Add Assistants'),
        ('update_assistants', 'Update Assistants'),
        ('list_assistants', 'List Assistants'),
        ('delete_assistants', 'Delete Assistants'),
    ]

    MODERATOR_ASSISTANT_PACKAGE = [
        ('update_assistants', 'Update Assistants'),
        ('list_assistants', 'List Assistants'),
    ]

    ADMIN_MEMORY_PACKAGE = [
        ('add_assistant_memories', 'Add Assistant Memories'),
        ('update_assistant_memories', 'Update Assistant Memories'),
        ('list_assistant_memories', 'List Assistant Memories'),
        ('delete_assistant_memories', 'Delete Assistant Memories'),
    ]

    MODERATOR_MEMORY_PACKAGE = [
        ('update_assistant_memories', 'Update Assistant Memories'),
        ('list_assistant_memories', 'List Assistant Memories'),
    ]

    ADMIN_EXPORT_ASSISTANT_PACKAGE = [
        ('add_export_assistant', 'Add Export Assistant'),
        ('update_export_assistant', 'Update Export Assistant'),
        ('list_export_assistant', 'List Export Assistant'),
        ('delete_export_assistant', 'Delete Export Assistant'),
    ]

    MODERATOR_EXPORT_ASSISTANT_PACKAGE = [
        ('update_export_assistant', 'Update Export Assistant'),
        ('list_export_assistant', 'List Export Assistant'),
    ]

    ADMIN_EXPORT_LEANMOD_PACKAGE = [
        ('add_export_leanmod', 'Add Export LeanMod'),
        ('update_export_leanmod', 'Update Export LeanMod'),
        ('list_export_leanmod', 'List Export LeanMod'),
        ('delete_export_leanmod', 'Delete Export LeanMod'),
    ]

    MODERATOR_EXPORT_LEANMOD_PACKAGE = [
        ('update_export_leanmod', 'Update Export LeanMod'),
        ('list_export_leanmod', 'List Export LeanMod'),
    ]

    ADMIN_ORCHESTRATION_PACKAGE = [
        ('add_orchestrations', 'Add Orchestrations'),
        ('update_orchestrations', 'Update Orchestrations'),
        ('list_orchestrations', 'List Orchestrations'),
        ('delete_orchestrations', 'Delete Orchestrations'),
    ]

    MODERATOR_ORCHESTRATION_PACKAGE = [
        ('update_orchestrations', 'Update Orchestrations'),
        ('list_orchestrations', 'List Orchestrations'),
    ]

    ADMIN_FILE_SYSTEM_PACKAGE = [
        ('add_file_systems', 'Add File Systems'),
        ('update_file_systems', 'Update File Systems'),
        ('list_file_systems', 'List File Systems'),
        ('delete_file_systems', 'Delete File Systems'),
    ]

    MODERATOR_FILE_SYSTEM_PACKAGE = [
        ('update_file_systems', 'Update File Systems'),
        ('list_file_systems', 'List File Systems'),
    ]

    ADMIN_WEB_BROWSER_PACKAGE = [
        ('add_web_browsers', 'Add Web Browsers'),
        ('update_web_browsers', 'Update Web Browsers'),
        ('list_web_browsers', 'List Web Browsers'),
        ('delete_web_browsers', 'Delete Web Browsers'),
    ]

    MODERATOR_WEB_BROWSER_PACKAGE = [
        ('update_web_browsers', 'Update Web Browsers'),
        ('list_web_browsers', 'List Web Browsers'),
    ]

    ADMIN_SQL_DATABASE_PACKAGE = [
        ('add_sql_databases', 'Add SQL Databases'),
        ('update_sql_databases', 'Update SQL Databases'),
        ('list_sql_databases', 'List SQL Databases'),
        ('delete_sql_databases', 'Delete SQL Databases'),
    ]

    MODERATOR_SQL_DATABASE_PACKAGE = [
        ('update_sql_databases', 'Update SQL Databases'),
        ('list_sql_databases', 'List SQL Databases'),
    ]

    ADMIN_NOSQL_DATABASE_PACKAGE = [
        ('add_nosql_databases', 'Add NoSQL Databases'),
        ('update_nosql_databases', 'Update NoSQL Databases'),
        ('list_nosql_databases', 'List NoSQL Databases'),
        ('delete_nosql_databases', 'Delete NoSQL Databases'),
    ]

    MODERATOR_NOSQL_DATABASE_PACKAGE = [
        ('update_nosql_databases', 'Update NoSQL Databases'),
        ('list_nosql_databases', 'List NoSQL Databases'),
    ]

    ADMIN_KNOWLEDGE_BASE_PACKAGE = [
        ('add_knowledge_bases', 'Add Knowledge Bases'),
        ('update_knowledge_bases', 'Update Knowledge Bases'),
        ('list_knowledge_bases', 'List Knowledge Bases'),
        ('delete_knowledge_bases', 'Delete Knowledge Bases'),
    ]

    MODERATOR_KNOWLEDGE_BASE_PACKAGE = [
        ('update_knowledge_bases', 'Update Knowledge Bases'),
        ('list_knowledge_bases', 'List Knowledge Bases'),
    ]

    ADMIN_MEDIA_STORAGE_PACKAGE = [
        ('add_media_storages', 'Add Media Storages'),
        ('update_media_storages', 'Update Media Storages'),
        ('list_media_storages', 'List Media Storages'),
        ('delete_media_storages', 'Delete Media Storages'),
    ]

    MODERATOR_MEDIA_STORAGE_PACKAGE = [
        ('update_media_storages', 'Update Media Storages'),
        ('list_media_storages', 'List Media Storages'),
    ]

    ADMIN_ML_MODEL_CONNECTION_PACKAGE = [
        ('add_ml_model_connections', 'Add ML Model Connections'),
        ('update_ml_model_connections', 'Update ML Model Connections'),
        ('list_ml_model_connections', 'List ML Model Connections'),
        ('delete_ml_model_connections', 'Delete ML Model Connections'),
    ]

    MODERATOR_ML_MODEL_CONNECTION_PACKAGE = [
        ('update_ml_model_connections', 'Update ML Model Connections'),
        ('list_ml_model_connections', 'List ML Model Connections'),
    ]

    ADMIN_FUNCTION_PACKAGE = [
        ('add_functions', 'Add Functions'),
        ('update_functions', 'Update Functions'),
        ('list_functions', 'List Functions'),
        ('delete_functions', 'Delete Functions'),
    ]

    MODERATOR_FUNCTION_PACKAGE = [
        ('update_functions', 'Update Functions'),
        ('list_functions', 'List Functions'),
    ]

    ADMIN_API_PACKAGE = [
        ('add_apis', 'Add APIs'),
        ('update_apis', 'Update APIs'),
        ('list_apis', 'List APIs'),
        ('delete_apis', 'Delete APIs'),
    ]

    MODERATOR_API_PACKAGE = [
        ('update_apis', 'Update APIs'),
        ('list_apis', 'List APIs'),
    ]

    ADMIN_SCRIPT_PACKAGE = [
        ('add_scripts', 'Add Scripts'),
        ('update_scripts', 'Update Scripts'),
        ('list_scripts', 'List Scripts'),
        ('delete_scripts', 'Delete Scripts'),
    ]

    MODERATOR_SCRIPT_PACKAGE = [
        ('update_scripts', 'Update Scripts'),
        ('list_scripts', 'List Scripts'),
    ]

    ADMIN_SCHEDULED_JOB_PACKAGE = [
        ('add_scheduled_jobs', 'Add Scheduled Jobs'),
        ('update_scheduled_jobs', 'Update Scheduled Jobs'),
        ('list_scheduled_jobs', 'List Scheduled Jobs'),
        ('delete_scheduled_jobs', 'Delete Scheduled Jobs'),
    ]

    MODERATOR_SCHEDULED_JOB_PACKAGE = [
        ('update_scheduled_jobs', 'Update Scheduled Jobs'),
        ('list_scheduled_jobs', 'List Scheduled Jobs'),
    ]

    ADMIN_TRIGGER_PACKAGE = [
        ('add_triggers', 'Add Triggers'),
        ('update_triggers', 'Update Triggers'),
        ('list_triggers', 'List Triggers'),
        ('delete_triggers', 'Delete Triggers'),
    ]

    MODERATOR_TRIGGER_PACKAGE = [
        ('update_triggers', 'Update Triggers'),
        ('list_triggers', 'List Triggers'),
    ]

    ADMIN_IMAGE_GENERATION_PACKAGE = [
        ('can_generate_images', 'Can Generate Images'),
    ]

    MODERATOR_IMAGE_GENERATION_PACKAGE = [
        ('can_generate_images', 'Can Generate Images'),
    ]

    ADMIN_AUDIO_GENERATION_PACKAGE = [
        ('can_generate_audio', 'Can Generate Audio'),
    ]

    MODERATOR_AUDIO_GENERATION_PACKAGE = [
        ('can_generate_audio', 'Can Generate Audio'),
    ]

    ADMIN_INTEGRATION_PACKAGE = [
        ('add_integrations', 'Add Integrations'),
        ('update_integrations', 'Update Integrations'),
        ('list_integrations', 'List Integrations'),
        ('delete_integrations', 'Delete Integrations'),
    ]

    MODERATOR_INTEGRATION_PACKAGE = [
        ('update_integrations', 'Update Integrations'),
        ('list_integrations', 'List Integrations'),
    ]

    ADMIN_META_INTEGRATION_PACKAGE = [
        ('add_meta_integrations', 'Add Meta Integrations'),
        ('update_meta_integrations', 'Update Meta Integrations'),
        ('list_meta_integrations', 'List Meta Integrations'),
        ('delete_meta_integrations', 'Delete Meta Integrations'),
    ]

    MODERATOR_META_INTEGRATION_PACKAGE = [
        ('update_meta_integrations', 'Update Meta Integrations'),
        ('list_meta_integrations', 'List Meta Integrations'),
    ]

    ADMIN_STARRED_MESSAGES_PACKAGE = [
        ('add_starred_messages', 'Add Starred Messages'),
        ('list_starred_messages', 'List Starred Messages'),
        ('remove_starred_messages', 'Remove Starred Messages'),
    ]

    MODERATOR_STARRED_MESSAGES_PACKAGE = [
        ('list_starred_messages', 'List Starred Messages'),
    ]

    ADMIN_TEMPLATE_MESSAGES_PACKAGE = [
        ('add_template_messages', 'Add Template Messages'),
        ('list_template_messages', 'List Template Messages'),
        ('update_template_messages', 'Update Template Messages'),
        ('remove_template_messages', 'Remove Template Messages'),
    ]

    MODERATOR_TEMPLATE_MESSAGES_PACKAGE = [
        ('list_template_messages', 'List Template Messages'),
    ]

    ADMIN_DATA_SECURITY_PACKAGE = [
        ('add_data_security', 'Add Data Security'),
        ('update_data_security', 'Update Data Security'),
        ('list_data_security', 'List Data Security'),
        ('delete_data_security', 'Delete Data Security'),
    ]

    MODERATOR_DATA_SECURITY_PACKAGE = [
        ('update_data_security', 'Update Data Security'),
        ('list_data_security', 'List Data Security'),
    ]

    ADMIN_CODE_BASE_PACKAGE = [
        ('add_code_base', 'Add Code Base'),
        ('update_code_base', 'Update Code Base'),
        ('list_code_base', 'List Code Base'),
        ('delete_code_base', 'Delete Code Base'),
    ]

    MODERATOR_CODE_BASE_PACKAGE = [
        ('update_code_base', 'Update Code Base'),
        ('list_code_base', 'List Code Base'),
    ]

    ADMIN_CODE_REPOSITORY_PACKAGE = [
        ('add_code_repository', 'Add Code Repository'),
        ('update_code_repository', 'Update Code Repository'),
        ('list_code_repository', 'List Code Repository'),
        ('delete_code_repository', 'Delete Code Repository'),
    ]

    MODERATOR_CODE_REPOSITORY_PACKAGE = [
        ('update_code_repository', 'Update Code Repository'),
        ('list_code_repository', 'List Code Repository'),
    ]

    ADMIN_KNOWLEDGE_BASE_DOCS_PACKAGE = [
        ('add_knowledge_base_docs', 'Add Knowledge Base Docs'),
        ('update_knowledge_base_docs', 'Update Knowledge Base Docs'),
        ('list_knowledge_base_docs', 'List Knowledge Base Docs'),
        ('delete_knowledge_base_docs', 'Delete Knowledge Base Docs'),
    ]

    MODERATOR_KNOWLEDGE_BASE_DOCS_PACKAGE = [
        ('update_knowledge_base_docs', 'Update Knowledge Base Docs'),
        ('list_knowledge_base_docs', 'List Knowledge Base Docs'),
    ]

    ADMIN_STORAGE_FILES_PACKAGE = [
        ('add_storage_files', 'Add Storage Files'),
        ('update_storage_files', 'Update Storage Files'),
        ('list_storage_files', 'List Storage Files'),
        ('delete_storage_files', 'Delete Storage Files'),
    ]

    MODERATOR_STORAGE_FILES_PACKAGE = [
        ('update_storage_files', 'Update Storage Files'),
        ('list_storage_files', 'List Storage Files'),
    ]

    ADMIN_ML_MODEL_FILES_PACKAGE = [
        ('add_ml_model_files', 'Add ML Model Files'),
        ('update_ml_model_files', 'Update ML Model Files'),
        ('list_ml_model_files', 'List ML Model Files'),
        ('delete_ml_model_files', 'Delete ML Model Files'),
    ]

    MODERATOR_ML_MODEL_FILES_PACKAGE = [
        ('update_ml_model_files', 'Update ML Model Files'),
        ('list_ml_model_files', 'List ML Model Files'),
    ]

    ADMIN_CUSTOM_SQL_QUERIES_PACKAGE = [
        ('add_custom_sql_queries', 'Add Custom SQL Queries'),
        ('update_custom_sql_queries', 'Update Custom SQL Queries'),
        ('list_custom_sql_queries', 'List Custom SQL Queries'),
        ('delete_custom_sql_queries', 'Delete Custom SQL Queries'),
    ]

    MODERATOR_CUSTOM_SQL_QUERIES_PACKAGE = [
        ('update_custom_sql_queries', 'Update Custom SQL Queries'),
        ('list_custom_sql_queries', 'List Custom SQL Queries'),
    ]

    ADMIN_EXPERT_NETWORKS_PACKAGE = [
        ('add_expert_networks', 'Add Expert Networks'),
        ('update_expert_networks', 'Update Expert Networks'),
        ('list_expert_networks', 'List Expert Networks'),
        ('delete_expert_networks', 'Delete Expert Networks'),
    ]

    MODERATOR_EXPERT_NETWORKS_PACKAGE = [
        ('update_expert_networks', 'Update Expert Networks'),
        ('list_expert_networks', 'List Expert Networks'),
    ]

    ADMIN_EXPORT_ORCHESTRATION_PACKAGE = [
        ('add_export_orchestration', 'Add Export Orchestration'),
        ('update_export_orchestration', 'Update Export Orchestration'),
        ('list_export_orchestration', 'List Export Orchestration'),
        ('delete_export_orchestration', 'Delete Export Orchestration'),
    ]

    MODERATOR_EXPORT_ORCHESTRATION_PACKAGE = [
        ('update_export_orchestration', 'Update Export Orchestration'),
        ('list_export_orchestration', 'List Export Orchestration'),
    ]

    ADMIN_FINETUNING_MODEL_PACKAGE = [
        ('add_finetuning_model', 'Add Finetuning Model'),
        ('update_finetuning_model', 'Update Finetuning Model'),
        ('list_finetuning_model', 'List Finetuning Model'),
        ('delete_finetuning_model', 'Delete Finetuning Model'),
    ]

    MODERATOR_FINETUNING_MODEL_PACKAGE = [
        ('update_finetuning_model', 'Update Finetuning Model'),
        ('list_finetuning_model', 'List Finetuning Model'),
    ]

    ADMIN_LEAN_ASSISTANT_PACKAGE = [
        ('add_lean_assistant', 'Add Lean Assistant'),
        ('update_lean_assistant', 'Update Lean Assistant'),
        ('list_lean_assistant', 'List Lean Assistant'),
        ('delete_lean_assistant', 'Delete Lean Assistant'),
    ]

    MODERATOR_LEAN_ASSISTANT_PACKAGE = [
        ('update_lean_assistant', 'Update Lean Assistant'),
        ('list_lean_assistant', 'List Lean Assistant'),
    ]

    ADMIN_CHAT_ARCHIVING_PACKAGE = [
        ('archive_chats', 'Archive Chats'),
        ('unarchive_chats', 'Unarchive Chats'),
    ]

    MODERATOR_CHAT_ARCHIVING_PACKAGE = [
        ('archive_chats', 'Archive Chats'),
        ('unarchive_chats', 'Unarchive Chats'),
    ]

    ADMIN_LEAN_CHAT_PERMISSIONS_PACKAGE = [
        ('create_and_use_lean_chats', 'Create and Use Lean Chats'),
        ('remove_lean_chats', 'Remove Lean Chats'),
        ('archive_lean_chats', 'Archive Lean Chats'),
        ('unarchive_lean_chats', 'Unarchive Lean Chats'),
    ]

    MODERATOR_LEAN_CHAT_PERMISSIONS_PACKAGE = [
        ('create_and_use_lean_chats', 'Create and Use Lean Chats'),
        ('remove_lean_chats', 'Remove Lean Chats'),
        ('archive_lean_chats', 'Archive Lean Chats'),
        ('unarchive_lean_chats', 'Unarchive Lean Chats'),
    ]

    ADMIN_ORCHESTRATION_CHAT_PERMISSIONS_PACKAGE = [
        ('create_and_use_orchestration_chats', 'Create and Use Orchestration Chats'),
        ('remove_orchestration_chats', 'Remove Orchestration Chats'),
    ]

    MODERATOR_ORCHESTRATION_CHAT_PERMISSIONS_PACKAGE = [
        ('create_and_use_orchestration_chats', 'Create and Use Orchestration Chats'),
        ('remove_orchestration_chats', 'Remove Orchestration Chats'),
    ]


USER_PERMISSIONS_ADMIN_LIST = ("user", "permission_type", "created_at",)
USER_PERMISSIONS_ADMIN_FILTER = ("user", "permission_type", "created_at")
USER_PERMISSIONS_ADMIN_SEARCH = ("user", "permission_type")

USER_ROLES_ADMIN_LIST = (
    "organization",
    "role_name",
    "role_description",
    "created_at",
    "updated_at",
)
USER_ROLES_ADMIN_FILTER = (
    "organization",
    "created_at",
    "updated_at",
)
USER_ROLES_ADMIN_SEARCH = (
    "organization__name",
    "role_name",
    "role_description",
)
