#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: confirm_delete_video_generator_connection_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:45
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

from django.shortcuts import (
    get_object_or_404,
    redirect
)

from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.user_permissions.utils import (
    PermissionNames
)

from apps.video_generations.models import (
    VideoGeneratorConnection
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class VideoGeneratorView_ConfirmDelete(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        pk = self.kwargs.get('pk')

        video_generator_connection = get_object_or_404(
            VideoGeneratorConnection, pk=pk
        )

        context['video_generator_connection'] = video_generator_connection

        return context

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - DELETE_VIDEO_GENERATOR_CONNECTIONS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DELETE_VIDEO_GENERATOR_CONNECTIONS
        ):
            messages.error(self.request, "You do not have permission to delete video generator connections.")
            return redirect('video_generations:list')
        ##############################

        pk = self.kwargs.get('pk')

        video_generator_connection = get_object_or_404(
            VideoGeneratorConnection,
            pk=pk
        )

        try:
            video_generator_connection.delete()

        except Exception as e:
            logger.error(f"Video Generator Connection deletion failed. Error: {e}")
            messages.error(request,
                           f'The Video Generator Connection "{video_generator_connection.name}" could not be deleted.')

            return redirect('video_generations:list')

        logger.info(f"Video Generator Connection was deleted by User: {self.request.user.id}.")
        messages.success(request, 'Video Generator Connection deleted successfully.')

        return redirect('video_generations:list')
