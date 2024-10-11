#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: urls.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:40
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#


from django.urls import path

from apps.user_settings.views import SettingsView_UserSettings, SettingsView_DeleteAllLLMModels, \
    SettingsView_DeleteAllAssistants, SettingsView_DeleteAllChats, SettingsView_DeleteAllStarredMessages, \
    SettingsView_DeleteAllStandardMemories, \
    SettingsView_DeleteAllMessageTemplates, SettingsView_DeleteAllExportAssistants, \
    SettingsView_DeleteAllOrchestrations, \
    SettingsView_DeleteAllFileSystems, SettingsView_DeleteAllBrowsers, SettingsView_DeleteAllSQLDBs, \
    SettingsView_DeleteAllSQLQueries, \
    SettingsView_DeleteAllVectorStoreManagers, SettingsView_DeleteAllVectorStoreDocuments, \
    SettingsView_DeleteAllCodeStorages, \
    SettingsView_DeleteAllMLManagers, SettingsView_DeleteAllMLModels, SettingsView_DeleteAllMediaManagers, \
    SettingsView_DeleteAllMediaItems, \
    SettingsView_DeleteAllFunctions, SettingsView_DeleteAllAPIs, SettingsView_DeleteAllScripts, \
    SettingsView_DeleteAllScheduledJobs, \
    SettingsView_DeleteAllTriggeredJobs, SettingsView_DeleteAllCodeRepos, SettingsView_DeleteAllLeanModAssistants, \
    SettingsView_DeleteAllExpertNets, \
    SettingsView_DeleteAllLeanModChats, SettingsView_ToggleAutoBackups

app_name = "user_settings"

urlpatterns = [
    path('settings/', SettingsView_UserSettings.as_view(template_name="user_settings/settings.html"),
         name='settings'),
    path('delete/all/llm_models/', SettingsView_DeleteAllLLMModels.as_view(),
         name='delete_all_llm_models'),
    path('delete/all/assistants/', SettingsView_DeleteAllAssistants.as_view(),
         name='delete_all_assistants'),
    path('delete/all/lean_assistants/', SettingsView_DeleteAllLeanModAssistants.as_view(),
         name='delete_all_lean_assistants'),
    path('delete/all/expert_networks/', SettingsView_DeleteAllExpertNets.as_view(),
         name='delete_all_expert_networks'),
    path('delete/all/chats/', SettingsView_DeleteAllChats.as_view(),
         name='delete_all_chats'),
    path('delete/all/lean_chats/', SettingsView_DeleteAllLeanModChats.as_view(),
         name='delete_all_lean_chats'),
    path('delete/all/starred_messages/', SettingsView_DeleteAllStarredMessages.as_view(),
         name='delete_all_starred_messages'),
    path('delete/all/memories/', SettingsView_DeleteAllStandardMemories.as_view(),
         name='delete_all_memories'),
    path('delete/all/message_templates/', SettingsView_DeleteAllMessageTemplates.as_view(),
         name='delete_all_message_templates'),
    path('delete/all/export_assistants/', SettingsView_DeleteAllExportAssistants.as_view(),
         name='delete_all_export_assistants'),
    path('delete/all/orchestrations/', SettingsView_DeleteAllOrchestrations.as_view(),
         name='delete_all_orchestrations'),
    path('delete/all/file_systems/', SettingsView_DeleteAllFileSystems.as_view(),
         name='delete_all_file_systems'),
    path('delete/all/web_browsers/', SettingsView_DeleteAllBrowsers.as_view(),
         name='delete_all_web_browsers'),
    path('delete/all/sql_databases/', SettingsView_DeleteAllSQLDBs.as_view(),
         name='delete_all_sql_databases'),
    path('delete/all/custom_sql_queries/', SettingsView_DeleteAllSQLQueries.as_view(),
         name='delete_all_custom_sql_queries'),
    path('delete/all/knowledge_bases/', SettingsView_DeleteAllVectorStoreManagers.as_view(),
         name='delete_all_knowledge_bases'),
    path('delete/all/knowledge_base_documents/', SettingsView_DeleteAllVectorStoreDocuments.as_view(),
         name='delete_all_knowledge_base_documents'),
    path('delete/all/code_storages/', SettingsView_DeleteAllCodeStorages.as_view(),
         name='delete_all_code_storages'),
    path('delete/all/repositories/', SettingsView_DeleteAllCodeRepos.as_view(),
         name='delete_all_repositories'),
    path('delete/all/ml_model_storages/', SettingsView_DeleteAllMLManagers.as_view(),
         name='delete_all_ml_model_storages'),
    path('delete/all/ml_models/', SettingsView_DeleteAllMLModels.as_view(),
         name='delete_all_ml_models'),
    path('delete/all/media_storages/', SettingsView_DeleteAllMediaManagers.as_view(),
         name='delete_all_media_storages'),
    path('delete/all/multimedia_files/', SettingsView_DeleteAllMediaItems.as_view(),
         name='delete_all_multimedia_files'),
    path('delete/all/functions/', SettingsView_DeleteAllFunctions.as_view(),
         name='delete_all_functions'),
    path('delete/all/apis/', SettingsView_DeleteAllAPIs.as_view(),
         name='delete_all_apis'),
    path('delete/all/scripts/', SettingsView_DeleteAllScripts.as_view(),
         name='delete_all_scripts'),
    path('delete/all/scheduled_jobs/', SettingsView_DeleteAllScheduledJobs.as_view(),
         name='delete_all_scheduled_jobs'),
    path('delete/all/triggered_jobs/', SettingsView_DeleteAllTriggeredJobs.as_view(),
         name='delete_all_triggered_jobs'),
    path('auto_backups/toggle/', SettingsView_ToggleAutoBackups.as_view(),
         name='toggle_automated_backups'),
]
