#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_all_metakanban_boards_views.py
#  Last Modified: 2024-10-30 19:17:56
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-30 19:17:57
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

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.metakanban.models import MetaKanbanBoard
from apps.organization.models import Organization

from apps.user_permissions.utils import (
    PermissionNames
)

logger = logging.getLogger(__name__)


class SettingsView_DeleteAllMetaKanbanBoards(View, LoginRequiredMixin):
    def post(self, request, *args, **kwargs):
        user = request.user

        user_orgs = Organization.objects.filter(
            users__in=[user]
        ).all()

        metakanban_boards = MetaKanbanBoard.objects.filter(
            project__organization__in=user_orgs
        ).all()

        confirmation_field = request.POST.get('confirmation', None)

        if confirmation_field != 'CONFIRM DELETING ALL METAKANBAN BOARDS':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL METAKANBAN BOARDS'.")
            logger.error(f"Invalid confirmation field: {confirmation_field}")

            return redirect('user_settings:settings')

        ##############################
        # PERMISSION CHECK FOR - DELETE_METAKANBAN_BOARD
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DELETE_METAKANBAN_BOARD
        ):
            messages.error(self.request, "You do not have permission to delete MetaKanban boards.")

            return redirect('user_settings:settings')
        ##############################

        try:
            for board in metakanban_boards:
                board.delete()

            messages.success(request, "All MetaKanban boards associated with your account have been deleted.")
            logger.info(f"All MetaKanban boards associated with User: {user.id} have been deleted.")

        except Exception as e:
            messages.error(request, f"Error deleting MetaKanban boards: {e}")
            logger.error(f"Error deleting MetaKanban boards: {e}")

        return redirect('user_settings:settings')
