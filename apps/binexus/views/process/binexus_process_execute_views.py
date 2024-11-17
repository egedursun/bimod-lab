#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: binexus_process_rerun_views.py
#  Last Modified: 2024-10-22 18:39:29
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-22 18:39:29
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

from apps.binexus.models import BinexusProcess
from apps.core.binexus.binexus_executor import BinexusExecutionManager
from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.user_permissions.utils import PermissionNames

logger = logging.getLogger(__name__)


class BinexusView_ProcessExecute(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - EXECUTE_BINEXUS_PROCESSES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.EXECUTE_BINEXUS_PROCESSES):
            messages.error(self.request, "You do not have permission to execute Binexus Processes.")
            return redirect('binexus:process_detail', pk=kwargs.get('pk'))
        ##############################

        process_id = kwargs.get('pk')
        process_object: BinexusProcess = BinexusProcess.objects.get(id=process_id)
        try:
            xc = BinexusExecutionManager(binexus_process=process_object)
        except Exception as e:
            messages.error(request, f"Error occurred while executing the process: {e}")
            return redirect('binexus:process_detail', pk=kwargs.get('pk'))

        try:
            success, error = xc.execute_binexus()
            if error is not None:
                logger.error(f"Error occurred while executing the process: {error}")
                messages.error(request, f"Error occurred while executing the process: {error}")
                return redirect('binexus:process_detail', pk=kwargs.get('pk'))
        except Exception as e:
            logger.error(f"Error occurred while executing the process: {e}")
            messages.error(request, f"Error occurred while executing the process: {e}")
            return redirect('binexus:process_detail', pk=kwargs.get('pk'))

        logger.info(f"Process executed successfully.")
        messages.success(request, f"Process executed successfully.")
        return redirect('binexus:process_detail', pk=kwargs.get('pk'))
