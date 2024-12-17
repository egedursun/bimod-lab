#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: assistant_vector_data_models.py
#  Last Modified: 2024-11-09 15:09:39
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-09 15:09:39
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import hashlib
import logging
import os
import faiss

import numpy as np

from apps.hadron_prime.models import (
    HadronNodeAssistantConnection
)

from apps.metakanban.models import (
    MetaKanbanAssistantConnection
)

from apps.metatempo.models import (
    MetaTempoAssistantConnection
)

from apps.orchestrations.models import (
    OrchestrationReactantAssistantConnection
)

from apps.semantor.utils.constant_utils import (
    OpenAIEmbeddingModels,
    VECTOR_INDEX_PATH_ASSISTANTS,
    OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS
)

import json

from django.db import models

from apps.datasource_browsers.models import (
    DataSourceBrowserConnection
)

from apps.datasource_codebase.models import (
    CodeRepositoryStorageConnection,
    CodeBaseRepository
)

from apps.datasource_knowledge_base.models import (
    DocumentKnowledgeBaseConnection,
    KnowledgeBaseDocument
)

from apps.datasource_media_storages.models import (
    DataSourceMediaStorageConnection
)

from apps.datasource_ml_models.models import (
    DataSourceMLModelConnection,
    DataSourceMLModelItem
)

from apps.datasource_nosql.models import (
    NoSQLDatabaseConnection,
    CustomNoSQLQuery
)

from apps.datasource_sql.models import (
    SQLDatabaseConnection,
    CustomSQLQuery
)

from apps.mm_apis.models import (
    CustomAPIReference
)

from apps.mm_functions.models import (
    CustomFunctionReference
)

from apps.mm_scripts.models import (
    CustomScriptReference
)

from apps.projects.models import (
    ProjectItem,
    ProjectTeamItem
)

from apps.video_generations.models import (
    VideoGeneratorConnection
)

from config.settings import (
    MAX_BROWSERS_PER_ASSISTANT,
    MAX_SQL_DBS_PER_ASSISTANT,
    MAX_FILE_SYSTEMS_PER_ASSISTANT,
    MAX_NOSQL_DBS_PER_ASSISTANT,
    MAX_KNOWLEDGE_BASES_PER_ASSISTANT,
    MAX_MEDIA_STORAGES_PER_ASSISTANT,
    MAX_ML_STORAGES_PER_ASSISTANT,
    MAX_PROJECTS_PER_ASSISTANT,
    MAX_VIDEO_GENERATORS_PER_ASSISTANT,
    MAX_FUNCTIONS_PER_ASSISTANT,
    MAX_APIS_PER_ASSISTANT,
    MAX_SCRIPTS_PER_ASSISTANT,
    MAX_HADRON_NODES_PER_ASSISTANT,
    MAX_METAKANBAN_BOARDS_PER_ASSISTANT,
    MAX_METATEMPO_TRACKERS_PER_ASSISTANT,
    MAX_ORCHESTRATION_TRIGGERS_PER_ASSISTANT
)

logger = logging.getLogger(__name__)


class AssistantVectorData(models.Model):
    assistant = models.ForeignKey(
        'assistants.Assistant',
        on_delete=models.CASCADE
    )

    raw_data = models.JSONField(blank=True, null=True)

    raw_data_hash = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    vector_data = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.assistant.name + " - " + self.assistant.organization.name

    class Meta:
        verbose_name = "Assistant Vector Data"
        verbose_name_plural = "Assistant Vector Data"

        indexes = [
            models.Index(fields=[
                'assistant'
            ]),
            models.Index(fields=[
                'created_at'
            ]),
            models.Index(fields=[
                'updated_at'
            ]),
        ]

    def _get_index_path(self):
        organization_id = self.assistant.organization.id

        return os.path.join(
            VECTOR_INDEX_PATH_ASSISTANTS,
            f'assistants_index_{organization_id}.index'
        )

    def save(self, *args, **kwargs):

        raw_data = {
            "assistant_name": self.assistant.name,
            "assistant_description": self.assistant.description,
            "assistant_instructions": self.assistant.instructions,
            "tools": {
                "image_generation_capability": False,
                "time_awareness": False,
                "place_awareness": False,
                "reasoning_capability_choice": "N/A",
                "functions": [],
                "apis": [],
                "scripts": [],
            },
            "data_sources": {
                "browsers": {},
                "file_systems": {},
                "sql_dbs": {},
                "nosql_dbs": {},
                "knowledge_bases": {},
                "codebases": {},
                "media_storages": {},
                "ml_storages": {},
                "projects": {},
                "video_generators": {},
                "hadron_node_connections": {},
                "metakanban_board_connections": {},
                "metatempo_tracker_connections": {},
                "orchestration_trigger_connections": {},
            },
        }

        assistant_browsers = self.assistant.datasourcebrowserconnection_set.all()
        assistant_file_systems = self.assistant.data_source_file_systems.all()
        assistant_sql_dbs = self.assistant.sql_database_connections.all()
        assistant_nosql_dbs = self.assistant.nosql_database_connections.all()
        assistant_kbs = self.assistant.documentknowledgebaseconnection_set.all()

        assistant_codebases = self.assistant.coderepositorystorageconnection_set.all()
        assistant_media_storages = self.assistant.datasourcemediastorageconnection_set.all()
        assistant_ml_storages = self.assistant.datasourcemlmodelconnection_set.all()
        assistant_projects = self.assistant.project_items.all()
        assistant_video_generators = self.assistant.videogeneratorconnection_set.all()

        hadron_node_connections = self.assistant.hadronnodeassistantconnection_set.all()
        metakanban_board_connections = self.assistant.metakanbanassistantconnection_set.all()
        metatempo_tracker_connections = self.assistant.metatempoassistantconnection_set.all()
        orchestration_trigger_connections = self.assistant.orchestrationreactantassistantconnection_set.all()
        mm_functions = self.assistant.customfunctionreference_set.all()

        mm_apis = self.assistant.customapireference_set.all()
        mm_scripts = self.assistant.customscriptreference_set.all()
        image_generation_capability = self.assistant.image_generation_capability
        time_awareness = self.assistant.time_awareness
        place_awareness = self.assistant.place_awareness
        reasoning_capability_choice = self.assistant.multi_step_reasoning_capability_choice

        # Tools: Image Generation Capability, Time Awareness, Place Awareness

        raw_data["tools"]["image_generation_capability"] = image_generation_capability
        raw_data["tools"]["time_awareness"] = time_awareness
        raw_data["tools"]["place_awareness"] = place_awareness
        raw_data["tools"]["reasoning_capability_choice"] = reasoning_capability_choice

        raw_data = self._populate_assistant_tools(
            mm_apis,
            mm_functions,
            mm_scripts,
            raw_data
        )

        raw_data = self._populate_assistant_data_sources(
            assistant_browsers,
            assistant_codebases,
            assistant_file_systems,
            assistant_kbs,
            assistant_media_storages,
            assistant_ml_storages,
            assistant_nosql_dbs,
            assistant_projects,
            assistant_sql_dbs,
            assistant_video_generators,
            hadron_node_connections,
            metakanban_board_connections,
            metatempo_tracker_connections,
            orchestration_trigger_connections,
            raw_data
        )

        self.raw_data = raw_data

        ##############################
        # Save the Index to Vector DB
        ##############################

        super().save(*args, **kwargs)

        self.raw_data = raw_data

        if (
            self.has_raw_data_changed() or
            self.vector_data is None or
            self.vector_data == []
        ):
            self._generate_embedding(raw_data)
            self._save_embedding()

        else:
            print("Raw data has not changed for Assistant with ID {self.assistant.id}. Skipping embedding generation.")

            logger.info(
                f"Raw data has not changed for Assistant with ID {self.assistant.id}. Skipping embedding generation.")

    def _populate_assistant_data_sources(
        self,
        assistant_browsers,
        assistant_codebases,
        assistant_file_systems,
        assistant_kbs,
        assistant_media_storages,
        assistant_ml_storages,
        assistant_nosql_dbs,
        assistant_projects,
        assistant_sql_dbs,
        assistant_video_generators,
        assistant_hadron_node_connections,
        assistant_metakanban_board_connections,
        assistant_metatempo_tracker_connections,
        assistant_orchestration_trigger_connections,
        raw_data
    ):
        from apps.datasource_file_systems.models import (
            DataSourceFileSystem
        )

        # Data Sources: Browsers

        for browser in assistant_browsers:
            browser: DataSourceBrowserConnection

            raw_data["data_sources"]["browsers"][browser.name] = {
                "type": browser.browser_type,
                "data_selectivity": browser.data_selectivity,
                "minimum_investigation_websites": browser.minimum_investigation_sites,
            }

        # Data Sources: File Systems

        for file_system in assistant_file_systems:
            file_system: DataSourceFileSystem

            raw_data["data_sources"]["file_systems"][file_system.name] = {
                "description": file_system.description,
                "is_read_only": file_system.is_read_only,
                "os_type": file_system.os_type,
            }

        # Data Sources: SQL DBs

        for sql_db in assistant_sql_dbs:
            sql_db: SQLDatabaseConnection

            raw_data["data_sources"]["sql_dbs"][sql_db.name] = {
                "description": sql_db.description,
                "host_uri": sql_db.host,
                "database_name": sql_db.database_name,
                "is_read_only": sql_db.is_read_only,
                "queries": {}
            }

            # Internal: Custom SQL Queries

            for query in sql_db.custom_queries.all():
                query: CustomSQLQuery

                raw_data["data_sources"]["sql_dbs"][sql_db.name]["queries"][query.name] = {
                    "query_content": query.sql_query,
                }

        # Data Sources: NoSQL DBs

        for nosql_db in assistant_nosql_dbs:
            nosql_db: NoSQLDatabaseConnection

            raw_data["data_sources"]["nosql_dbs"][nosql_db.name] = {
                "description": nosql_db.description,
                "host_uri": nosql_db.host,
                "bucket_name": nosql_db.bucket_name,
                "is_read_only": nosql_db.is_read_only,
                "queries": {}
            }

            # Internal: Custom NoSQL Queries

            for query in nosql_db.custom_queries.all():
                query: CustomNoSQLQuery

                raw_data["data_sources"]["nosql_dbs"][nosql_db.name]["queries"][query.name] = {
                    "query_content": query.nosql_query,
                }

        # Data Sources: Knowledge Bases

        for kb in assistant_kbs:
            kb: DocumentKnowledgeBaseConnection

            raw_data["data_sources"]["knowledge_bases"][kb.name] = {
                "description": kb.description,
                "vectorizer": kb.vectorizer,
            }

        # Data Sources: Code Bases

        for codebase in assistant_codebases:
            codebase: CodeRepositoryStorageConnection

            raw_data["data_sources"]["codebases"][codebase.name] = {
                "description": codebase.description,
                "vectorizer": codebase.vectorizer,
            }

        # Data Sources: Media Storages

        for media_storage in assistant_media_storages:
            media_storage: DataSourceMediaStorageConnection

            raw_data["data_sources"]["media_storages"][media_storage.name] = {
                "description": media_storage.description,
                "media_category": media_storage.media_category,
            }

            # Internal: Media Files (skip)
            pass

        # Data Sources: ML Storages

        for ml_storage in assistant_ml_storages:
            ml_storage: DataSourceMLModelConnection

            raw_data["data_sources"]["ml_storages"][ml_storage.name] = {
                "description": ml_storage.description,
                "models": {}
            }

            # Internal: ML Models

            for model in ml_storage.items.all():
                model: DataSourceMLModelItem

                raw_data["data_sources"]["ml_storages"][ml_storage.name]["models"][model.ml_model_name] = {
                    "model_name": model.ml_model_name,
                }

        # Data Sources: Projects

        for project in assistant_projects:
            project: ProjectItem

            raw_data["data_sources"]["projects"][project.project_name] = {
                "description": project.project_description,
                "priority": project.project_priority,
                "risk_level": project.project_risk_level,
                "status": project.project_status,
                "stakeholders": project.project_stakeholders,
                "teams": {}
            }

            # Internal: Teams

            for team in project.project_teams.all():
                team: ProjectTeamItem

                raw_data["data_sources"]["projects"][project.project_name]["teams"][team.team_name] = {
                    "team_lead": team.team_lead.username,
                }

        # Data Sources: Video Generators

        for video_generator in assistant_video_generators:
            video_generator: VideoGeneratorConnection

            raw_data["data_sources"]["video_generators"][video_generator.name] = {
                "provider": video_generator.provider,
            }

        # Data Sources: Hadron Prime Node Connections

        for hadron_node_connection in assistant_hadron_node_connections:
            hadron_node_connection: HadronNodeAssistantConnection

            raw_data["data_sources"]["hadron_node_connections"][hadron_node_connection.hadron_prime_node.node_name] = {
                "node_description": hadron_node_connection.hadron_prime_node.node_description,
            }

        # Data Sources: MetaKanban Board Connections

        for hadron_node_connection in assistant_metakanban_board_connections:
            hadron_node_connection: MetaKanbanAssistantConnection

            raw_data["data_sources"]["metakanban_board_connections"][
                hadron_node_connection.metakanban_board.title] = {
                "board_description": hadron_node_connection.metakanban_board.description,
            }

        # Data Sources: MetaTempo Tracker Connections

        for hadron_node_connection in assistant_metatempo_tracker_connections:
            hadron_node_connection: MetaTempoAssistantConnection

            raw_data["data_sources"]["metatempo_tracker_connections"][
                hadron_node_connection.metatempo_instance.board.title] = {
                "associated_board_title": hadron_node_connection.metatempo_instance.board.title,
                "associated_board_description": hadron_node_connection.metatempo_instance.board.description,
            }

        # Data Sources: Orchestration Trigger Connections

        for hadron_node_connection in assistant_orchestration_trigger_connections:
            hadron_node_connection: OrchestrationReactantAssistantConnection

            raw_data["data_sources"]["orchestration_trigger_connections"][
                hadron_node_connection.orchestration_maestro.name] = {
                "orchestrator_description": hadron_node_connection.orchestration_maestro.description,
            }

        # Pruning data sources and tools

        if len(raw_data["data_sources"]["browsers"]) > MAX_BROWSERS_PER_ASSISTANT:
            raw_data["data_sources"]["browsers"] = dict(
                list(
                    raw_data["data_sources"]["browsers"].items()
                )[:MAX_BROWSERS_PER_ASSISTANT]
            )

        if len(raw_data["data_sources"]["file_systems"]) > MAX_FILE_SYSTEMS_PER_ASSISTANT:
            raw_data["data_sources"]["file_systems"] = dict(
                list(
                    raw_data["data_sources"]["file_systems"].items()
                )[:MAX_FILE_SYSTEMS_PER_ASSISTANT]
            )

        if len(raw_data["data_sources"]["sql_dbs"]) > MAX_SQL_DBS_PER_ASSISTANT:
            raw_data["data_sources"]["sql_dbs"] = dict(
                list(
                    raw_data["data_sources"]["sql_dbs"].items()
                )[:MAX_SQL_DBS_PER_ASSISTANT]
            )

        if len(raw_data["data_sources"]["nosql_dbs"]) > MAX_NOSQL_DBS_PER_ASSISTANT:
            raw_data["data_sources"]["nosql_dbs"] = dict(
                list(
                    raw_data["data_sources"]["nosql_dbs"].items()
                )[:MAX_NOSQL_DBS_PER_ASSISTANT]
            )

        if len(raw_data["data_sources"]["knowledge_bases"]) > MAX_KNOWLEDGE_BASES_PER_ASSISTANT:
            raw_data["data_sources"]["knowledge_bases"] = dict(
                list(
                    raw_data["data_sources"]["knowledge_bases"].items()
                )[:MAX_KNOWLEDGE_BASES_PER_ASSISTANT]
            )

        if len(raw_data["data_sources"]["codebases"]) > MAX_KNOWLEDGE_BASES_PER_ASSISTANT:
            raw_data["data_sources"]["codebases"] = dict(
                list(
                    raw_data["data_sources"]["codebases"].items()
                )[:MAX_KNOWLEDGE_BASES_PER_ASSISTANT]
            )

        if len(raw_data["data_sources"]["media_storages"]) > MAX_MEDIA_STORAGES_PER_ASSISTANT:
            raw_data["data_sources"]["media_storages"] = dict(
                list(
                    raw_data["data_sources"]["media_storages"].items()
                )[:MAX_MEDIA_STORAGES_PER_ASSISTANT]
            )

        if len(raw_data["data_sources"]["ml_storages"]) > MAX_ML_STORAGES_PER_ASSISTANT:
            raw_data["data_sources"]["ml_storages"] = dict(
                list(
                    raw_data["data_sources"]["ml_storages"].items()
                )[:MAX_ML_STORAGES_PER_ASSISTANT]
            )

        if len(raw_data["data_sources"]["projects"]) > MAX_PROJECTS_PER_ASSISTANT:
            raw_data["data_sources"]["projects"] = dict(
                list(
                    raw_data["data_sources"]["projects"].items()
                )[:MAX_PROJECTS_PER_ASSISTANT]
            )

        if len(raw_data["data_sources"]["video_generators"]) > MAX_VIDEO_GENERATORS_PER_ASSISTANT:
            raw_data["data_sources"]["video_generators"] = dict(
                list(
                    raw_data["data_sources"]["video_generators"].items()
                )[:MAX_VIDEO_GENERATORS_PER_ASSISTANT]
            )

        if len(raw_data["data_sources"]["hadron_node_connections"]) > MAX_HADRON_NODES_PER_ASSISTANT:
            raw_data["data_sources"]["hadron_node_connections"] = dict(
                list(
                    raw_data["data_sources"]["hadron_node_connections"].items()
                )[:MAX_HADRON_NODES_PER_ASSISTANT]
            )

        if len(raw_data["data_sources"]["metakanban_board_connections"]) > MAX_METAKANBAN_BOARDS_PER_ASSISTANT:
            raw_data["data_sources"]["metakanban_board_connections"] = dict(
                list(
                    raw_data["data_sources"]["metakanban_board_connections"].items()
                )[:MAX_HADRON_NODES_PER_ASSISTANT]
            )

        if len(raw_data["data_sources"]["metatempo_tracker_connections"]) > MAX_METATEMPO_TRACKERS_PER_ASSISTANT:
            raw_data["data_sources"]["metatempo_tracker_connections"] = dict(
                list(
                    raw_data["data_sources"]["metatempo_tracker_connections"].items()
                )[:MAX_METATEMPO_TRACKERS_PER_ASSISTANT]
            )

        if len(
            raw_data["data_sources"]["orchestration_trigger_connections"]) > MAX_ORCHESTRATION_TRIGGERS_PER_ASSISTANT:
            raw_data["data_sources"]["orchestration_trigger_connections"] = dict(
                list(
                    raw_data["data_sources"]["orchestration_trigger_connections"].items()
                )[:MAX_ORCHESTRATION_TRIGGERS_PER_ASSISTANT]
            )

        if len(raw_data["tools"]["functions"]) > MAX_FUNCTIONS_PER_ASSISTANT:
            raw_data["tools"]["functions"] = list(
                raw_data["tools"]["functions"]
            )[:MAX_FUNCTIONS_PER_ASSISTANT]

        if len(raw_data["tools"]["apis"]) > MAX_APIS_PER_ASSISTANT:
            raw_data["tools"]["apis"] = list(
                raw_data["tools"]["apis"]
            )[:MAX_APIS_PER_ASSISTANT]

        if len(raw_data["tools"]["scripts"]) > MAX_SCRIPTS_PER_ASSISTANT:
            raw_data["tools"]["scripts"] = list(
                raw_data["tools"]["scripts"]
            )[:MAX_SCRIPTS_PER_ASSISTANT]

        return raw_data

    def _populate_assistant_tools(
        self,
        mm_apis,
        mm_functions,
        mm_scripts,
        raw_data
    ):

        # Tools: Functions

        for function_ref in mm_functions:
            function_ref: CustomFunctionReference

            raw_data["tools"]["functions"].append({
                "name": function_ref.custom_function.name,
                "description": function_ref.custom_function.description,
            })

        # Tools: APIs

        for api_ref in mm_apis:
            api_ref: CustomAPIReference

            raw_data["tools"]["apis"].append({
                "name": api_ref.custom_api.name,
                "description": api_ref.custom_api.description,
            })

        # Tools: Scripts

        for script_ref in mm_scripts:
            script_ref: CustomScriptReference

            raw_data["tools"]["scripts"].append({
                "name": script_ref.custom_script.name,
                "description": script_ref.custom_script.description,
            })

        return raw_data

    def _generate_embedding(self, raw_data):
        from apps.core.generative_ai.gpt_openai_manager import (
            OpenAIGPTClientManager
        )

        c = OpenAIGPTClientManager.get_naked_client(
            llm_model=self.assistant.llm_model
        )

        raw_data_text = json.dumps(
            raw_data,
            indent=2
        )

        try:
            response = c.embeddings.create(
                input=raw_data_text,
                model=OpenAIEmbeddingModels.TEXT_EMBEDDING_3_LARGE
            )

            embedding_vector = response.data[0].embedding

            self.vector_data = embedding_vector

        except Exception as e:
            logger.error(f"Error in generating embedding: {e}")

            self.vector_data = []

    def _save_embedding(self):
        if self.vector_data:
            x = np.array(
                [
                    self.vector_data
                ],
                dtype=np.float32
            ).reshape(
                1,
                OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS
            )

            xids = np.array(
                [
                    self.id
                ],
                dtype=np.int64
            )

            index_path = self._get_index_path()

            if not os.path.exists(index_path):
                index = faiss.IndexIDMap(
                    faiss.IndexFlatL2(
                        OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS
                    )
                )

            else:
                index = faiss.read_index(index_path)

                if not isinstance(
                    index,
                    faiss.IndexIDMap
                ):
                    index = faiss.IndexIDMap(index)

                index.remove_ids(xids)

            index.add_with_ids(
                x,
                xids
            )

            faiss.write_index(
                index,
                index_path
            )

    def has_raw_data_changed(self):
        raw_data_str = json.dumps(
            self.raw_data,
            sort_keys=True
        )

        new_raw_data_hash = hashlib.sha256(
            raw_data_str.encode('utf-8')
        ).hexdigest()

        if self.raw_data_hash == new_raw_data_hash:
            return False

        self.raw_data_hash = new_raw_data_hash

        return True
