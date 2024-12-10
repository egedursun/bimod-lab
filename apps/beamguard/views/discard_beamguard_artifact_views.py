#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: discard_beamguard_artifact_views.py
#  Last Modified: 2024-12-02 22:27:05
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-02 22:27:06
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

from apps.core.beamguard.beamguard_executor import (
    BeamGuardExecutionManager
)

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.user_permissions.utils import PermissionNames

logger = logging.getLogger(__name__)


class BeamGuardView_DiscardArtifact(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        referer_url = request.META.get('HTTP_REFERER', '/')
        artifact_id = kwargs.get('pk')

        ##############################
        # PERMISSION CHECK FOR - DISCARD_BEAMGUARD_ARTIFACTS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DISCARD_BEAMGUARD_ARTIFACTS
        ):
            messages.error(self.request, "You do not have permission to discard BeamGuard artifacts.")
            return redirect(referer_url)
        ##############################

        try:
            success = BeamGuardExecutionManager.reject_and_discard_artifact(
                artifact_id=artifact_id
            )

            if success is True:
                logger.info(f"BeamGuardView_DiscardArtifact: Artifact with ID {artifact_id} has been discarded.")
                messages.success(request, 'Artifact has been discarded successfully.')

            else:
                logger.error(f"BeamGuardView_DiscardArtifact: Failed to discard artifact with ID {artifact_id}.")
                messages.error(request, 'Failed to discard the artifact, reverting.')

        except Exception as e:
            logger.error(f"BeamGuardView_DiscardArtifact: Failed to discard artifact with ID {artifact_id}.")
            messages.error(request, 'Failed to discard the artifact, reverting.')

        return redirect(referer_url)
