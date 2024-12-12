#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: integrate_assistant_to_organization_views.py
#  Last Modified: 2024-11-05 20:12:33
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-05 20:12:34
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

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View

from apps.assistants.models import Assistant
from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.datasource_browsers.models import DataSourceBrowserConnection

from apps.datasource_codebase.models import (
    CodeRepositoryStorageConnection,
    CodeBaseRepository,
)

from apps.datasource_file_systems.models import DataSourceFileSystem

from apps.datasource_knowledge_base.models import (
    DocumentKnowledgeBaseConnection,
    KnowledgeBaseDocument,
    DocumentChunkVectorData
)

from apps.datasource_media_storages.models import DataSourceMediaStorageConnection, DataSourceMediaStorageItem
from apps.datasource_ml_models.models import DataSourceMLModelConnection, DataSourceMLModelItem
from apps.datasource_nosql.models import NoSQLDatabaseConnection, CustomNoSQLQuery
from apps.datasource_sql.models import SQLDatabaseConnection, CustomSQLQuery
from apps.datasource_website.models import DataSourceWebsiteStorageConnection
from apps.hadron_prime.models import HadronNodeAssistantConnection
from apps.integrations.models import AssistantIntegrationCategory, AssistantIntegration
from apps.llm_core.models import LLMCore
from apps.metakanban.models import MetaKanbanAssistantConnection
from apps.metatempo.models import MetaTempoAssistantConnection
from apps.orchestrations.models import OrchestrationReactantAssistantConnection
from apps.organization.models import Organization
from apps.projects.models import ProjectItem
from apps.user_permissions.utils import PermissionNames
from apps.video_generations.models import VideoGeneratorConnection

logger = logging.getLogger(__name__)


class IntegrationView_IntegrateAssistantToOrganization(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        #############################################################################################################
        #  USER DEFINED PROPERTIES
        #############################################################################################################
        # Configuration:
        #   i. organization
        #   ii. llm_model
        #############################################################################################################
        #  DATA SOURCE ADDITIONS (A 'DUPLICATE' of the data source connection must be created) (OPTIONAL)
        #############################################################################################################
        # i. Web Browsers (Optional) -- (WEB)
        # ii. SSH File Systems (Optional) -- (SSH)
        # iii. SQL Databases (Optional) -- (SQL)
        # iv. NoSQL Databases (Optional) -- (NOSQL)
        # v. Knowledge Bases (Optional) -- (KB + DOCS)
        # vi. Code Bases (Optional) -- (CODE)
        # vii. Website Storage Connections (Optional) -- (WEBSITE)
        # viii. Media Storages (Optional) -- (MEDIA + FILES)
        # ix. ML models (Optional) -- (ML)
        # x. Video Generators (Optional) -- (VID)
        # xi. Projects (Optional) -- (PROJECT)
        # _
        # _____ new _____
        # _
        # xii. Hadron Node <> Assistant Connections
        # xiii. MetaKanban <> Assistant Connections
        # xiv. MetaTempo <> Assistant Connections
        # xv. Orchestration <> Assistant Connections
        #############################################################################################################
        # MULTI-MODALITIES (Can be later MODIFIED BY USER, but on creation content PASSED FROM BIMOD STAFF) (OPTIONAL)
        #############################################################################################################
        # i. Custom Functions
        # ii. Custom APIs
        # iii. Custom Scripts
        #############################################################################################################

        category_id = request.POST.get('category_id')
        category = AssistantIntegrationCategory.objects.get(id=category_id)
        user = request.user

        ##############################
        # PERMISSION CHECK FOR - INTEGRATE_PLUG_AND_PLAY_AGENTS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.INTEGRATE_PLUG_AND_PLAY_AGENTS
        ):
            messages.error(self.request, "You do not have permission to integrate plug-and-play agents.")
            return redirect('integrations:store', category_slug=category.category_slug)
        ##############################

        integration_id = request.POST.get('integration_id')
        integration_data = AssistantIntegration.objects.get(id=integration_id)

        organization_id = request.POST.get('organization')
        llm_model_id = request.POST.get('llm_model')
        web_browser_id = request.POST.get('web_browser')
        file_system_id = request.POST.get('file_system')
        sql_database_id = request.POST.get('sql_database')
        nosql_database_id = request.POST.get('nosql_database')
        knowledge_base_id = request.POST.get('knowledge_base')
        code_base_id = request.POST.get('code_base')
        website_storage_id = request.POST.get('website_storage')
        media_storage_id = request.POST.get('media_storage')
        ml_storage_id = request.POST.get('ml_storage')
        video_generator_id = request.POST.get('video_generator')
        project_item_id = request.POST.get('project_item')
        hadron_node_conn_id = request.POST.get('hadron_node')
        metakanban_conn_id = request.POST.get('metakanban')
        metatempo_conn_id = request.POST.get('metatempo')
        orchestration_conn_id = request.POST.get('orchestration')

        organization = Organization.objects.get(id=organization_id)
        llm_model = LLMCore.objects.get(id=llm_model_id)

        web_browser = None
        if web_browser_id:
            web_browser = DataSourceBrowserConnection.objects.get(id=web_browser_id)

        file_system = None
        if file_system_id:
            file_system = DataSourceFileSystem.objects.get(id=file_system_id)

        sql_database = None
        if sql_database_id:
            sql_database = SQLDatabaseConnection.objects.get(id=sql_database_id)

        nosql_database = None
        if nosql_database_id:
            nosql_database = NoSQLDatabaseConnection.objects.get(id=nosql_database_id)

        knowledge_base = None
        if knowledge_base_id:
            knowledge_base = DocumentKnowledgeBaseConnection.objects.get(id=knowledge_base_id)

        code_base = None
        if code_base_id:
            code_base = CodeRepositoryStorageConnection.objects.get(id=code_base_id)

        website_storage = None
        if website_storage_id:
            website_storage = DataSourceWebsiteStorageConnection.objects.get(id=website_storage_id)

        media_storage = None
        if media_storage_id:
            media_storage = DataSourceMediaStorageConnection.objects.get(id=media_storage_id)

        ml_storage = None
        if ml_storage_id:
            ml_storage = DataSourceMLModelConnection.objects.get(id=ml_storage_id)

        video_generator = None
        if video_generator_id:
            video_generator = VideoGeneratorConnection.objects.get(id=video_generator_id)

        project_item = None
        if project_item_id:
            project_item = ProjectItem.objects.get(id=project_item_id)

        hadron_node = None
        if hadron_node_conn_id:
            hadron_node = HadronNodeAssistantConnection.objects.get(id=hadron_node_conn_id)

        metakanban = None
        if metakanban_conn_id:
            metakanban = MetaKanbanAssistantConnection.objects.get(id=metakanban_conn_id)

        metatempo = None
        if metatempo_conn_id:
            metatempo = MetaTempoAssistantConnection.objects.get(id=metatempo_conn_id)

        orchestration = None
        if orchestration_conn_id:
            orchestration = OrchestrationReactantAssistantConnection.objects.get(id=orchestration_conn_id)

        # Step 1: Create the assistant
        created_assistant = Assistant.objects.create(
            organization=organization,
            llm_model=llm_model,
            name=integration_data.integration_name,
            description=integration_data.integration_description,
            instructions=integration_data.integration_instructions,
            response_template=integration_data.integration_response_template,
            audience=integration_data.integration_audience,
            tone=integration_data.integration_tone,
            assistant_image=integration_data.integration_assistant_image,
            max_retry_count=integration_data.integration_max_retries,
            tool_max_attempts_per_instance=integration_data.integration_max_tool_retries,
            tool_max_chains=integration_data.integration_max_tool_pipelines,
            max_context_messages=integration_data.integration_max_message_memory,
            time_awareness=integration_data.integration_time_awareness,
            place_awareness=integration_data.integration_location_awareness,
            multi_step_reasoning_capability_choice=integration_data.integration_multi_step_reasoning,
            image_generation_capability=integration_data.integration_image_generation_capability,
            context_overflow_strategy=integration_data.integration_context_overflow_strategy,
            response_language=integration_data.integration_response_language,
            glossary=integration_data.integration_glossary,
            ner_integration=integration_data.ner_integration,
            created_by_user=user,
            last_updated_by_user=user
        )
        if project_item:
            created_assistant.project_items.set([project_item])
        created_assistant.save()

        # Step 2: Create a copy of the web browser
        try:
            if web_browser:
                duplicated_web_browser = web_browser
                duplicated_web_browser.pk = None
                duplicated_web_browser.assistant = created_assistant
                duplicated_web_browser.created_by_user = user
                duplicated_web_browser.save()
                created_assistant.save()
        except Exception as e:
            messages.error(request, 'An error occurred while integrating the web browser.')
            logger.error(f"Error occurred while integrating the web browser: {e}")

        # Step 3: Create a copy of the file system
        try:
            if file_system:
                duplicated_file_system = file_system
                duplicated_file_system.pk = None
                duplicated_file_system.assistant = created_assistant
                duplicated_file_system.created_by_user = user
                duplicated_file_system.save()
                created_assistant.save()
        except Exception as e:
            messages.error(request, 'An error occurred while integrating the file system.')
            logger.error(f"Error occurred while integrating the file system: {e}")

        # Step 4: Create a copy of the video generator
        try:
            if video_generator:
                duplicated_video_generator = video_generator
                duplicated_video_generator.pk = None
                duplicated_video_generator.organization = organization
                duplicated_video_generator.assistant = created_assistant
                duplicated_video_generator.created_by_user = user
                duplicated_video_generator.save()
                created_assistant.save()
        except Exception as e:
            messages.error(request, 'An error occurred while integrating the video generator.')
            logger.error(f"Error occurred while integrating the video generator: {e}")

        # Step 5: Create a copy of the SQL database
        try:
            if sql_database:
                sql_database: SQLDatabaseConnection
                duplicated_sql_database = sql_database
                duplicated_sql_database.pk = None
                duplicated_sql_database.assistant = created_assistant
                duplicated_sql_database.created_by_user = user
                duplicated_sql_database.save()
                created_assistant.save()

                sql_queries = sql_database.custom_queries.all()
                for sql_query in sql_queries:
                    sql_query: CustomSQLQuery
                    duplicated_sql_query = sql_query
                    duplicated_sql_query: CustomSQLQuery
                    duplicated_sql_query.pk = None
                    duplicated_sql_query.database_connection = duplicated_sql_database
                    duplicated_sql_query.save()
                    duplicated_sql_database.save()
        except Exception as e:
            messages.error(request, 'An error occurred while integrating the SQL database.')
            logger.error(f"Error occurred while integrating the SQL database: {e}")

        # Step 6: Create a copy of the NoSQL database
        try:
            if nosql_database:
                nosql_database: NoSQLDatabaseConnection
                duplicated_nosql_database = nosql_database
                duplicated_nosql_database.pk = None
                duplicated_nosql_database.assistant = created_assistant
                duplicated_nosql_database.created_by_user = user
                duplicated_nosql_database.save()
                created_assistant.save()

                nosql_queries = nosql_database.custom_queries.all()
                for nosql_query in nosql_queries:
                    nosql_query: CustomNoSQLQuery
                    duplicated_nosql_query = nosql_query
                    duplicated_nosql_query: CustomNoSQLQuery
                    duplicated_nosql_query.pk = None
                    duplicated_nosql_query.database_connection = duplicated_nosql_database
                    duplicated_nosql_query.save()
                    duplicated_nosql_database.save()
        except Exception as e:
            messages.error(request, 'An error occurred while integrating the NoSQL database.')
            logger.error(f"Error occurred while integrating the NoSQL database: {e}")

        # Step 7: Create a copy of the knowledge base
        try:
            if knowledge_base:
                knowledge_base: DocumentKnowledgeBaseConnection
                duplicated_knowledge_base = knowledge_base
                duplicated_knowledge_base: DocumentKnowledgeBaseConnection
                duplicated_knowledge_base.pk = None
                duplicated_knowledge_base.assistant = created_assistant
                duplicated_knowledge_base.save()
                created_assistant.save()

                kb_documents = knowledge_base.knowledge_base_documents.all()
                for kb_document in kb_documents:
                    kb_document: KnowledgeBaseDocument
                    duplicated_kb_document = kb_document
                    duplicated_kb_document: KnowledgeBaseDocument
                    duplicated_kb_document.pk = None
                    duplicated_kb_document.knowledge_base = duplicated_knowledge_base
                    duplicated_kb_document.save()
                    duplicated_knowledge_base.save()

        except Exception as e:
            messages.error(request, 'An error occurred while integrating the knowledge base.')
            logger.error(f"Error occurred while integrating the knowledge base: {e}")

        # Step 8: Create a copy of the code base
        try:
            if code_base:
                code_base: CodeRepositoryStorageConnection
                duplicated_code_base = code_base
                duplicated_code_base: CodeRepositoryStorageConnection
                duplicated_code_base.pk = None
                duplicated_code_base.assistant = created_assistant
                duplicated_code_base.save()
                created_assistant.save()

                code_repos = code_base.code_base_repositories.all()
                for code_repo in code_repos:
                    code_repo: CodeBaseRepository
                    duplicated_code_repo = code_repo
                    duplicated_code_repo: CodeBaseRepository
                    duplicated_code_repo.pk = None
                    duplicated_code_repo.knowledge_base = duplicated_code_base
                    duplicated_code_repo.save()
                    duplicated_code_base.save()

        except Exception as e:
            messages.error(request, 'An error occurred while integrating the code base.')
            logger.error(f"Error occurred while integrating the code base: {e}")

        # Step 9: Create a copy of the website storage
        try:
            if website_storage:
                website_storage: DataSourceWebsiteStorageConnection
                duplicated_website_storage = website_storage
                duplicated_website_storage: DataSourceWebsiteStorageConnection
                duplicated_website_storage.pk = None
                duplicated_website_storage.assistant = created_assistant
                duplicated_website_storage.save()
                created_assistant.save()

        except Exception as e:
            messages.error(request, 'An error occurred while integrating the website storage.')
            logger.error(f"Error occurred while integrating the website storage: {e}")

        # Step 10: Create a copy of the media storage
        try:
            if media_storage:
                media_storage: DataSourceMediaStorageConnection
                duplicated_media_storage = media_storage
                duplicated_media_storage: DataSourceMediaStorageConnection
                duplicated_media_storage.pk = None
                duplicated_media_storage.assistant = created_assistant
                duplicated_media_storage.save()
                created_assistant.save()

                media_files = media_storage.items.all()
                for media_file in media_files:
                    media_file: DataSourceMediaStorageItem
                    duplicated_media_file = media_file
                    duplicated_media_file: DataSourceMediaStorageItem
                    duplicated_media_file.pk = None
                    duplicated_media_file.storage_base = duplicated_media_storage
                    duplicated_media_file.save()
                    duplicated_media_storage.save()
        except Exception as e:
            messages.error(request, 'An error occurred while integrating the media storage.')
            logger.error(f"Error occurred while integrating the media storage: {e}")

        # Step 11: Create a copy of the ML storage
        try:
            if ml_storage:
                ml_storage: DataSourceMLModelConnection
                duplicated_ml_storage = ml_storage
                duplicated_ml_storage: DataSourceMLModelConnection
                duplicated_ml_storage.pk = None
                duplicated_ml_storage.assistant = created_assistant
                duplicated_ml_storage.save()
                created_assistant.save()

                ml_models = ml_storage.items.all()
                for ml_model in ml_models:
                    ml_model: DataSourceMLModelItem
                    duplicated_ml_model = ml_model
                    duplicated_ml_model: DataSourceMLModelItem
                    duplicated_ml_model.pk = None
                    duplicated_ml_model.ml_model_base = duplicated_ml_storage
                    duplicated_ml_model.save()
                    duplicated_ml_storage.save()
        except Exception as e:
            messages.error(request, 'An error occurred while integrating the ML storage.')
            logger.error(f"Error occurred while integrating the ML storage: {e}")

        # Step 12: Create a copy of the Hadron Node connection
        try:
            if hadron_node:
                hadron_node: HadronNodeAssistantConnection
                duplicated_hadron_node = hadron_node
                duplicated_hadron_node: HadronNodeAssistantConnection
                duplicated_hadron_node.pk = None
                duplicated_hadron_node.assistant = created_assistant
                duplicated_hadron_node.save()
                created_assistant.save()
        except Exception as e:
            messages.error(request, 'An error occurred while integrating the Hadron Node <> Assistant connection.')
            logger.error(f"Error occurred while integrating the Hadron Node <> Assistant connection: {e}")

        # Step 13: Create a copy of the MetaKanban connection
        try:
            if metakanban:
                metakanban: MetaKanbanAssistantConnection
                duplicated_metakanban = metakanban
                duplicated_metakanban: MetaKanbanAssistantConnection
                duplicated_metakanban.pk = None
                duplicated_metakanban.assistant = created_assistant
                duplicated_metakanban.save()
                created_assistant.save()
        except Exception as e:
            messages.error(request, 'An error occurred while integrating the MetaKanban <> Assistant connection.')
            logger.error(f"Error occurred while integrating the MetaKanban <> Assistant connection: {e}")

        # Step 14: Create a copy of the MetaTempo connection
        try:
            if metatempo:
                metatempo: MetaTempoAssistantConnection
                duplicated_metatempo = metatempo
                duplicated_metatempo: MetaTempoAssistantConnection
                duplicated_metatempo.pk = None
                duplicated_metatempo.assistant = created_assistant
                duplicated_metatempo.save()
                created_assistant.save()
        except Exception as e:
            messages.error(request, 'An error occurred while integrating the MetaTempo <> Assistant connection.')
            logger.error(f"Error occurred while integrating the MetaTempo <> Assistant connection: {e}")

        # Step 15: Create a copy of the Orchestration connection
        try:
            if orchestration:
                orchestration: OrchestrationReactantAssistantConnection
                duplicated_orchestration = orchestration
                duplicated_orchestration: OrchestrationReactantAssistantConnection
                duplicated_orchestration.pk = None
                duplicated_orchestration.assistant = created_assistant
                duplicated_orchestration.save()
                created_assistant.save()
        except Exception as e:
            messages.error(request, 'An error occurred while integrating the Orchestration <> Assistant connection.')
            logger.error(f"Error occurred while integrating the Orchestration <> Assistant connection: {e}")

        messages.success(request, 'Assistant has been integrated to the organization successfully.')
        return redirect('integrations:store', category_slug=category.category_slug)
