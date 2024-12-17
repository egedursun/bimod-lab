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
    CONNECT_ASSISTANTS_TO_METAKANBAN = 'connect_assistants_to_metakanban'
    DISCONNECT_ASSISTANTS_FROM_METAKANBAN = 'disconnect_assistants_from_metakanban'

    USE_METAKANBAN_MEETING_TRANSCRIPTION = 'use_metakanban_meeting_transcription'
    IMPLEMENT_MEETING_TRANSCRIPTION_WITH_AI = 'implement_meeting_transcription_with_ai'
    DELETE_MEETING_TRANSCRIPTION = 'delete_meeting_transcription'

    ADD_METATEMPO_CONNECTION = 'add_metatempo_connection'
    UPDATE_METATEMPO_CONNECTION = 'update_metatempo_connection'
    LIST_METATEMPO_CONNECTION = 'list_metatempo_connection'
    DELETE_METATEMPO_CONNECTION = 'delete_metatempo_connection'

    USE_META_TEMPO_AI = 'use_meta_tempo_ai'
    CONNECT_ASSISTANTS_TO_METATEMPO = 'connect_assistants_to_metatempo'
    DISCONNECT_ASSISTANTS_FROM_METATEMPO = 'disconnect_assistants_from_metatempo'

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

    INTEGRATE_PLUG_AND_PLAY_AGENTS = 'integrate_plug_and_play_agents'
    LIST_PLUG_AND_PLAY_AGENTS = 'list_plug_and_play_agents'

    INTEGRATE_PLUG_AND_PLAY_TEAMS = 'integrate_plug_and_play_teams'
    LIST_PLUG_AND_PLAY_TEAMS = 'list_plug_and_play_teams'

    CREATE_AND_USE_CHATS = 'create_and_use_chats'
    REMOVE_CHATS = 'remove_chats'

    UPDATE_VOIDFORGER_CONFIGURATIONS = 'update_voidforger_configurations'
    REFRESH_VOIDFORGER_CONNECTIONS = 'refresh_voidforger_connections'
    TOGGLE_ACTIVATE_AND_DEACTIVATE_VOIDFORGER = 'toggle_activate_and_deactivate_voidforger'
    MANUALLY_TRIGGER_VOIDFORGER = 'manually_trigger_voidforger'
    LIST_VOIDFORGER_ACTION_MEMORY_LOGS = 'list_voidforger_action_logs'
    DELETE_VOIDFORGER_ACTION_MEMORY_LOGS = 'delete_voidforger_action_logs'
    LIST_VOIDFORGER_AUTO_EXECUTION_MEMORY_LOGS = 'list_voidforger_auto_execution_logs'
    DELETE_VOIDFORGER_AUTO_EXECUTION_MEMORY_LOGS = 'delete_voidforger_auto_execution_logs'
    CREATE_AND_USE_VOIDFORGER_CHATS = 'create_and_use_voidforger_chats'
    UPDATE_VOIDFORGER_CHAT_NAME = 'update_voidforger_chat_name'
    REMOVE_VOIDFORGER_CHATS = 'remove_voidforger_chats'

    ADD_EXPORT_VOIDFORGER = 'add_export_voidforger'
    UPDATE_EXPORT_VOIDFORGER = 'update_export_voidforger'
    LIST_EXPORT_VOIDFORGER = 'list_export_voidforger'
    DELETE_EXPORT_VOIDFORGER = 'delete_export_voidforger'

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
    CONNECT_REACTANT_ASSISTANTS_TO_ORCHESTRATION = 'connect_reactant_assistants_to_orchestration'
    DISCONNECT_REACTANT_ASSISTANTS_FROM_ORCHESTRATION = 'disconnect_reactant_assistants_from_orchestration'

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

    ADD_WEBSITE_STORAGES = 'add_website_storages'
    UPDATE_WEBSITE_STORAGES = 'update_website_storages'
    LIST_WEBSITE_STORAGES = 'list_website_storages'
    DELETE_WEBSITE_STORAGES = 'delete_website_storages'

    ADD_WEBSITE_ITEMS = 'add_website_items'
    UPDATE_WEBSITE_ITEMS = 'update_website_items'
    LIST_WEBSITE_ITEMS = 'list_website_items'
    DELETE_WEBSITE_ITEMS = 'delete_website_items'

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

    ADD_LEANMOD_SCHEDULED_JOBS = 'add_leanmod_scheduled_jobs'
    UPDATE_LEANMOD_SCHEDULED_JOBS = 'update_leanmod_scheduled_jobs'
    LIST_LEANMOD_SCHEDULED_JOBS = 'list_leanmod_scheduled_jobs'
    DELETE_LEANMOD_SCHEDULED_JOBS = 'delete_leanmod_scheduled_jobs'

    ADD_ORCHESTRATION_SCHEDULED_JOBS = 'add_orchestration_scheduled_jobs'
    UPDATE_ORCHESTRATION_SCHEDULED_JOBS = 'update_orchestration_scheduled_jobs'
    LIST_ORCHESTRATION_SCHEDULED_JOBS = 'list_orchestration_scheduled_jobs'
    DELETE_ORCHESTRATION_SCHEDULED_JOBS = 'delete_orchestration_scheduled_jobs'

    ADD_TRIGGERS = 'add_triggers'
    UPDATE_TRIGGERS = 'update_triggers'
    LIST_TRIGGERS = 'list_triggers'
    DELETE_TRIGGERS = 'delete_triggers'

    ADD_LEANMOD_TRIGGERS = 'add_leanmod_triggers'
    UPDATE_LEANMOD_TRIGGERS = 'update_leanmod_triggers'
    LIST_LEANMOD_TRIGGERS = 'list_leanmod_triggers'
    DELETE_LEANMOD_TRIGGERS = 'delete_leanmod_triggers'

    ADD_ORCHESTRATION_TRIGGERS = 'add_orchestration_triggers'
    UPDATE_ORCHESTRATION_TRIGGERS = 'update_orchestration_triggers'
    LIST_ORCHESTRATION_TRIGGERS = 'list_orchestration_triggers'
    DELETE_ORCHESTRATION_TRIGGERS = 'delete_orchestration_triggers'

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

    LIST_BEAMGUARD_ARTIFACTS = 'list_beamguard_artifacts'
    INTEGRATE_BEAMGUARD_ARTIFACTS = 'integrate_beamguard_artifacts'
    DISCARD_BEAMGUARD_ARTIFACTS = 'discard_beamguard_artifacts'

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

    INTEGRATE_ML_MODEL_FILES = 'integrate_ml_model_files'
    LIST_ML_MODEL_INTEGRATIONS = 'list_ml_model_integrations'

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

    CREATE_ELLMA_SCRIPTS = "create_ellma_scripts"
    LIST_ELLMA_SCRIPTS = "list_ellma_scripts"
    UPDATE_ELLMA_SCRIPTS = "update_ellma_scripts"
    DELETE_ELLMA_SCRIPTS = "delete_ellma_scripts"

    ADD_DRAFTING_FOLDERS = 'add_drafting_folders'
    UPDATE_DRAFTING_FOLDERS = 'update_drafting_folders'
    LIST_DRAFTING_FOLDERS = 'list_drafting_folders'
    DELETE_DRAFTING_FOLDERS = 'delete_drafting_folders'

    ADD_DRAFTING_DOCUMENTS = 'add_drafting_documents'
    UPDATE_DRAFTING_DOCUMENTS = 'update_drafting_documents'
    LIST_DRAFTING_DOCUMENTS = 'list_drafting_documents'
    DELETE_DRAFTING_DOCUMENTS = 'delete_drafting_documents'

    ADD_DRAFTING_GOOGLE_APPS_CONNECTIONS = 'add_drafting_google_apps_connections'
    LIST_DRAFTING_GOOGLE_APPS_CONNECTIONS = 'list_drafting_google_apps_connections'
    UPDATE_DRAFTING_GOOGLE_APPS_CONNECTIONS = 'update_drafting_google_apps_connections'
    DELETE_DRAFTING_GOOGLE_APPS_CONNECTIONS = 'delete_drafting_google_apps_connections'

    ADD_SHEETOS_FOLDERS = 'add_sheetos_folders'
    UPDATE_SHEETOS_FOLDERS = 'update_sheetos_folders'
    LIST_SHEETOS_FOLDERS = 'list_sheetos_folders'
    DELETE_SHEETOS_FOLDERS = 'delete_sheetos_folders'

    ADD_SHEETOS_DOCUMENTS = 'add_sheetos_documents'
    UPDATE_SHEETOS_DOCUMENTS = 'update_sheetos_documents'
    LIST_SHEETOS_DOCUMENTS = 'list_sheetos_documents'
    DELETE_SHEETOS_DOCUMENTS = 'delete_sheetos_documents'

    ADD_SHEETOS_GOOGLE_APPS_CONNECTIONS = 'add_sheetos_google_apps_connections'
    UPDATE_SHEETOS_GOOGLE_APPS_CONNECTIONS = 'update_sheetos_google_apps_connections'
    LIST_SHEETOS_GOOGLE_APPS_CONNECTIONS = 'list_sheetos_google_apps_connections'
    DELETE_SHEETOS_GOOGLE_APPS_CONNECTIONS = 'delete_sheetos_google_apps_connections'

    ADD_SLIDER_FOLDERS = 'add_slider_folders'
    UPDATE_SLIDER_FOLDERS = 'update_slider_folders'
    LIST_SLIDER_FOLDERS = 'list_slider_folders'
    DELETE_SLIDER_FOLDERS = 'delete_slider_folders'

    ADD_SLIDER_DOCUMENTS = 'add_slider_documents'
    UPDATE_SLIDER_DOCUMENTS = 'update_slider_documents'
    LIST_SLIDER_DOCUMENTS = 'list_slider_documents'
    DELETE_SLIDER_DOCUMENTS = 'delete_slider_documents'

    ADD_SLIDER_GOOGLE_APPS_CONNECTIONS = 'add_slider_google_apps_connections'
    UPDATE_SLIDER_GOOGLE_APPS_CONNECTIONS = 'update_slider_google_apps_connections'
    LIST_SLIDER_GOOGLE_APPS_CONNECTIONS = 'list_slider_google_apps_connections'
    DELETE_SLIDER_GOOGLE_APPS_CONNECTIONS = 'delete_slider_google_apps_connections'

    ADD_FORMICA_GOOGLE_APPS_CONNECTIONS = 'add_formica_google_apps_connections'
    UPDATE_FORMICA_GOOGLE_APPS_CONNECTIONS = 'update_formica_google_apps_connections'
    LIST_FORMICA_GOOGLE_APPS_CONNECTIONS = 'list_formica_google_apps_connections'
    DELETE_FORMICA_GOOGLE_APPS_CONNECTIONS = 'delete_formica_google_apps_connections'

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

    CONNECT_ASSISTANTS_TO_HADRON_NODE = 'connect_assistants_to_hadron_node'
    DISCONNECT_ASSISTANTS_FROM_HADRON_NODE = 'disconnect_assistants_from_hadron_node'

    CREATE_BLOCKCHAIN_WALLET_CONNECTIONS = 'create_blockchain_wallet_connections'
    LIST_BLOCKCHAIN_WALLET_CONNECTIONS = 'list_blockchain_wallet_connections'
    UPDATE_BLOCKCHAIN_WALLET_CONNECTIONS = 'update_blockchain_wallet_connections'
    DELETE_BLOCKCHAIN_WALLET_CONNECTIONS = 'delete_blockchain_wallet_connections'

    CREATE_SMART_CONTRACTS = 'create_smart_contracts'
    LIST_SMART_CONTRACTS = 'list_smart_contracts'
    SOFT_DELETE_SMART_CONTRACTS = 'soft_delete_smart_contracts'

    CONNECT_SMART_CONTRACTS_TO_ASSISTANT = 'connect_smart_contracts_to_assistant'
    DISCONNECT_SMART_CONTRACTS_FROM_ASSISTANT = 'disconnect_smart_contracts_from_assistant'

    CREATE_INTERNAL_NOTIFICATIONS = 'create_internal_notifications'
    DELETE_INTERNAL_NOTIFICATIONS = 'delete_internal_notifications'

    CREATE_BINEXUS_PROCESSES = 'create_binexus_processes'
    LIST_BINEXUS_PROCESSES = 'list_binexus_processes'
    UPDATE_BINEXUS_PROCESSES = 'update_binexus_processes'
    DELETE_BINEXUS_PROCESSES = 'delete_binexus_processes'
    EXECUTE_BINEXUS_PROCESSES = 'execute_binexus_processes'

    DELETE_BINEXUS_ELITES = 'delete_binexus_elites'
    LIST_BINEXUS_ELITES = 'list_binexus_elites'

    USE_SINAPTERA_CONFIGURATION = 'use_sinaptera_configuration'


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
    ('connect_assistants_to_metakanban', 'Connect Assistants to MetaKanban'),
    ('disconnect_assistants_from_metakanban', 'Disconnect Assistants from MetaKanban'),

    ("use_metakanban_meeting_transcription", "Use MetaKanban Meeting Transcription"),
    ("implement_meeting_transcription_with_ai", "Implement Meeting Transcription with AI"),
    ("delete_meeting_transcription", "Delete Meeting Transcription"),

    ('add_metatempo_connection', 'Add MetaTempo Connection'),
    ('update_metatempo_connection', 'Update MetaTempo Connection'),
    ('list_metatempo_connection', 'List MetaTempo Connection'),
    ('delete_metatempo_connection', 'Delete MetaTempo Connection'),

    ('use_meta_tempo_ai', 'Use MetaTempo AI'),
    ('connect_assistants_to_metatempo', 'Connect Assistants to MetaTempo'),
    ('disconnect_assistants_from_metatempo', 'Disconnect Assistants from MetaTempo'),

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

    ('integrate_plug_and_play_agents', 'Integrate Plug and Play Agents'),
    ('list_plug_and_play_agents', 'List Plug and Play Agents'),

    ('integrate_plug_and_play_teams', 'Integrate Plug and Play Teams'),
    ('list_plug_and_play_teams', 'List Plug and Play Teams'),

    ('create_and_use_chats', 'Create and Use Chats'),
    ('remove_chats', 'Remove Chats'),

    ('update_voidforger_configurations', 'Update VoidForger Configurations'),
    ('refresh_voidforger_connections', 'Refresh VoidForger Connections'),
    ('toggle_activate_and_deactivate_voidforger', 'Toggle Activate and Deactivate VoidForger'),
    ('manually_trigger_voidforger', 'Manually Trigger VoidForger'),
    ('list_voidforger_action_logs', 'List VoidForger Action Logs'),
    ('delete_voidforger_action_logs', 'Delete VoidForger Action Logs'),
    ('list_voidforger_auto_execution_logs', 'List VoidForger Auto Execution Logs'),
    ('delete_voidforger_auto_execution_logs', 'Delete VoidForger Auto Execution Logs'),
    ('create_and_use_voidforger_chats', 'Create and Use VoidForger Chats'),
    ('update_voidforger_chat_name', 'Update VoidForger Chat Name'),
    ('remove_voidforger_chats', 'Remove VoidForger Chats'),

    ('add_export_voidforger', 'Add Export VoidForger'),
    ('update_export_voidforger', 'Update Export VoidForger'),
    ('list_export_voidforger', 'List Export VoidForger'),
    ('delete_export_voidforger', 'Delete Export VoidForger'),

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
    ('connect_reactant_assistants_to_orchestration', 'Connect Reactant Assistants to Orchestration'),
    ('disconnect_reactant_assistants_from_orchestration', 'Disconnect Reactant Assistants from Orchestration'),

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

    ('add_website_storages', 'Add Website Storages'),
    ('update_website_storages', 'Update Website Storages'),
    ('list_website_storages', 'List Website Storages'),
    ('delete_website_storages', 'Delete Website Storages'),

    ('add_website_items', 'Add Website Items'),
    ('update_website_items', 'Update Website Items'),
    ('list_website_items', 'List Website Items'),
    ('delete_website_items', 'Delete Website Items'),

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

    ('add_leanmod_scheduled_jobs', 'Add LeanMod Scheduled Jobs'),
    ('update_leanmod_scheduled_jobs', 'Update LeanMod Scheduled Jobs'),
    ('list_leanmod_scheduled_jobs', 'List LeanMod Scheduled Jobs'),
    ('delete_leanmod_scheduled_jobs', 'Delete LeanMod Scheduled Jobs'),

    ('add_orchestration_scheduled_jobs', 'Add Orchestration Scheduled Jobs'),
    ('update_orchestration_scheduled_jobs', 'Update Orchestration Scheduled Jobs'),
    ('list_orchestration_scheduled_jobs', 'List Orchestration Scheduled Jobs'),
    ('delete_orchestration_scheduled_jobs', 'Delete Orchestration Scheduled Jobs'),

    ('add_triggers', 'Add Triggers'),
    ('update_triggers', 'Update Triggers'),
    ('list_triggers', 'List Triggers'),
    ('delete_triggers', 'Delete Triggers'),

    ('add_leanmod_triggers', 'Add LeanMod Triggers'),
    ('update_leanmod_triggers', 'Update LeanMod Triggers'),
    ('list_leanmod_triggers', 'List LeanMod Triggers'),
    ('delete_leanmod_triggers', 'Delete LeanMod Triggers'),

    ('add_orchestration_triggers', 'Add Orchestration Triggers'),
    ('update_orchestration_triggers', 'Update Orchestration Triggers'),
    ('list_orchestration_triggers', 'List Orchestration Triggers'),
    ('delete_orchestration_triggers', 'Delete Orchestration Triggers'),

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

    ('list_beamguard_artifacts', 'List BeamGuard Artifacts'),
    ('integrate_beamguard_artifacts', 'Integrate BeamGuard Artifacts'),
    ('discard_beamguard_artifacts', 'Discard BeamGuard Artifacts'),

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

    ('integrate_ml_model_files', 'Integrate ML Model Files'),
    ('list_ml_model_integrations', 'List ML Model Integrations'),

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

    ('create_ellma_scripts', 'Create Ellma Scripts'),
    ('list_ellma_scripts', 'List Ellma Scripts'),
    ('update_ellma_scripts', 'Update Ellma Scripts'),
    ('delete_ellma_scripts', 'Delete Ellma Scripts'),

    ('add_drafting_folders', 'Add Drafting Folders'),
    ('update_drafting_folders', 'Update Drafting Folders'),
    ('list_drafting_folders', 'List Drafting Folders'),
    ('delete_drafting_folders', 'Delete Drafting Folders'),

    ('add_drafting_documents', 'Add Drafting Documents'),
    ('update_drafting_documents', 'Update Drafting Documents'),
    ('list_drafting_documents', 'List Drafting Documents'),
    ('delete_drafting_documents', 'Delete Drafting Documents'),

    ('add_drafting_google_apps_connections', 'Add Drafting Google Apps Connections'),
    ('list_drafting_google_apps_connections', 'List Drafting Google Apps Connections'),
    ('update_drafting_google_apps_connections', 'Update Drafting Google Apps Connections'),
    ('delete_drafting_google_apps_connections', 'Delete Drafting Google Apps Connections'),

    ('add_sheetos_folders', 'Add Sheetos Folders'),
    ('update_sheetos_folders', 'Update Sheetos Folders'),
    ('list_sheetos_folders', 'List Sheetos Folders'),
    ('delete_sheetos_folders', 'Delete Sheetos Folders'),

    ('add_sheetos_documents', 'Add Sheetos Documents'),
    ('update_sheetos_documents', 'Update Sheetos Documents'),
    ('list_sheetos_documents', 'List Sheetos Documents'),
    ('delete_sheetos_documents', 'Delete Sheetos Documents'),

    ('add_sheetos_google_apps_connections', 'Add Sheetos Google Apps Connections'),
    ('update_sheetos_google_apps_connections', 'Update Sheetos Google Apps Connections'),
    ('list_sheetos_google_apps_connections', 'List Sheetos Google Apps Connections'),
    ('delete_sheetos_google_apps_connections', 'Delete Sheetos Google Apps Connections'),

    ('add_slider_folders', 'Add Slider Folders'),
    ('update_slider_folders', 'Update Slider Folders'),
    ('list_slider_folders', 'List Slider Folders'),
    ('delete_slider_folders', 'Delete Slider Folders'),

    ('add_slider_documents', 'Add Slider Documents'),
    ('update_slider_documents', 'Update Slider Documents'),
    ('list_slider_documents', 'List Slider Documents'),
    ('delete_slider_documents', 'Delete Slider Documents'),

    ('add_slider_google_apps_connections', 'Add Slider Google Apps Connections'),
    ('update_slider_google_apps_connections', 'Update Slider Google Apps Connections'),
    ('list_slider_google_apps_connections', 'List Slider Google Apps Connections'),
    ('delete_slider_google_apps_connections', 'Delete Slider Google Apps Connections'),

    ('add_formica_google_apps_connections', 'Add Formica Google Apps Connections'),
    ('update_formica_google_apps_connections', 'Update Formica Google Apps Connections'),
    ('list_formica_google_apps_connections', 'List Formica Google Apps Connections'),
    ('delete_formica_google_apps_connections', 'Delete Formica Google Apps Connections'),

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

    ('connect_assistants_to_hadron_node', 'Connect Assistants to Hadron Node'),
    ('disconnect_assistants_from_hadron_node', 'Disconnect Assistants from Hadron Node'),

    ('create_blockchain_wallet_connections', 'Create Blockchain Wallet Connections'),
    ('list_blockchain_wallet_connections', 'List Blockchain Wallet Connections'),
    ('update_blockchain_wallet_connections', 'Update Blockchain Wallet Connections'),
    ('delete_blockchain_wallet_connections', 'Delete Blockchain Wallet Connections'),

    ('create_smart_contracts', 'Create Smart Contracts'),
    ('list_smart_contracts', 'List Smart Contracts'),
    ('soft_delete_smart_contracts', 'Soft Delete Smart Contracts'),

    ('connect_smart_contracts_to_assistant', 'Connect Smart Contracts to Assistant'),
    ('disconnect_smart_contracts_from_assistant', 'Disconnect Smart Contracts from Assistant'),

    ('create_internal_notifications', 'Create Internal Notifications'),
    ('delete_internal_notifications', 'Delete Internal Notifications'),

    ('create_binexus_processes', 'Create Binexus Processes'),
    ('list_binexus_processes', 'List Binexus Processes'),
    ('update_binexus_processes', 'Update Binexus Processes'),
    ('delete_binexus_processes', 'Delete Binexus Processes'),
    ('execute_binexus_processes', 'Execute Binexus Processes'),

    ('delete_binexus_elites', 'Delete Binexus Elites'),
    ('list_binexus_elites', 'List Binexus Elites'),

    ('use_sinaptera_configuration', 'Use Sinaptera Configuration'),
]


class PredefinedRolePackages__Functional:

    class Names:
        SuperUserAdminRole = 'SuperUserAdminRole'
        CreationAdminRole = 'CreationAdminRole'
        ModificationAdminRole = 'ModificationAdminRole'
        ReadAdminRole = 'ReadAdminRole'
        DeletionAdminRole = 'DeletionAdminRole'

    class SuperUserAdminRole:
        @staticmethod
        def get():
            return PERMISSION_TYPES

    class CreationAdminRole:
        @staticmethod
        def get():
            return [
                ('add_projects', 'Add Projects'),
                ('add_teams', 'Add Teams'),
                ('add_metakanban_board', 'Add MetaKanban Board'),
                ('add_metakanban_task_label', 'Add MetaKanban Task Label'),
                ('add_metakanban_column', 'Add MetaKanban Column'),
                ('add_metakanban_task', 'Add MetaKanban Task'),
                ('assign_metakanban_task', 'Assign MetaKanban Task'),
                ('use_metakanban_ai', 'Use MetaKanban AI'),
                ('connect_assistants_to_metakanban', 'Connect Assistants to MetaKanban'),
                ("use_metakanban_meeting_transcription", "Use MetaKanban Meeting Transcription"),
                ("implement_meeting_transcription_with_ai", "Implement Meeting Transcription with AI"),
                ('add_metatempo_connection', 'Add MetaTempo Connection'),
                ('use_meta_tempo_ai', 'Use MetaTempo AI'),
                ('connect_assistants_to_metatempo', 'Connect Assistants to MetaTempo'),
                ('add_users', 'Add Users'),
                ('connect_user_to_organization', 'Connect User to Organization'),
                ('add_assistants', 'Add Assistants'),
                ('add_harmoniq_agents', 'Add Harmoniq Agents'),
                ('integrate_plug_and_play_agents', 'Integrate Plug and Play Agents'),
                ('integrate_plug_and_play_teams', 'Integrate Plug and Play Teams'),
                ('create_and_use_chats', 'Create and Use Chats'),
                ('refresh_voidforger_connections', 'Refresh VoidForger Connections'),
                ('toggle_activate_and_deactivate_voidforger', 'Toggle Activate and Deactivate VoidForger'),
                ('manually_trigger_voidforger', 'Manually Trigger VoidForger'),
                ('create_and_use_voidforger_chats', 'Create and Use VoidForger Chats'),
                ('add_assistant_memories', 'Add Assistant Memories'),
                ('add_export_assistant', 'Add Export Assistant'),
                ('add_orchestrations', 'Add Orchestrations'),
                ('connect_reactant_assistants_to_orchestration', 'Connect Reactant Assistants to Orchestration'),
                ('add_file_systems', 'Add File Systems'),
                ('add_web_browsers', 'Add Web Browsers'),
                ('add_sql_databases', 'Add SQL Databases'),
                ('add_nosql_databases', 'Add NoSQL Databases'),
                ('add_custom_nosql_queries', 'Add Custom NoSQL Queries'),
                ('add_knowledge_bases', 'Add Knowledge Bases'),
                ('add_media_storages', 'Add Media Storages'),
                ('add_ml_model_connections', 'Add ML Model Connections'),
                ('add_functions', 'Add Functions'),
                ('add_apis', 'Add APIs'),
                ('add_scripts', 'Add Scripts'),
                ('add_scheduled_jobs', 'Add Scheduled Jobs'),
                ('add_leanmod_scheduled_jobs', 'Add LeanMod Scheduled Jobs'),
                ('add_orchestration_scheduled_jobs', 'Add Orchestration Scheduled Jobs'),
                ('add_triggers', 'Add Triggers'),
                ('add_leanmod_triggers', 'Add LeanMod Triggers'),
                ('add_orchestration_triggers', 'Add Orchestration Triggers'),
                ('can_generate_images', 'Can Generate Images'),
                ('can_generate_audio', 'Can Generate Audio'),
                ('add_integrations', 'Add Integrations'),
                ('add_meta_integrations', 'Add Meta Integrations'),
                ('add_starred_messages', 'Add Starred Messages'),
                ('add_template_messages', 'Add Template Messages'),
                ('add_data_security', 'Add Data Security'),
                ('integrate_beamguard_artifacts', 'Integrate BeamGuard Artifacts'),
                ('add_code_base', 'Add Code Base'),
                ('add_code_repository', 'Add Code Repository'),
                ('add_website_storages', 'Add Website Storages'),
                ('add_website_items', 'Add Website Items'),
                ('add_knowledge_base_docs', 'Add Knowledge Base Docs'),
                ('add_storage_files', 'Add Storage Files'),
                ('add_ml_model_files', 'Add ML Model Files'),
                ('integrate_ml_model_files', 'Integrate ML Model Files'),
                ('add_custom_sql_queries', 'Add Custom SQL Queries'),
                ('add_export_leanmod', 'Add Export LeanMod'),
                ('add_expert_networks', 'Add Expert Networks'),
                ('add_export_orchestration', 'Add Export Orchestration'),
                ('add_export_voidforger', 'Add Export VoidForger'),
                ('add_finetuning_model', 'Add Finetuning Model'),
                ('add_lean_assistant', 'Add Lean Assistant'),
                ('archive_chats', 'Archive Chats'),
                ('unarchive_chats', 'Unarchive Chats'),
                ('create_and_use_lean_chats', 'Create and Use Lean Chats'),
                ('remove_lean_chats', 'Remove Lean Chats'),
                ('archive_lean_chats', 'Archive Lean Chats'),
                ('unarchive_lean_chats', 'Unarchive Lean Chats'),
                ('create_and_use_orchestration_chats', 'Create and Use Orchestration Chats'),
                ('create_support_tickets', 'Create Support Tickets'),
                ('create_user_roles', 'Create User Roles'),
                ('create_data_backups', 'Create Data Backups'),
                ('restore_data_backups', 'Restore Data Backups'),
                ('create_brainstorming_sessions', 'Create Brainstorming Sessions'),
                ('create_brainstorming_ideas', 'Create Brainstorming Ideas'),
                ('create_brainstorming_syntheses', 'Create Brainstorming Syntheses'),
                ('bookmark_brainstorming_ideas', 'Bookmark Brainstorming Ideas'),
                ('create_video_generator_connections', 'Create Video Generator Connections'),
                ('create_ellma_scripts', 'Create Ellma Scripts'),
                ('add_drafting_folders', 'Add Drafting Folders'),
                ('add_drafting_documents', 'Add Drafting Documents'),
                ('add_drafting_google_apps_connections', 'Add Drafting Google Apps Connections'),
                ('add_sheetos_folders', 'Add Sheetos Folders'),
                ('add_sheetos_documents', 'Add Sheetos Documents'),
                ('add_sheetos_google_apps_connections', 'Add Sheetos Google Apps Connections'),
                ('add_slider_folders', 'Add Slider Folders'),
                ('add_slider_documents', 'Add Slider Documents'),
                ('add_slider_google_apps_connections', 'Add Slider Google Apps Connections'),
                ('add_formica_google_apps_connections', 'Add Formica Google Apps Connections'),
                ('create_hadron_systems', 'Create Hadron Systems'),
                ('create_hadron_nodes', 'Create Hadron Nodes'),
                ('create_hadron_topics', 'Create Hadron Topics'),
                ('connect_assistants_to_hadron_node', 'Connect Assistants to Hadron Node'),
                ('create_blockchain_wallet_connections', 'Create Blockchain Wallet Connections'),
                ('create_smart_contracts', 'Create Smart Contracts'),
                ('connect_smart_contracts_to_assistant', 'Connect Smart Contracts to Assistant'),
                ('create_internal_notifications', 'Create Internal Notifications'),
                ('create_binexus_processes', 'Create Binexus Processes'),
                ('execute_binexus_processes', 'Execute Binexus Processes'),
                ('use_sinaptera_configuration', 'Use Sinaptera Configuration'),
            ]

    class ModificationAdminRole:
        @staticmethod
        def get():
            return [
                ('update_projects', 'Update Projects'),
                ('update_teams', 'Update Teams'),
                ('update_metakanban_board', 'Update MetaKanban Board'),
                ('update_metakanban_task_label', 'Update MetaKanban Task Label'),
                ('update_metakanban_column', 'Update MetaKanban Column'),
                ('update_metakanban_task', 'Update MetaKanban Task'),
                ('move_metakanban_task', 'Move MetaKanban Task'),
                ('assign_metakanban_task', 'Assign MetaKanban Task'),
                ('use_metakanban_ai', 'Use MetaKanban AI'),
                ('connect_assistants_to_metakanban', 'Connect Assistants to MetaKanban'),
                ('disconnect_assistants_from_metakanban', 'Disconnect Assistants from MetaKanban'),
                ("use_metakanban_meeting_transcription", "Use MetaKanban Meeting Transcription"),
                ("implement_meeting_transcription_with_ai", "Implement Meeting Transcription with AI"),
                ('update_metatempo_connection', 'Update MetaTempo Connection'),
                ('use_meta_tempo_ai', 'Use MetaTempo AI'),
                ('connect_assistants_to_metatempo', 'Connect Assistants to MetaTempo'),
                ('disconnect_assistants_from_metatempo', 'Disconnect Assistants from MetaTempo'),
                ('update_users', 'Update Users'),
                ('connect_user_to_organization', 'Connect User to Organization'),
                ('remove_user_from_organization', 'Remove User from Organization'),
                ('update_assistants', 'Update Assistants'),
                ('update_harmoniq_agents', 'Update Harmoniq Agents'),
                ('chat_with_harmoniq_agents', 'Chat with Harmoniq Agents'),
                ('integrate_plug_and_play_agents', 'Integrate Plug and Play Agents'),
                ('integrate_plug_and_play_teams', 'Integrate Plug and Play Teams'),
                ('create_and_use_chats', 'Create and Use Chats'),
                ('update_voidforger_configurations', 'Update VoidForger Configurations'),
                ('refresh_voidforger_connections', 'Refresh VoidForger Connections'),
                ('toggle_activate_and_deactivate_voidforger', 'Toggle Activate and Deactivate VoidForger'),
                ('manually_trigger_voidforger', 'Manually Trigger VoidForger'),
                ('create_and_use_voidforger_chats', 'Create and Use VoidForger Chats'),
                ('update_voidforger_chat_name', 'Update VoidForger Chat Name'),
                ('update_assistant_memories', 'Update Assistant Memories'),
                ('update_export_assistant', 'Update Export Assistant'),
                ('update_orchestrations', 'Update Orchestrations'),
                ('connect_reactant_assistants_to_orchestration', 'Connect Reactant Assistants to Orchestration'),
                ('disconnect_reactant_assistants_from_orchestration',
                 'Disconnect Reactant Assistants from Orchestration'),
                ('update_file_systems', 'Update File Systems'),
                ('update_web_browsers', 'Update Web Browsers'),
                ('update_sql_databases', 'Update SQL Databases'),
                ('update_nosql_databases', 'Update NoSQL Databases'),
                ('update_custom_nosql_queries', 'Update Custom NoSQL Queries'),
                ('update_knowledge_bases', 'Update Knowledge Bases'),
                ('update_website_storages', 'Update Website Storages'),
                ('update_website_items', 'Update Website Items'),
                ('update_media_storages', 'Update Media Storages'),
                ('update_ml_model_connections', 'Update ML Model Connections'),
                ('update_functions', 'Update Functions'),
                ('update_apis', 'Update APIs'),
                ('update_scripts', 'Update Scripts'),
                ('update_scheduled_jobs', 'Update Scheduled Jobs'),
                ('update_leanmod_scheduled_jobs', 'Update LeanMod Scheduled Jobs'),
                ('update_orchestration_scheduled_jobs', 'Update Orchestration Scheduled Jobs'),
                ('update_triggers', 'Update Triggers'),
                ('update_leanmod_triggers', 'Update LeanMod Triggers'),
                ('update_orchestration_triggers', 'Update Orchestration Triggers'),
                ('can_generate_images', 'Can Generate Images'),
                ('can_generate_audio', 'Can Generate Audio'),
                ('update_integrations', 'Update Integrations'),
                ('update_meta_integrations', 'Update Meta Integrations'),
                ('add_starred_messages', 'Add Starred Messages'),
                ('update_template_messages', 'Update Template Messages'),
                ('update_data_security', 'Update Data Security'),
                ('integrate_beamguard_artifacts', 'Integrate BeamGuard Artifacts'),
                ('discard_beamguard_artifacts', 'Discard BeamGuard Artifacts'),
                ('update_code_base', 'Update Code Base'),
                ('update_code_repository', 'Update Code Repository'),
                ('update_knowledge_base_docs', 'Update Knowledge Base Docs'),
                ('update_storage_files', 'Update Storage Files'),
                ('update_ml_model_files', 'Update ML Model Files'),
                ('integrate_ml_model_files', 'Integrate ML Model Files'),
                ('update_custom_sql_queries', 'Update Custom SQL Queries'),
                ('update_export_leanmod', 'Update Export LeanMod'),
                ('update_expert_networks', 'Update Expert Networks'),
                ('update_export_orchestration', 'Update Export Orchestration'),
                ('update_export_voidforger', 'Update Export VoidForger'),
                ('update_finetuning_model', 'Update Finetuning Model'),
                ('update_lean_assistant', 'Update Lean Assistant'),
                ('archive_chats', 'Archive Chats'),
                ('unarchive_chats', 'Unarchive Chats'),
                ('create_and_use_lean_chats', 'Create and Use Lean Chats'),
                ('archive_lean_chats', 'Archive Lean Chats'),
                ('unarchive_lean_chats', 'Unarchive Lean Chats'),
                ('create_and_use_orchestration_chats', 'Create and Use Orchestration Chats'),
                ('create_support_tickets', 'Create Support Tickets'),
                ('list_support_tickets', 'List Support Tickets'),
                ('update_support_tickets', 'Update Support Tickets'),
                ('update_user_roles', 'Update User Roles'),
                ('create_data_backups', 'Create Data Backups'),
                ('restore_data_backups', 'Restore Data Backups'),
                ('update_brainstorming_sessions', 'Update Brainstorming Sessions'),
                ('create_brainstorming_ideas', 'Create Brainstorming Ideas'),
                ('create_brainstorming_syntheses', 'Create Brainstorming Syntheses'),
                ('bookmark_brainstorming_ideas', 'Bookmark Brainstorming Ideas'),
                ('update_video_generator_connections', 'Update Video Generator Connections'),
                ('update_ellma_scripts', 'Update Ellma Scripts'),
                ('update_drafting_folders', 'Update Drafting Folders'),
                ('update_drafting_documents', 'Update Drafting Documents'),
                ('update_drafting_google_apps_connections', 'Update Drafting Google Apps Connections'),
                ('update_sheetos_folders', 'Update Sheetos Folders'),
                ('update_sheetos_documents', 'Update Sheetos Documents'),
                ('update_sheetos_google_apps_connections', 'Update Sheetos Google Apps Connections'),
                ('update_slider_folders', 'Update Slider Folders'),
                ('update_slider_documents', 'Update Slider Documents'),
                ('update_slider_google_apps_connections', 'Update Slider Google Apps Connections'),
                ('update_formica_google_apps_connections', 'Update Formica Google Apps Connections'),
                ('update_hadron_systems', 'Update Hadron Systems'),
                ('update_hadron_nodes', 'Update Hadron Nodes'),
                ('update_hadron_topics', 'Update Hadron Topics'),
                ('connect_assistants_to_hadron_node', 'Connect Assistants to Hadron Node'),
                ('disconnect_assistants_from_hadron_node', 'Disconnect Assistants from Hadron Node'),
                ('update_blockchain_wallet_connections', 'Update Blockchain Wallet Connections'),
                ('create_smart_contracts', 'Create Smart Contracts'),
                ('connect_smart_contracts_to_assistant', 'Connect Smart Contracts to Assistant'),
                ('disconnect_smart_contracts_from_assistant', 'Disconnect Smart Contracts from Assistant'),
                ('create_internal_notifications', 'Create Internal Notifications'),
                ('update_binexus_processes', 'Update Binexus Processes'),
                ('execute_binexus_processes', 'Execute Binexus Processes'),
                ('use_sinaptera_configuration', 'Use Sinaptera Configuration'),
            ]

    class ReadAdminRole:
        @staticmethod
        def get():
            return [
                ('list_organizations', 'List Organizations'),
                ('list_projects', 'List Projects'),
                ('list_teams', 'List Teams'),
                ('list_metakanban_board', 'List MetaKanban Board'),
                ('list_metakanban_task_label', 'List MetaKanban Task Label'),
                ('use_metakanban_ai', 'Use MetaKanban AI'),
                ("use_metakanban_meeting_transcription", "Use MetaKanban Meeting Transcription"),
                ('list_metatempo_connection', 'List MetaTempo Connection'),
                ('use_meta_tempo_ai', 'Use MetaTempo AI'),
                ('list_llm_cores', 'List LLM Cores'),
                ('list_transactions', 'List Transactions'),
                ('list_users', 'List Users'),
                ('list_user_permissions', 'List User Permissions'),
                ('list_assistants', 'List Assistants'),
                ('list_harmoniq_agents', 'List Harmoniq Agents'),
                ('chat_with_harmoniq_agents', 'Chat with Harmoniq Agents'),
                ('list_plug_and_play_agents', 'List Plug and Play Agents'),
                ('list_plug_and_play_teams', 'List Plug and Play Teams'),
                ('create_and_use_chats', 'Create and Use Chats'),
                ('refresh_voidforger_connections', 'Refresh VoidForger Connections'),
                ('list_voidforger_action_logs', 'List VoidForger Action Logs'),
                ('list_voidforger_auto_execution_logs', 'List VoidForger Auto Execution Logs'),
                ('create_and_use_voidforger_chats', 'Create and Use VoidForger Chats'),
                ('list_assistant_memories', 'List Assistant Memories'),
                ('list_export_assistant', 'List Export Assistant'),
                ('list_orchestrations', 'List Orchestrations'),
                ('list_file_systems', 'List File Systems'),
                ('list_web_browsers', 'List Web Browsers'),
                ('list_sql_databases', 'List SQL Databases'),
                ('list_nosql_databases', 'List NoSQL Databases'),
                ('list_custom_nosql_queries', 'List Custom NoSQL Queries'),
                ('list_knowledge_bases', 'List Knowledge Bases'),
                ('list_website_storages', 'List Website Storages'),
                ('list_website_items', 'List Website Items'),
                ('list_media_storages', 'List Media Storages'),
                ('list_ml_model_connections', 'List ML Model Connections'),
                ('list_functions', 'List Functions'),
                ('list_apis', 'List APIs'),
                ('list_scripts', 'List Scripts'),
                ('list_scheduled_jobs', 'List Scheduled Jobs'),
                ('list_leanmod_scheduled_jobs', 'List LeanMod Scheduled Jobs'),
                ('list_orchestration_scheduled_jobs', 'List Orchestration Scheduled Jobs'),
                ('list_triggers', 'List Triggers'),
                ('list_leanmod_triggers', 'List LeanMod Triggers'),
                ('list_orchestration_triggers', 'List Orchestration Triggers'),
                ('can_generate_images', 'Can Generate Images'),
                ('can_generate_audio', 'Can Generate Audio'),
                ('list_integrations', 'List Integrations'),
                ('list_meta_integrations', 'List Meta Integrations'),
                ('list_starred_messages', 'List Starred Messages'),
                ('list_template_messages', 'List Template Messages'),
                ('list_data_security', 'List Data Security'),
                ('list_beamguard_artifacts', 'List BeamGuard Artifacts'),
                ('list_code_base', 'List Code Base'),
                ('list_code_repository', 'List Code Repository'),
                ('list_knowledge_base_docs', 'List Knowledge Base Docs'),
                ('list_storage_files', 'List Storage Files'),
                ('list_ml_model_files', 'List ML Model Files'),
                ('list_ml_model_integrations', 'List ML Model Integrations'),
                ('list_custom_sql_queries', 'List Custom SQL Queries'),
                ('list_export_leanmod', 'List Export LeanMod'),
                ('list_expert_networks', 'List Expert Networks'),
                ('list_export_orchestration', 'List Export Orchestration'),
                ('list_export_voidforger', 'List Export VoidForger'),
                ('list_finetuning_model', 'List Finetuning Model'),
                ('list_lean_assistant', 'List Lean Assistant'),
                ('archive_chats', 'Archive Chats'),
                ('unarchive_chats', 'Unarchive Chats'),
                ('create_and_use_lean_chats', 'Create and Use Lean Chats'),
                ('archive_lean_chats', 'Archive Lean Chats'),
                ('unarchive_lean_chats', 'Unarchive Lean Chats'),
                ('create_and_use_orchestration_chats', 'Create and Use Orchestration Chats'),
                ('list_support_tickets', 'List Support Tickets'),
                ('list_user_roles', 'List User Roles'),
                ('list_data_backups', 'List Data Backups'),
                ('list_brainstorming_sessions', 'List Brainstorming Sessions'),
                ('bookmark_brainstorming_ideas', 'Bookmark Brainstorming Ideas'),
                ('list_video_generator_connections', 'List Video Generator Connections'),
                ('list_ellma_scripts', 'List Ellma Scripts'),
                ('list_drafting_folders', 'List Drafting Folders'),
                ('list_drafting_documents', 'List Drafting Documents'),
                ('list_drafting_google_apps_connections', 'List Drafting Google Apps Connections'),
                ('list_sheetos_folders', 'List Sheetos Folders'),
                ('list_sheetos_documents', 'List Sheetos Documents'),
                ('list_sheetos_google_apps_connections', 'List Sheetos Google Apps Connections'),
                ('list_slider_folders', 'List Slider Folders'),
                ('list_slider_documents', 'List Slider Documents'),
                ('list_slider_google_apps_connections', 'List Slider Google Apps Connections'),
                ('list_formica_google_apps_connections', 'List Formica Google Apps Connections'),
                ('list_hadron_systems', 'List Hadron Systems'),
                ('list_hadron_nodes', 'List Hadron Nodes'),
                ('list_hadron_topics', 'List Hadron Topics'),
                ('list_blockchain_wallet_connections', 'List Blockchain Wallet Connections'),
                ('list_smart_contracts', 'List Smart Contracts'),
                ('list_binexus_processes', 'List Binexus Processes'),
                ('list_binexus_elites', 'List Binexus Elites'),
            ]

    class DeletionAdminRole:
        @staticmethod
        def get():
            return [
                ('delete_projects', 'Delete Projects'),
                ('delete_teams', 'Delete Teams'),
                ('delete_metakanban_board', 'Delete MetaKanban Board'),
                ('delete_metakanban_task_label', 'Delete MetaKanban Task Label'),
                ('delete_metakanban_column', 'Delete MetaKanban Column'),
                ('delete_metakanban_task', 'Delete MetaKanban Task'),
                ('disconnect_assistants_from_metakanban', 'Disconnect Assistants from MetaKanban'),
                ("delete_meeting_transcription", "Delete Meeting Transcription"),
                ('delete_metatempo_connection', 'Delete MetaTempo Connection'),
                ('disconnect_assistants_from_metatempo', 'Disconnect Assistants from MetaTempo'),
                ('delete_users', 'Delete Users'),
                ('remove_user_from_organization', 'Remove User from Organization'),
                ('delete_assistants', 'Delete Assistants'),
                ('delete_harmoniq_agents', 'Delete Harmoniq Agents'),
                ('remove_chats', 'Remove Chats'),
                ('delete_voidforger_action_logs', 'Delete VoidForger Action Logs'),
                ('delete_voidforger_auto_execution_logs', 'Delete VoidForger Auto Execution Logs'),
                ('remove_voidforger_chats', 'Remove VoidForger Chats'),
                ('delete_assistant_memories', 'Delete Assistant Memories'),
                ('delete_export_assistant', 'Delete Export Assistant'),
                ('delete_orchestrations', 'Delete Orchestrations'),
                ('disconnect_reactant_assistants_from_orchestration',
                 'Disconnect Reactant Assistants from Orchestration'),
                ('delete_file_systems', 'Delete File Systems'),
                ('delete_web_browsers', 'Delete Web Browsers'),
                ('delete_sql_databases', 'Delete SQL Databases'),
                ('delete_nosql_databases', 'Delete NoSQL Databases'),
                ('delete_custom_nosql_queries', 'Delete Custom NoSQL Queries'),
                ('delete_knowledge_bases', 'Delete Knowledge Bases'),
                ('delete_website_storages', 'Delete Website Storages'),
                ('delete_website_items', 'Delete Website Items'),
                ('delete_media_storages', 'Delete Media Storages'),
                ('delete_ml_model_connections', 'Delete ML Model Connections'),
                ('delete_functions', 'Delete Functions'),
                ('delete_apis', 'Delete APIs'),
                ('delete_scripts', 'Delete Scripts'),
                ('delete_scheduled_jobs', 'Delete Scheduled Jobs'),
                ('delete_leanmod_scheduled_jobs', 'Delete LeanMod Scheduled Jobs'),
                ('delete_orchestration_scheduled_jobs', 'Delete Orchestration Scheduled Jobs'),
                ('delete_triggers', 'Delete Triggers'),
                ('delete_leanmod_triggers', 'Delete LeanMod Triggers'),
                ('delete_orchestration_triggers', 'Delete Orchestration Triggers'),
                ('delete_integrations', 'Delete Integrations'),
                ('delete_meta_integrations', 'Delete Meta Integrations'),
                ('remove_starred_messages', 'Remove Starred Messages'),
                ('remove_template_messages', 'Remove Template Messages'),
                ('delete_data_security', 'Delete Data Security'),
                ('discard_beamguard_artifacts', 'Discard BeamGuard Artifacts'),
                ('delete_code_base', 'Delete Code Base'),
                ('delete_code_repository', 'Delete Code Repository'),
                ('delete_knowledge_base_docs', 'Delete Knowledge Base Docs'),
                ('delete_storage_files', 'Delete Storage Files'),
                ('delete_ml_model_files', 'Delete ML Model Files'),
                ('delete_custom_sql_queries', 'Delete Custom SQL Queries'),
                ('delete_export_leanmod', 'Delete Export LeanMod'),
                ('delete_expert_networks', 'Delete Expert Networks'),
                ('delete_export_orchestration', 'Delete Export Orchestration'),
                ('delete_export_voidforger', 'Delete Export VoidForger'),
                ('delete_finetuning_model', 'Delete Finetuning Model'),
                ('delete_lean_assistant', 'Delete Lean Assistant'),
                ('remove_lean_chats', 'Remove Lean Chats'),
                ('remove_orchestration_chats', 'Remove Orchestration Chats'),
                ('delete_user_roles', 'Delete User Roles'),
                ('delete_data_backups', 'Delete Data Backups'),
                ('delete_brainstorming_sessions', 'Delete Brainstorming Sessions'),
                ('delete_brainstorming_ideas', 'Delete Brainstorming Ideas'),
                ('delete_video_generator_connections', 'Delete Video Generator Connections'),
                ('delete_ellma_scripts', 'Delete Ellma Scripts'),
                ('delete_drafting_folders', 'Delete Drafting Folders'),
                ('delete_drafting_documents', 'Delete Drafting Documents'),
                ('delete_drafting_google_apps_connections', 'Delete Drafting Google Apps Connections'),
                ('delete_sheetos_folders', 'Delete Sheetos Folders'),
                ('delete_sheetos_documents', 'Delete Sheetos Documents'),
                ('delete_sheetos_google_apps_connections', 'Delete Sheetos Google Apps Connections'),
                ('delete_slider_folders', 'Delete Slider Folders'),
                ('delete_slider_documents', 'Delete Slider Documents'),
                ('delete_slider_google_apps_connections', 'Delete Slider Google Apps Connections'),
                ('delete_formica_google_apps_connections', 'Delete Formica Google Apps Connections'),
                ('delete_hadron_systems', 'Delete Hadron Systems'),
                ('delete_hadron_nodes', 'Delete Hadron Nodes'),
                ('delete_hadron_topics', 'Delete Hadron Topics'),
                ('delete_hadron_node_execution_logs', 'Delete Hadron Node Execution Logs'),
                ('delete_hadron_node_sase_logs', 'Delete Hadron Node SASE Logs'),
                ('delete_hadron_node_publish_history_logs', 'Delete Hadron Node Publish History Logs'),
                ('delete_hadron_topic_message_history_logs', 'Delete Hadron Topic Message History Logs'),
                ('delete_hadron_node_speech_logs', 'Delete Hadron Node Speech Logs'),
                ('disconnect_assistants_from_hadron_node', 'Disconnect Assistants from Hadron Node'),
                ('delete_blockchain_wallet_connections', 'Delete Blockchain Wallet Connections'),
                ('soft_delete_smart_contracts', 'Soft Delete Smart Contracts'),
                ('disconnect_smart_contracts_from_assistant', 'Disconnect Smart Contracts from Assistant'),
                ('delete_internal_notifications', 'Delete Internal Notifications'),
                ('delete_binexus_processes', 'Delete Binexus Processes'),
                ('delete_binexus_elites', 'Delete Binexus Elites'),
            ]

    @staticmethod
    def get_dict():
        return {
            "SuperUserAdminRole": PredefinedRolePackages__Functional.SuperUserAdminRole.get(),
            "CreationAdminRole": PredefinedRolePackages__Functional.CreationAdminRole.get(),
            "ModificationAdminRole": PredefinedRolePackages__Functional.ModificationAdminRole.get(),
            "ReadAdminRole": PredefinedRolePackages__Functional.ReadAdminRole.get(),
            "DeletionAdminRole": PredefinedRolePackages__Functional.DeletionAdminRole.get(),
        }


class PredefinedRolePackages__Contextual:
    class Names:
        PermissionAdmin__Dangerous = "PermissionAdmin__Dangerous"
        OrganizationAdmin = "OrganizationAdmin"
        AssistantAdmin = "AssistantAdmin"
        UsersAdmin = "UsersAdmin"
        FinanceAdmin = "FinanceAdmin"
        ChatInteractionUser = "ChatInteractionUser"
        NotificationAdmin = "NotificationAdmin"
        DataSourceAdmin = "DataSourceAdmin"
        SecurityAdmin = "SecurityAdmin"
        SupportUser = "SupportUser"
        ScriptingUser = "ScriptingUser"
        DeveloperUser = "DeveloperUser"
        BlockchainAdmin = "BlockchainAdmin"
        HardwareAdmin = "HardwareAdmin"
        OfficeUser = "OfficeUser"
        PromptEngineerUser = "PromptEngineerUser"
        ProjectTeamAdmin = "ProjectTeamAdmin"

    class PermissionAdmin__Dangerous:
        @staticmethod
        def get():
            return [
                ('modify_user_permissions', 'Modify User Permissions'),
                ('list_user_permissions', 'List User Permissions'),
                ('create_user_roles', 'Create User Roles'),
                ('list_user_roles', 'List User Roles'),
                ('update_user_roles', 'Update User Roles'),
                ('delete_user_roles', 'Delete User Roles'),
            ]

    class OrganizationAdmin:
        @staticmethod
        def get():
            return [
                ('add_organizations', 'Add Organizations'),
                ('update_organizations', 'Update Organizations'),
                ('list_organizations', 'List Organizations'),
                ('delete_organizations', 'Delete Organizations'),
                ('add_llm_cores', 'Add LLM Cores'),
                ('update_llm_cores', 'Update LLM Cores'),
                ('list_llm_cores', 'List LLM Cores'),
                ('delete_llm_cores', 'Delete LLM Cores'),
                ('list_transactions', 'List Transactions'),
            ]

    class AssistantAdmin:
        @staticmethod
        def get():
            return [
                ('use_metakanban_ai', 'Use MetaKanban AI'),
                ('connect_assistants_to_metakanban', 'Connect Assistants to MetaKanban'),
                ('disconnect_assistants_from_metakanban', 'Disconnect Assistants from MetaKanban'),
                ("use_metakanban_meeting_transcription", "Use MetaKanban Meeting Transcription"),
                ("implement_meeting_transcription_with_ai", "Implement Meeting Transcription with AI"),
                ("delete_meeting_transcription", "Delete Meeting Transcription"),
                ('use_meta_tempo_ai', 'Use MetaTempo AI'),
                ('connect_assistants_to_metatempo', 'Connect Assistants to MetaTempo'),
                ('disconnect_assistants_from_metatempo', 'Disconnect Assistants from MetaTempo'),
                ('add_assistants', 'Add Assistants'),
                ('update_assistants', 'Update Assistants'),
                ('list_assistants', 'List Assistants'),
                ('delete_assistants', 'Delete Assistants'),
                ('add_harmoniq_agents', 'Add Harmoniq Agents'),
                ('update_harmoniq_agents', 'Update Harmoniq Agents'),
                ('list_harmoniq_agents', 'List Harmoniq Agents'),
                ('delete_harmoniq_agents', 'Delete Harmoniq Agents'),
                ('chat_with_harmoniq_agents', 'Chat with Harmoniq Agents'),
                ('integrate_plug_and_play_agents', 'Integrate Plug and Play Agents'),
                ('list_plug_and_play_agents', 'List Plug and Play Agents'),
                ('integrate_plug_and_play_teams', 'Integrate Plug and Play Teams'),
                ('list_plug_and_play_teams', 'List Plug and Play Teams'),
                ('create_and_use_chats', 'Create and Use Chats'),
                ('remove_chats', 'Remove Chats'),
                ('update_voidforger_configurations', 'Update VoidForger Configurations'),
                ('refresh_voidforger_connections', 'Refresh VoidForger Connections'),
                ('toggle_activate_and_deactivate_voidforger', 'Toggle Activate and Deactivate VoidForger'),
                ('manually_trigger_voidforger', 'Manually Trigger VoidForger'),
                ('list_voidforger_action_logs', 'List VoidForger Action Logs'),
                ('delete_voidforger_action_logs', 'Delete VoidForger Action Logs'),
                ('list_voidforger_auto_execution_logs', 'List VoidForger Auto Execution Logs'),
                ('delete_voidforger_auto_execution_logs', 'Delete VoidForger Auto Execution Logs'),
                ('create_and_use_voidforger_chats', 'Create and Use VoidForger Chats'),
                ('update_voidforger_chat_name', 'Update VoidForger Chat Name'),
                ('remove_voidforger_chats', 'Remove VoidForger Chats'),
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
                ('connect_reactant_assistants_to_orchestration', 'Connect Reactant Assistants to Orchestration'),
                ('disconnect_reactant_assistants_from_orchestration', 'Disconnect Reactant Assistants from Orchestration'),
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
                ('add_export_voidforger', 'Add Export VoidForger'),
                ('update_export_voidforger', 'Update Export VoidForger'),
                ('list_export_voidforger', 'List Export VoidForger'),
                ('delete_export_voidforger', 'Delete Export VoidForger'),
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
                ('create_binexus_processes', 'Create Binexus Processes'),
                ('list_binexus_processes', 'List Binexus Processes'),
                ('update_binexus_processes', 'Update Binexus Processes'),
                ('delete_binexus_processes', 'Delete Binexus Processes'),
                ('execute_binexus_processes', 'Execute Binexus Processes'),
                ('delete_binexus_elites', 'Delete Binexus Elites'),
                ('list_binexus_elites', 'List Binexus Elites'),
                ('use_sinaptera_configuration', 'Use Sinaptera Configuration'),
            ]

    class UsersAdmin:
        @staticmethod
        def get():
            return [
                ('add_users', 'Add Users'),
                ('update_users', 'Update Users'),
                ('list_users', 'List Users'),
                ('delete_users', 'Delete Users'),
                ('connect_user_to_organization', 'Connect User to Organization'),
                ('remove_user_from_organization', 'Remove User from Organization'),
            ]

    class FinanceAdmin:
        @staticmethod
        def get():
            return [
                ('add_balance_to_organization', 'Add Balance to Organization'),
                ('transfer_balance_between_organizations', 'Transfer Balance Between Organizations'),
                ('list_transactions', 'List Transactions'),
            ]

    class ChatInteractionUser:
        @staticmethod
        def get():
            return [
                ('use_metakanban_ai', 'Use MetaKanban AI'),
                ("use_metakanban_meeting_transcription", "Use MetaKanban Meeting Transcription"),
                ('use_meta_tempo_ai', 'Use MetaTempo AI'),
                ('chat_with_harmoniq_agents', 'Chat with Harmoniq Agents'),
                ('create_and_use_chats', 'Create and Use Chats'),
                ('create_and_use_voidforger_chats', 'Create and Use VoidForger Chats'),
                ('can_generate_images', 'Can Generate Images'),
                ('can_generate_audio', 'Can Generate Audio'),
                ('add_starred_messages', 'Add Starred Messages'),
                ('list_starred_messages', 'List Starred Messages'),
                ('remove_starred_messages', 'Remove Starred Messages'),
                ('list_template_messages', 'List Template Messages'),
                ('create_and_use_lean_chats', 'Create and Use Lean Chats'),
                ('create_and_use_orchestration_chats', 'Create and Use Orchestration Chats'),
                ('create_brainstorming_ideas', 'Create Brainstorming Ideas'),
                ('create_brainstorming_syntheses', 'Create Brainstorming Syntheses'),
                ('bookmark_brainstorming_ideas', 'Bookmark Brainstorming Ideas'),
                ('add_drafting_google_apps_connections', 'Add Drafting Google Apps Connections'),
                ('list_drafting_google_apps_connections', 'List Drafting Google Apps Connections'),
                ('update_drafting_google_apps_connections', 'Update Drafting Google Apps Connections'),
                ('delete_drafting_google_apps_connections', 'Delete Drafting Google Apps Connections'),
                ('add_sheetos_google_apps_connections', 'Add Sheetos Google Apps Connections'),
                ('update_sheetos_google_apps_connections', 'Update Sheetos Google Apps Connections'),
                ('list_sheetos_google_apps_connections', 'List Sheetos Google Apps Connections'),
                ('delete_sheetos_google_apps_connections', 'Delete Sheetos Google Apps Connections'),
                ('add_slider_google_apps_connections', 'Add Slider Google Apps Connections'),
                ('update_slider_google_apps_connections', 'Update Slider Google Apps Connections'),
                ('list_slider_google_apps_connections', 'List Slider Google Apps Connections'),
                ('delete_slider_google_apps_connections', 'Delete Slider Google Apps Connections'),
                ('add_formica_google_apps_connections', 'Add Formica Google Apps Connections'),
                ('update_formica_google_apps_connections', 'Update Formica Google Apps Connections'),
                ('list_formica_google_apps_connections', 'List Formica Google Apps Connections'),
                ('delete_formica_google_apps_connections', 'Delete Formica Google Apps Connections'),
                ('use_sinaptera_configuration', 'Use Sinaptera Configuration'),

            ]

    class NotificationAdmin:
        @staticmethod
        def get():
            return [
                ('create_internal_notifications', 'Create Internal Notifications'),
                ('delete_internal_notifications', 'Delete Internal Notifications'),
            ]

    class DataSourceAdmin:
        @staticmethod
        def get():
            return [
                ('add_export_assistant', 'Add Export Assistant'),
                ('update_export_assistant', 'Update Export Assistant'),
                ('list_export_assistant', 'List Export Assistant'),
                ('delete_export_assistant', 'Delete Export Assistant'),
                ('add_orchestrations', 'Add Orchestrations'),
                ('update_orchestrations', 'Update Orchestrations'),
                ('list_orchestrations', 'List Orchestrations'),
                ('delete_orchestrations', 'Delete Orchestrations'),
                ('connect_reactant_assistants_to_orchestration', 'Connect Reactant Assistants to Orchestration'),
                ('disconnect_reactant_assistants_from_orchestration',
                 'Disconnect Reactant Assistants from Orchestration'),
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
                ('add_website_storages', 'Add Website Storages'),
                ('update_website_storages', 'Update Website Storages'),
                ('list_website_storages', 'List Website Storages'),
                ('delete_website_storages', 'Delete Website Storages'),
                ('add_website_items', 'Add Website Items'),
                ('update_website_items', 'Update Website Items'),
                ('list_website_items', 'List Website Items'),
                ('delete_website_items', 'Delete Website Items'),
                ('add_media_storages', 'Add Media Storages'),
                ('update_media_storages', 'Update Media Storages'),
                ('list_media_storages', 'List Media Storages'),
                ('delete_media_storages', 'Delete Media Storages'),
                ('add_ml_model_connections', 'Add ML Model Connections'),
                ('update_ml_model_connections', 'Update ML Model Connections'),
                ('list_ml_model_connections', 'List ML Model Connections'),
                ('delete_ml_model_connections', 'Delete ML Model Connections'),
                ('create_video_generator_connections', 'Create Video Generator Connections'),
                ('list_video_generator_connections', 'List Video Generator Connections'),
                ('update_video_generator_connections', 'Update Video Generator Connections'),
                ('delete_video_generator_connections', 'Delete Video Generator Connections'),
                ('add_scheduled_jobs', 'Add Scheduled Jobs'),
                ('update_scheduled_jobs', 'Update Scheduled Jobs'),
                ('list_scheduled_jobs', 'List Scheduled Jobs'),
                ('delete_scheduled_jobs', 'Delete Scheduled Jobs'),
                ('add_leanmod_scheduled_jobs', 'Add LeanMod Scheduled Jobs'),
                ('update_leanmod_scheduled_jobs', 'Update LeanMod Scheduled Jobs'),
                ('list_leanmod_scheduled_jobs', 'List LeanMod Scheduled Jobs'),
                ('delete_leanmod_scheduled_jobs', 'Delete LeanMod Scheduled Jobs'),
                ('add_orchestration_scheduled_jobs', 'Add Orchestration Scheduled Jobs'),
                ('update_orchestration_scheduled_jobs', 'Update Orchestration Scheduled Jobs'),
                ('list_orchestration_scheduled_jobs', 'List Orchestration Scheduled Jobs'),
                ('delete_orchestration_scheduled_jobs', 'Delete Orchestration Scheduled Jobs'),
                ('add_triggers', 'Add Triggers'),
                ('update_triggers', 'Update Triggers'),
                ('list_triggers', 'List Triggers'),
                ('delete_triggers', 'Delete Triggers'),
                ('add_leanmod_triggers', 'Add LeanMod Triggers'),
                ('update_leanmod_triggers', 'Update LeanMod Triggers'),
                ('list_leanmod_triggers', 'List LeanMod Triggers'),
                ('delete_leanmod_triggers', 'Delete LeanMod Triggers'),
                ('add_orchestration_triggers', 'Add Orchestration Triggers'),
                ('update_orchestration_triggers', 'Update Orchestration Triggers'),
                ('list_orchestration_triggers', 'List Orchestration Triggers'),
                ('delete_orchestration_triggers', 'Delete Orchestration Triggers'),
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
                ('integrate_ml_model_files', 'Integrate ML Model Files'),
                ('list_ml_model_integrations', 'List ML Model Integrations'),
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
                ('add_export_voidforger', 'Add Export VoidForger'),
                ('update_export_voidforger', 'Update Export VoidForger'),
                ('list_export_voidforger', 'List Export VoidForger'),
                ('delete_export_voidforger', 'Delete Export VoidForger'),
            ]

    class SecurityAdmin:
        @staticmethod
        def get():
            return [
                ('add_data_security', 'Add Data Security'),
                ('update_data_security', 'Update Data Security'),
                ('list_data_security', 'List Data Security'),
                ('delete_data_security', 'Delete Data Security'),
                ('list_beamguard_artifacts', 'List BeamGuard Artifacts'),
                ('integrate_beamguard_artifacts', 'Integrate BeamGuard Artifacts'),
                ('discard_beamguard_artifacts', 'Discard BeamGuard Artifacts'),
                ('create_data_backups', 'Create Data Backups'),
                ('list_data_backups', 'List Data Backups'),
                ('delete_data_backups', 'Delete Data Backups'),
                ('restore_data_backups', 'Restore Data Backups'),
            ]

    class SupportUser:
        @staticmethod
        def get():
            return [
                ('create_support_tickets', 'Create Support Tickets'),
                ('list_support_tickets', 'List Support Tickets'),
                ('update_support_tickets', 'Update Support Tickets'),
            ]

    class ScriptingUser:
        @staticmethod
        def get():
            return [
                ('create_ellma_scripts', 'Create Ellma Scripts'),
                ('list_ellma_scripts', 'List Ellma Scripts'),
                ('update_ellma_scripts', 'Update Ellma Scripts'),
                ('delete_ellma_scripts', 'Delete Ellma Scripts'),
            ]

    class DeveloperUser:
        @staticmethod
        def get():
            return [
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
                ('add_leanmod_scheduled_jobs', 'Add LeanMod Scheduled Jobs'),
                ('update_leanmod_scheduled_jobs', 'Update LeanMod Scheduled Jobs'),
                ('list_leanmod_scheduled_jobs', 'List LeanMod Scheduled Jobs'),
                ('delete_leanmod_scheduled_jobs', 'Delete LeanMod Scheduled Jobs'),
                ('add_orchestration_scheduled_jobs', 'Add Orchestration Scheduled Jobs'),
                ('update_orchestration_scheduled_jobs', 'Update Orchestration Scheduled Jobs'),
                ('list_orchestration_scheduled_jobs', 'List Orchestration Scheduled Jobs'),
                ('delete_orchestration_scheduled_jobs', 'Delete Orchestration Scheduled Jobs'),
                ('add_triggers', 'Add Triggers'),
                ('update_triggers', 'Update Triggers'),
                ('list_triggers', 'List Triggers'),
                ('delete_triggers', 'Delete Triggers'),
                ('add_leanmod_triggers', 'Add LeanMod Triggers'),
                ('update_leanmod_triggers', 'Update LeanMod Triggers'),
                ('list_leanmod_triggers', 'List LeanMod Triggers'),
                ('delete_leanmod_triggers', 'Delete LeanMod Triggers'),
                ('add_orchestration_triggers', 'Add Orchestration Triggers'),
                ('update_orchestration_triggers', 'Update Orchestration Triggers'),
                ('list_orchestration_triggers', 'List Orchestration Triggers'),
                ('delete_orchestration_triggers', 'Delete Orchestration Triggers'),
            ]

    class BlockchainAdmin:
        @staticmethod
        def get():
            return [
                ('create_blockchain_wallet_connections', 'Create Blockchain Wallet Connections'),
                ('list_blockchain_wallet_connections', 'List Blockchain Wallet Connections'),
                ('update_blockchain_wallet_connections', 'Update Blockchain Wallet Connections'),
                ('delete_blockchain_wallet_connections', 'Delete Blockchain Wallet Connections'),
                ('create_smart_contracts', 'Create Smart Contracts'),
                ('list_smart_contracts', 'List Smart Contracts'),
                ('soft_delete_smart_contracts', 'Soft Delete Smart Contracts'),
                ('connect_smart_contracts_to_assistant', 'Connect Smart Contracts to Assistant'),
                ('disconnect_smart_contracts_from_assistant', 'Disconnect Smart Contracts from Assistant'),
            ]

    class HardwareAdmin:
        @staticmethod
        def get():
            return [
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
                ('connect_assistants_to_hadron_node', 'Connect Assistants to Hadron Node'),
                ('disconnect_assistants_from_hadron_node', 'Disconnect Assistants from Hadron Node'),
            ]

    class OfficeUser:
        @staticmethod
        def get():
            return [
                ('list_brainstorming_sessions', 'List Brainstorming Sessions'),
                ('create_brainstorming_ideas', 'Create Brainstorming Ideas'),
                ('delete_brainstorming_ideas', 'Delete Brainstorming Ideas'),
                ('create_brainstorming_syntheses', 'Create Brainstorming Syntheses'),
                ('bookmark_brainstorming_ideas', 'Bookmark Brainstorming Ideas'),
                ('add_drafting_folders', 'Add Drafting Folders'),
                ('update_drafting_folders', 'Update Drafting Folders'),
                ('list_drafting_folders', 'List Drafting Folders'),
                ('delete_drafting_folders', 'Delete Drafting Folders'),
                ('add_drafting_documents', 'Add Drafting Documents'),
                ('update_drafting_documents', 'Update Drafting Documents'),
                ('list_drafting_documents', 'List Drafting Documents'),
                ('delete_drafting_documents', 'Delete Drafting Documents'),
                ('add_drafting_google_apps_connections', 'Add Drafting Google Apps Connections'),
                ('list_drafting_google_apps_connections', 'List Drafting Google Apps Connections'),
                ('update_drafting_google_apps_connections', 'Update Drafting Google Apps Connections'),
                ('delete_drafting_google_apps_connections', 'Delete Drafting Google Apps Connections'),
                ('add_sheetos_folders', 'Add Sheetos Folders'),
                ('update_sheetos_folders', 'Update Sheetos Folders'),
                ('list_sheetos_folders', 'List Sheetos Folders'),
                ('delete_sheetos_folders', 'Delete Sheetos Folders'),
                ('add_sheetos_documents', 'Add Sheetos Documents'),
                ('update_sheetos_documents', 'Update Sheetos Documents'),
                ('list_sheetos_documents', 'List Sheetos Documents'),
                ('delete_sheetos_documents', 'Delete Sheetos Documents'),
                ('add_sheetos_google_apps_connections', 'Add Sheetos Google Apps Connections'),
                ('update_sheetos_google_apps_connections', 'Update Sheetos Google Apps Connections'),
                ('list_sheetos_google_apps_connections', 'List Sheetos Google Apps Connections'),
                ('delete_sheetos_google_apps_connections', 'Delete Sheetos Google Apps Connections'),
                ('add_slider_folders', 'Add Slider Folders'),
                ('update_slider_folders', 'Update Slider Folders'),
                ('list_slider_folders', 'List Slider Folders'),
                ('delete_slider_folders', 'Delete Slider Folders'),
                ('add_slider_documents', 'Add Slider Documents'),
                ('update_slider_documents', 'Update Slider Documents'),
                ('list_slider_documents', 'List Slider Documents'),
                ('delete_slider_documents', 'Delete Slider Documents'),
                ('add_slider_google_apps_connections', 'Add Slider Google Apps Connections'),
                ('update_slider_google_apps_connections', 'Update Slider Google Apps Connections'),
                ('list_slider_google_apps_connections', 'List Slider Google Apps Connections'),
                ('delete_slider_google_apps_connections', 'Delete Slider Google Apps Connections'),
                ('add_formica_google_apps_connections', 'Add Formica Google Apps Connections'),
                ('update_formica_google_apps_connections', 'Update Formica Google Apps Connections'),
                ('list_formica_google_apps_connections', 'List Formica Google Apps Connections'),
                ('delete_formica_google_apps_connections', 'Delete Formica Google Apps Connections'),
            ]

    class PromptEngineerUser:
        @staticmethod
        def get():
            return [
                ('create_binexus_processes', 'Create Binexus Processes'),
                ('list_binexus_processes', 'List Binexus Processes'),
                ('update_binexus_processes', 'Update Binexus Processes'),
                ('delete_binexus_processes', 'Delete Binexus Processes'),
                ('execute_binexus_processes', 'Execute Binexus Processes'),
                ('delete_binexus_elites', 'Delete Binexus Elites'),
                ('list_binexus_elites', 'List Binexus Elites'),
                ('add_finetuning_model', 'Add Finetuning Model'),
                ('update_finetuning_model', 'Update Finetuning Model'),
                ('list_finetuning_model', 'List Finetuning Model'),
                ('delete_finetuning_model', 'Delete Finetuning Model'),
            ]

    class ProjectTeamAdmin:
        @staticmethod
        def get():
            return [
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
                ('connect_assistants_to_metakanban', 'Connect Assistants to MetaKanban'),
                ('disconnect_assistants_from_metakanban', 'Disconnect Assistants from MetaKanban'),
                ("use_metakanban_meeting_transcription", "Use MetaKanban Meeting Transcription"),
                ("implement_meeting_transcription_with_ai", "Implement Meeting Transcription with AI"),
                ("delete_meeting_transcription", "Delete Meeting Transcription"),
                ('add_metatempo_connection', 'Add MetaTempo Connection'),
                ('update_metatempo_connection', 'Update MetaTempo Connection'),
                ('list_metatempo_connection', 'List MetaTempo Connection'),
                ('delete_metatempo_connection', 'Delete MetaTempo Connection'),
                ('use_meta_tempo_ai', 'Use MetaTempo AI'),
                ('connect_assistants_to_metatempo', 'Connect Assistants to MetaTempo'),
                ('disconnect_assistants_from_metatempo', 'Disconnect Assistants from MetaTempo'),
                ('create_brainstorming_sessions', 'Create Brainstorming Sessions'),
                ('list_brainstorming_sessions', 'List Brainstorming Sessions'),
                ('update_brainstorming_sessions', 'Update Brainstorming Sessions'),
                ('delete_brainstorming_sessions', 'Delete Brainstorming Sessions'),
                ('create_brainstorming_ideas', 'Create Brainstorming Ideas'),
                ('delete_brainstorming_ideas', 'Delete Brainstorming Ideas'),
                ('create_brainstorming_syntheses', 'Create Brainstorming Syntheses'),
                ('bookmark_brainstorming_ideas', 'Bookmark Brainstorming Ideas'),
                ('add_drafting_folders', 'Add Drafting Folders'),
                ('update_drafting_folders', 'Update Drafting Folders'),
                ('list_drafting_folders', 'List Drafting Folders'),
                ('delete_drafting_folders', 'Delete Drafting Folders'),
                ('add_drafting_documents', 'Add Drafting Documents'),
                ('update_drafting_documents', 'Update Drafting Documents'),
                ('list_drafting_documents', 'List Drafting Documents'),
                ('delete_drafting_documents', 'Delete Drafting Documents'),
                ('add_drafting_google_apps_connections', 'Add Drafting Google Apps Connections'),
                ('list_drafting_google_apps_connections', 'List Drafting Google Apps Connections'),
                ('update_drafting_google_apps_connections', 'Update Drafting Google Apps Connections'),
                ('delete_drafting_google_apps_connections', 'Delete Drafting Google Apps Connections'),
                ('add_sheetos_folders', 'Add Sheetos Folders'),
                ('update_sheetos_folders', 'Update Sheetos Folders'),
                ('list_sheetos_folders', 'List Sheetos Folders'),
                ('delete_sheetos_folders', 'Delete Sheetos Folders'),
                ('add_sheetos_documents', 'Add Sheetos Documents'),
                ('update_sheetos_documents', 'Update Sheetos Documents'),
                ('list_sheetos_documents', 'List Sheetos Documents'),
                ('delete_sheetos_documents', 'Delete Sheetos Documents'),
                ('add_sheetos_google_apps_connections', 'Add Sheetos Google Apps Connections'),
                ('update_sheetos_google_apps_connections', 'Update Sheetos Google Apps Connections'),
                ('list_sheetos_google_apps_connections', 'List Sheetos Google Apps Connections'),
                ('delete_sheetos_google_apps_connections', 'Delete Sheetos Google Apps Connections'),
                ('add_slider_folders', 'Add Slider Folders'),
                ('update_slider_folders', 'Update Slider Folders'),
                ('list_slider_folders', 'List Slider Folders'),
                ('delete_slider_folders', 'Delete Slider Folders'),
                ('add_slider_documents', 'Add Slider Documents'),
                ('update_slider_documents', 'Update Slider Documents'),
                ('list_slider_documents', 'List Slider Documents'),
                ('delete_slider_documents', 'Delete Slider Documents'),
                ('add_slider_google_apps_connections', 'Add Slider Google Apps Connections'),
                ('update_slider_google_apps_connections', 'Update Slider Google Apps Connections'),
                ('list_slider_google_apps_connections', 'List Slider Google Apps Connections'),
                ('delete_slider_google_apps_connections', 'Delete Slider Google Apps Connections'),
                ('add_formica_google_apps_connections', 'Add Formica Google Apps Connections'),
                ('update_formica_google_apps_connections', 'Update Formica Google Apps Connections'),
                ('list_formica_google_apps_connections', 'List Formica Google Apps Connections'),
                ('delete_formica_google_apps_connections', 'Delete Formica Google Apps Connections'),
                ('create_internal_notifications', 'Create Internal Notifications'),
                ('delete_internal_notifications', 'Delete Internal Notifications'),
            ]

    @staticmethod
    def get_dict():
        return {
            "PermissionAdmin__Dangerous": PredefinedRolePackages__Contextual.PermissionAdmin__Dangerous.get(),
            "OrganizationAdmin": PredefinedRolePackages__Contextual.OrganizationAdmin.get(),
            "AssistantAdmin": PredefinedRolePackages__Contextual.AssistantAdmin.get(),
            "UsersAdmin": PredefinedRolePackages__Contextual.UsersAdmin.get(),
            "FinanceAdmin": PredefinedRolePackages__Contextual.FinanceAdmin.get(),
            "ChatInteractionUser": PredefinedRolePackages__Contextual.ChatInteractionUser.get(),
            "NotificationAdmin": PredefinedRolePackages__Contextual.NotificationAdmin.get(),
            "DataSourceAdmin": PredefinedRolePackages__Contextual.DataSourceAdmin.get(),
            "SecurityAdmin": PredefinedRolePackages__Contextual.SecurityAdmin.get(),
            "SupportUser": PredefinedRolePackages__Contextual.SupportUser.get(),
            "ScriptingUser": PredefinedRolePackages__Contextual.ScriptingUser.get(),
            "DeveloperUser": PredefinedRolePackages__Contextual.DeveloperUser.get(),
            "BlockchainAdmin": PredefinedRolePackages__Contextual.BlockchainAdmin.get(),
            "HardwareAdmin": PredefinedRolePackages__Contextual.HardwareAdmin.get(),
            "OfficeUser": PredefinedRolePackages__Contextual.OfficeUser.get(),
            "PromptEngineerUser": PredefinedRolePackages__Contextual.PromptEngineerUser.get(),
            "ProjectTeamAdmin": PredefinedRolePackages__Contextual.ProjectTeamAdmin.get(),
        }


USER_PERMISSIONS_ADMIN_LIST = (
    "user",
    "permission_type",
    "created_at",
)
USER_PERMISSIONS_ADMIN_FILTER = (
    "user",
    "permission_type",
    "created_at"
)
USER_PERMISSIONS_ADMIN_SEARCH = (
    "user",
    "permission_type"
)

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
