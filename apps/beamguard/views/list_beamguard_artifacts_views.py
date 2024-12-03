#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: list_beamguard_artifacts_views.py
#  Last Modified: 2024-12-02 01:22:07
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-02 01:22:07
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
from django.views.generic import TemplateView

from apps.assistants.models import Assistant
from apps.beamguard.models import BeamGuardArtifact

from apps.beamguard.utils import (
    BeamGuardConfirmationStatusesNames,
    BeamGuardArtifactTypesNames
)
from apps.core.user_permissions.permission_manager import UserPermissionManager

from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class BeamGuardView_ListArtifacts(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data())

        ##############################
        # PERMISSION CHECK FOR - LIST_BEAMGUARD_ARTIFACTS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.LIST_BEAMGUARD_ARTIFACTS
        ):
            messages.error(self.request, "You do not have permission to list BeamGuard artifacts.")
            return context
        ##############################

        user_orgs = Organization.objects.filter(
            users__in=[self.request.user]
        )
        org_assistants = Assistant.objects.filter(
            organization__in=user_orgs
        )
        beamguard_artifacts = BeamGuardArtifact.objects.filter(
            assistant__in=org_assistants
        )

        context_obj_grouped_by_org_and_assistant__sql = {}
        context_obj_grouped_by_org_and_assistant__nosql = {}
        context_obj_grouped_by_org_and_assistant__file_system = {}

        """
            1: {
                "organization_data": {
                    "id": 1,
                    ...
                }
                "assistants": {
                    11: {
                        "assistants_data": {
                            "id": 11,
                            ...
                        },
                        "beamguard_artifacts": {
                            "pending": [
                                { ... },
                            ],
                            "confirmed": [
                                { ... },
                            ],
                            "rejected": [
                                { ... },
                            ],
                        }
                    }
                }
            },
            ...
        """
        for user_org in user_orgs:
            user_org: Organization

            context_obj_grouped_by_org_and_assistant__sql[user_org.id] = {
                "organization_data": user_org,
                "assistants": {}
            }
            context_obj_grouped_by_org_and_assistant__nosql[user_org.id] = {
                "organization_data": user_org,
                "assistants": {}
            }
            context_obj_grouped_by_org_and_assistant__file_system[user_org.id] = {
                "organization_data": user_org,
                "assistants": {}
            }

            for org_assistant in org_assistants:
                org_assistant: Assistant

                if org_assistant.organization == user_org:

                    context_obj_grouped_by_org_and_assistant__sql[user_org.id]["assistants"][org_assistant.id] = {
                        "assistant_data": org_assistant,
                        "beamguard_artifacts": {
                            BeamGuardConfirmationStatusesNames.PENDING: [],
                            BeamGuardConfirmationStatusesNames.CONFIRMED: [],
                            BeamGuardConfirmationStatusesNames.REJECTED: [],
                        }
                    }

                    context_obj_grouped_by_org_and_assistant__nosql[user_org.id]["assistants"][org_assistant.id] = {
                        "assistant_data": org_assistant,
                        "beamguard_artifacts": {
                            BeamGuardConfirmationStatusesNames.PENDING: [],
                            BeamGuardConfirmationStatusesNames.CONFIRMED: [],
                            BeamGuardConfirmationStatusesNames.REJECTED: [],
                        }
                    }

                    context_obj_grouped_by_org_and_assistant__file_system[user_org.id]["assistants"][
                        org_assistant.id] = {
                        "assistant_data": org_assistant,
                        "beamguard_artifacts": {
                            BeamGuardConfirmationStatusesNames.PENDING: [],
                            BeamGuardConfirmationStatusesNames.CONFIRMED: [],
                            BeamGuardConfirmationStatusesNames.REJECTED: [],
                        }
                    }

                    for beamguard_artifact in beamguard_artifacts:

                        beamguard_artifact: BeamGuardArtifact
                        if beamguard_artifact.assistant == org_assistant:

                            if beamguard_artifact.type == BeamGuardArtifactTypesNames.SQL:
                                (
                                    context_obj_grouped_by_org_and_assistant__sql[user_org.id]
                                    ["assistants"][org_assistant.id]["beamguard_artifacts"]
                                    [beamguard_artifact.confirmation_status].append(beamguard_artifact)
                                )

                            elif beamguard_artifact.type == BeamGuardArtifactTypesNames.NOSQL:
                                (
                                    context_obj_grouped_by_org_and_assistant__nosql[user_org.id]
                                    ["assistants"][org_assistant.id]["beamguard_artifacts"]
                                    [beamguard_artifact.confirmation_status].append(beamguard_artifact)
                                )

                            elif beamguard_artifact.type == BeamGuardArtifactTypesNames.FILE_SYSTEM:
                                (
                                    context_obj_grouped_by_org_and_assistant__file_system[user_org.id]
                                    ["assistants"][org_assistant.id]["beamguard_artifacts"]
                                    [beamguard_artifact.confirmation_status].append(beamguard_artifact)
                                )

                        else:
                            # This artifact does not belong to this assistant.
                            continue
                else:
                    # This assistant does not belong to this organization.
                    continue

        context['data_object__sql'] = context_obj_grouped_by_org_and_assistant__sql
        context['data_object__nosql'] = context_obj_grouped_by_org_and_assistant__nosql
        context['data_object__file_system'] = context_obj_grouped_by_org_and_assistant__file_system

        context["user"] = self.request.user

        return context
