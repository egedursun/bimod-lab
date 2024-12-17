#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: list_video_generator_connections_views.py
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

from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.organization.models import Organization

from apps.user_permissions.utils import (
    PermissionNames
)

from apps.video_generations.models import (
    VideoGeneratorConnection
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class VideoGeneratorView_Connections(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_VIDEO_GENERATOR_CONNECTIONS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.LIST_VIDEO_GENERATOR_CONNECTIONS
        ):
            messages.error(self.request, "You do not have permission to list video generator connections.")

            return context
        ##############################

        user_organizations = Organization.objects.filter(
            users__in=[self.request.user]
        )

        context['video_generator_connections'] = VideoGeneratorConnection.objects.filter(
            organization__in=user_organizations
        )

        logger.info(f"Video Generator Connections were listed by User: {self.request.user.id}.")

        return context
