#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: action_003_meta_integrations.py
#  Last Modified: 2024-11-18 20:42:56
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-18 20:42:56
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
import os
import random
import uuid

from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.storage import default_storage

from apps.assistants.models import Assistant
from apps.core.semantor.semantor_executor import SemantorVectorSearchExecutionManager
from apps.leanmod.models import ExpertNetwork, ExpertNetworkAssistantReference, LeanAssistant
from apps.llm_core.models import LLMCore
from apps.meta_integrations.models import MetaIntegrationTeam
from apps.meta_integrations.utils import META_INTEGRATION_ORCHESTRATOR_STANDARD_INSTRUCTIONS, \
    META_INTEGRATION_LEANMOD_STANDARD_INSTRUCTIONS
from apps.orchestrations.models import Maestro, OrchestrationReactantAssistantConnection
from apps.organization.models import Organization
from apps.quick_setup_helper.utils import ASSISTANT_INTEGRATION_SEARCH_RELATED_LIMIT
from config import settings

logger = logging.getLogger(__name__)


def action__003_meta_integration_teams_create(
    metadata__user,
    metadata__organization,
    metadata__llm_core,
    response__assistant_use_cases_list
):
    try:

        # Define the storages
        total_created_assistants, total_created_leanmods, total_created_orchestrators = [], [], []

        # Search the most relevant assistants from the integrations
        xc = SemantorVectorSearchExecutionManager(user=metadata__user, llm_model=metadata__llm_core)
        for use_case_query in response__assistant_use_cases_list:
            search_results = xc.search_integrations(
                query=use_case_query,
                n_results=ASSISTANT_INTEGRATION_SEARCH_RELATED_LIMIT
            )

            team_references = {}
            for search_result in search_results:
                integration_raw_data = search_result.get("data")
                integration_teams = integration_raw_data.get("included_in_meta_integration_teams")
                for team_ref in integration_teams:
                    team_references[team_ref] = team_references.get(team_ref, 0) + 1

            # Determine the most referenced team
            most_referenced_team = None
            most_references = 0
            for team_ref, references in team_references.items():
                if references > most_references:
                    most_referenced_team = team_ref
                    most_references = references

            # Integrate the meta-integration team
            (
                integrated_assistants,
                integrated_leanmods,
                integrated_orchestrators
            ) = integrate_meta_integration_team_naked(
                user=metadata__user,
                organization=metadata__organization,
                llm_model=metadata__llm_core,
                team_name=most_referenced_team
            )

            total_created_assistants.extend(integrated_assistants)
            total_created_leanmods.append(integrated_leanmods)
            total_created_orchestrators.append(integrated_orchestrators)

    except Exception as e:
        logger.error(f"An error occurred while creating the meta integrations: {e}")
        return False, [], [], []

    logger.info(f"Meta integrations have been successfully created.")
    return True, total_created_assistants, total_created_leanmods, total_created_orchestrators


def integrate_meta_integration_team_naked(user: User, organization: Organization, llm_model: LLMCore, team_name: str):
    try:
        meta_integration_data: MetaIntegrationTeam = MetaIntegrationTeam.objects.get(meta_integration_name=team_name)
        integration_assistants = meta_integration_data.integration_assistants.all()

        # Integrate the assistants
        created_team_members, created_lean_assistant, orchestration_maestro = [], None, None
        for integration_data in integration_assistants:

            try:
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
                created_team_members.append(created_assistant)
            except Exception as e:
                logger.error(f"Error occurred while integrating the assistant: {e}")

        # Create the orchestrator for the assistants
        try:
            orchestration_maestro = Maestro.objects.create(
                organization=organization,
                llm_model=llm_model,
                name="Team Manager: " + meta_integration_data.meta_integration_name,
                description="Team Description: " + meta_integration_data.meta_integration_description,
                instructions=META_INTEGRATION_ORCHESTRATOR_STANDARD_INSTRUCTIONS,
                workflow_step_guide="",
                maximum_assistant_limits=10,
                response_template="",
                audience="Inherited from Team",
                tone="Inherited from Team",
                maestro_image=meta_integration_data.meta_integration_team_image,
                created_by_user=user,
                last_updated_by_user=user
            )
            orchestration_maestro.workers.set(created_team_members)
            orchestration_maestro.save()
        except Exception as e:
            logger.error(f"Error occurred while integrating the orchestrator: {e}")

        # Create the expert network, references and leanmod assistant
        try:
            expert_network = ExpertNetwork.objects.create(
                organization=organization,
                name="Team Expert Network: " + meta_integration_data.meta_integration_name,
                meta_description="Team Description: " + meta_integration_data.meta_integration_description,
                created_by_user=user,
                last_updated_by_user=user
            )
            expert_network.save()

            for team_member in created_team_members:
                created_expert_network_member = ExpertNetworkAssistantReference.objects.create(
                    assistant=team_member,
                    context_instructions=team_member.instructions,
                    created_by_user=user,
                    last_updated_by_user=user
                )
                created_expert_network_member.save()
                expert_network.assistant_references.add(created_expert_network_member)

            static_image_directory = os.path.join(settings.STATIC_ROOT, 'img', 'team-leanmod-oracle-avatars')
            unique_filename = None
            available_images = [f for f in os.listdir(static_image_directory) if f.endswith(('png', 'jpg', 'jpeg'))]
            if available_images:
                random_image = random.choice(available_images)
                random_image_path = os.path.join(static_image_directory, random_image)
                unique_filename = f'lean_assistant_images/{uuid.uuid4()}.png'
                with open(random_image_path, 'rb') as img_file:
                    default_storage.save(unique_filename, File(img_file))

            created_lean_assistant = LeanAssistant.objects.create(
                organization=organization,
                llm_model=llm_model,
                name="Oracle Assistant for Team: " + meta_integration_data.meta_integration_name,
                instructions=META_INTEGRATION_LEANMOD_STANDARD_INSTRUCTIONS,
                lean_assistant_image=unique_filename if available_images else None,
                created_by_user=user,
                last_updated_by_user=user
            )
            created_lean_assistant.expert_networks.set([expert_network])
            created_lean_assistant.save()
        except Exception as e:
            logger.error(f"Error occurred while integrating the expert network and lean assistant: {e}")

    except Exception as e:
        logger.error(f"An error occurred while integrating the meta integration team: {e}")
        return [], None, None

    # Connect Orchestrator to Reactant Assistants
    try:
        for assistant in created_team_members:
            assistant: Assistant

            OrchestrationReactantAssistantConnection.objects.create(
                assistant=assistant,
                orchestration_maestro=orchestration_maestro,
                created_by_user=user
            )

    except Exception as e:
        logger.error(f"Error while connecting Reactant assistants to the orchestrator maestro: {e}")
        return False, None

    logger.info(f"Meta integration team {team_name} has been successfully integrated.")
    return created_team_members, created_lean_assistant, orchestration_maestro
