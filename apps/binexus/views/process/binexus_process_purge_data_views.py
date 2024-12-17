#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: binexus_process_purge_data_views.py
#  Last Modified: 2024-10-23 02:02:53
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-23 02:02:53
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

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.shortcuts import redirect
from django.views import View

from apps.binexus.models import (
    BinexusProcess,
    BinexusEliteAgent
)

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.user_permissions.utils import (
    PermissionNames
)

logger = logging.getLogger(__name__)


class BinexusView_ProcessPurgeData(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - DELETE_BINEXUS_PROCESSES
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DELETE_BINEXUS_PROCESSES
        ):
            messages.error(self.request, "You do not have permission to delete Binexus Processes.")

            return redirect('binexus:process_list')
        ##############################

        process_id = kwargs.get('pk')

        try:
            process: BinexusProcess = BinexusProcess.objects.get(
                id=process_id
            )

            process.post_processing_history_average_fitness_per_epoch = []
            process.post_processing_history_best_fitness_per_epoch = []
            process.post_processing_history_worst_fitness_per_epoch = []
            process.post_processing_history_average_of_average_fitnesses = 0.0
            process.post_processing_history_average_of_best_fitnesses = 0.0
            process.post_processing_history_average_of_worst_fitnesses = 0.0
            process.post_processing_history_visual_chart = None

            process.save()

            logger.info(f"Binexus process internal information purged successfully.")

            elite_agents = BinexusEliteAgent.objects.filter(
                binexus_process=process
            )

            for elite_agent in elite_agents:
                elite_agent.delete()

            logger.info(f"Binexus elite agents purged successfully.")

        except Exception as e:
            logger.error(f"Error purging binexus process data: {e}")
            messages.error(request, f"Error purging binexus process data: {e}")

            return redirect(
                'binexus:process_detail',
                pk=process_id
            )

        messages.success(request, "Binexus process data purged successfully.")
        logger.info(f"Binexus process data purged successfully.")

        return redirect(
            'binexus:process_detail',
            pk=process_id
        )
