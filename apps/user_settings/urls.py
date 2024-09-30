#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: urls.py
#  Last Modified: 2024-09-25 17:51:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:12:29
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.urls import path

from apps.user_settings.views import UserSettingsView, DeleteAllLLMModelsView, \
    DeleteAllAssistantsView, DeleteAllChatsView, DeleteAllStarredMessagesView, DeleteAllMemoriesView, \
    DeleteAllMessageTemplatesView, DeleteAllExportAssistantsView, DeleteAllOrchestrationsView, \
    DeleteAllFileSystemsView, DeleteAllWebBrowsersView, DeleteAllSQLDatabasesView, DeleteAllCustomSQLQueriesView, \
    DeleteAllKnowledgeBasesView, DeleteAllKnowledgeBaseDocumentsView, DeleteAllCodeStoragesView, \
    DeleteAllMLModelStoragesView, DeleteAllMLModelsView, DeleteAllMediaStoragesView, DeleteAllMultimediaFilesView, \
    DeleteAllFunctionsView, DeleteAllAPIsView, DeleteAllScriptsView, DeleteAllScheduledJobsView, \
    DeleteAllTriggeredJobsView, DeleteAllRepositoriesView, DeleteAllLeanAssistantsView, DeleteAllExpertNetworksView, \
    DeleteAllLeanChatsView, ToggleAutomatedBackupView

app_name = "user_settings"

urlpatterns = [
    path('settings/', UserSettingsView.as_view(
        template_name="user_settings/settings.html"
    ), name='settings'),
    ###########
    # path('delete/all/organizations/', DeleteAllOrganizationsView.as_view(), name='delete_all_organizations'),
    path('delete/all/llm_models/', DeleteAllLLMModelsView.as_view(), name='delete_all_llm_models'),
    path('delete/all/assistants/', DeleteAllAssistantsView.as_view(), name='delete_all_assistants'),
    path('delete/all/lean_assistants/', DeleteAllLeanAssistantsView.as_view(), name='delete_all_lean_assistants'),
    path('delete/all/expert_networks/', DeleteAllExpertNetworksView.as_view(), name='delete_all_expert_networks'),
    path('delete/all/chats/', DeleteAllChatsView.as_view(), name='delete_all_chats'),
    path('delete/all/lean_chats/', DeleteAllLeanChatsView.as_view(), name='delete_all_lean_chats'),
    path('delete/all/starred_messages/', DeleteAllStarredMessagesView.as_view(), name='delete_all_starred_messages'),
    path('delete/all/memories/', DeleteAllMemoriesView.as_view(), name='delete_all_memories'),
    path('delete/all/message_templates/', DeleteAllMessageTemplatesView.as_view(),
         name='delete_all_message_templates'),
    path('delete/all/export_assistants/', DeleteAllExportAssistantsView.as_view(),
         name='delete_all_export_assistants'),
    path('delete/all/orchestrations/', DeleteAllOrchestrationsView.as_view(), name='delete_all_orchestrations'),
    path('delete/all/file_systems/', DeleteAllFileSystemsView.as_view(), name='delete_all_file_systems'),
    path('delete/all/web_browsers/', DeleteAllWebBrowsersView.as_view(), name='delete_all_web_browsers'),
    path('delete/all/sql_databases/', DeleteAllSQLDatabasesView.as_view(), name='delete_all_sql_databases'),
    path('delete/all/custom_sql_queries/', DeleteAllCustomSQLQueriesView.as_view(),
         name='delete_all_custom_sql_queries'),
    path('delete/all/knowledge_bases/', DeleteAllKnowledgeBasesView.as_view(), name='delete_all_knowledge_bases'),
    path('delete/all/knowledge_base_documents/', DeleteAllKnowledgeBaseDocumentsView.as_view(),
         name='delete_all_knowledge_base_documents'),
    path('delete/all/code_storages/', DeleteAllCodeStoragesView.as_view(), name='delete_all_code_storages'),
    path('delete/all/repositories/', DeleteAllRepositoriesView.as_view(), name='delete_all_repositories'),
    path('delete/all/ml_model_storages/', DeleteAllMLModelStoragesView.as_view(), name='delete_all_ml_model_storages'),
    path('delete/all/ml_models/', DeleteAllMLModelsView.as_view(), name='delete_all_ml_models'),
    path('delete/all/media_storages/', DeleteAllMediaStoragesView.as_view(), name='delete_all_media_storages'),
    path('delete/all/multimedia_files/', DeleteAllMultimediaFilesView.as_view(), name='delete_all_multimedia_files'),
    path('delete/all/functions/', DeleteAllFunctionsView.as_view(), name='delete_all_functions'),
    path('delete/all/apis/', DeleteAllAPIsView.as_view(), name='delete_all_apis'),
    path('delete/all/scripts/', DeleteAllScriptsView.as_view(), name='delete_all_scripts'),
    path('delete/all/scheduled_jobs/', DeleteAllScheduledJobsView.as_view(), name='delete_all_scheduled_jobs'),
    path('delete/all/triggered_jobs/', DeleteAllTriggeredJobsView.as_view(), name='delete_all_triggered_jobs'),
    #####
    path('auto_backups/toggle/', ToggleAutomatedBackupView.as_view(), name='toggle_automated_backups'),
]
