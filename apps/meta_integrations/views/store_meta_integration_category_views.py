#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: store_meta_integration_category_views.py
#  Last Modified: 2024-11-06 17:50:41
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-06 17:50:42
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.datasource_browsers.models import DataSourceBrowserConnection
from apps.datasource_codebase.models import CodeRepositoryStorageConnection
from apps.datasource_file_systems.models import DataSourceFileSystem
from apps.datasource_knowledge_base.models import DocumentKnowledgeBaseConnection
from apps.datasource_media_storages.models import DataSourceMediaStorageConnection
from apps.datasource_ml_models.models import DataSourceMLModelConnection
from apps.datasource_nosql.models import NoSQLDatabaseConnection
from apps.datasource_sql.models import SQLDatabaseConnection
from apps.datasource_website.models import DataSourceWebsiteStorageConnection
from apps.hadron_prime.models import HadronNodeAssistantConnection
from apps.llm_core.models import LLMCore
from apps.meta_integrations.models import MetaIntegrationCategory, MetaIntegrationTeam
from apps.metakanban.models import MetaKanbanAssistantConnection
from apps.metatempo.models import MetaTempoAssistantConnection
from apps.orchestrations.models import OrchestrationReactantAssistantConnection
from apps.organization.models import Organization
from apps.projects.models import ProjectItem
from apps.user_permissions.utils import PermissionNames
from apps.video_generations.models import VideoGeneratorConnection
from web_project import TemplateLayout


class MetaIntegrationView_MetaIntegrationCategoryStore(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_PLUG_AND_PLAY_TEAMS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_PLUG_AND_PLAY_TEAMS):
            messages.error(self.request, "You do not have permission to list plug and play teams.")
            return context
        ##############################

        category = MetaIntegrationCategory.objects.get(
            category_slug=self.kwargs['category_slug']
        )

        user_organizations = Organization.objects.filter(
            users__in=[self.request.user]

        )
        llm_models = LLMCore.objects.filter(
            organization__in=user_organizations
        )

        web_browsers = DataSourceBrowserConnection.objects.filter(
            assistant__organization__in=user_organizations
        )

        ssh_file_systems = DataSourceFileSystem.objects.filter(
            assistant__organization__in=user_organizations
        )

        sql_databases = SQLDatabaseConnection.objects.filter(
            assistant__organization__in=user_organizations
        )

        nosql_databases = NoSQLDatabaseConnection.objects.filter(
            assistant__organization__in=user_organizations
        )

        knowledge_bases = DocumentKnowledgeBaseConnection.objects.filter(
            assistant__organization__in=user_organizations
        )

        code_bases = CodeRepositoryStorageConnection.objects.filter(
            assistant__organization__in=user_organizations
        )

        website_storages = DataSourceWebsiteStorageConnection.objects.filter(
            assistant__organization__in=user_organizations
        )

        media_storages = DataSourceMediaStorageConnection.objects.filter(
            assistant__organization__in=user_organizations
        )

        ml_storages = DataSourceMLModelConnection.objects.filter(
            assistant__organization__in=user_organizations
        )

        video_generators = VideoGeneratorConnection.objects.filter(
            assistant__organization__in=user_organizations
        )

        project_items = ProjectItem.objects.filter(
            organization__in=user_organizations
        )

        hadron_node_connections = HadronNodeAssistantConnection.objects.filter(
            assistant__organization__in=user_organizations
        )
        metakanban_connections = MetaKanbanAssistantConnection.objects.filter(
            assistant__organization__in=user_organizations
        )
        metatempo_connections = MetaTempoAssistantConnection.objects.filter(
            assistant__organization__in=user_organizations
        )
        orchestration_connections = OrchestrationReactantAssistantConnection.objects.filter(
            assistant__organization__in=user_organizations
        )

        meta_integrations = MetaIntegrationTeam.objects.filter(
            meta_integration_category__category_slug=self.kwargs['category_slug']
        ).order_by("meta_integration_name")

        context['category'] = category
        context['organizations'] = user_organizations
        context['meta_integration_teams'] = meta_integrations

        context['llm_models'] = llm_models
        context['web_browsers'] = web_browsers
        context['ssh_file_systems'] = ssh_file_systems
        context['sql_databases'] = sql_databases

        context['nosql_databases'] = nosql_databases
        context['knowledge_bases'] = knowledge_bases
        context['code_bases'] = code_bases
        context['website_storages'] = website_storages

        context['media_storages'] = media_storages
        context['ml_storages'] = ml_storages
        context['video_generators'] = video_generators
        context['project_items'] = project_items

        context['hadron_node_connections'] = hadron_node_connections
        context['metakanban_connections'] = metakanban_connections
        context['metatempo_connections'] = metatempo_connections
        context['orchestration_connections'] = orchestration_connections

        return context
