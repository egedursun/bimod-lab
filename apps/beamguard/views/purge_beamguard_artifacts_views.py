#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: purge_beamguard_artifacts_views.py
#  Last Modified: 2024-12-02 01:22:18
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-02 01:22:18
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

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames

logger = logging.getLogger(__name__)


class BeamGuardView_PurgeAllArtifacts(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = request.user

        ##############################
        # PERMISSION CHECK FOR - DISCARD_BEAMGUARD_ARTIFACTS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DISCARD_BEAMGUARD_ARTIFACTS
        ):
            messages.error(self.request, "You do not have permission to discard BeamGuard artifacts.")
            return redirect("beamguard:list")
        ##############################

        user_orgs = Organization.objects.filter(
            users__in=[user]
        )

        user_assistants = Assistant.objects.filter(
            organization__in=user_orgs
        )

        try:
            for assistant in user_assistants:
                assistant: Assistant

                beamguard_artifacts = assistant.beamguard_artifacts.all()

                for artifact in beamguard_artifacts:

                    try:
                        artifact.delete()

                    except Exception as e:
                        logger.error("Failed to purge the artifact with ID {artifact.id}: {e}")
                        continue

        except Exception as e:
            logger.error(f"BeamGuardView_PurgeAllArtifacts: Failed to purge all artifacts.")
            messages.error(request, 'Failed to purge all artifacts during the operation.')

        logger.info(f"BeamGuardView_PurgeAllArtifacts: All artifacts have been purged successfully.")
        messages.success(request, 'All artifacts have been purged successfully.')

        return redirect("beamguard:list")
