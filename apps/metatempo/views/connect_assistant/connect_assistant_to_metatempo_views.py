#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: connect_assistant_to_metatempo_views.py
#  Last Modified: 2024-11-13 03:20:40
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-13 03:20:40
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

from apps.assistants.models import Assistant

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.metatempo.models import (
    MetaTempoConnection,
    MetaTempoAssistantConnection
)

from apps.organization.models import Organization

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class MetaTempoView_ConnectAssistantToMetaTempo(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        user_orgs = Organization.objects.filter(
            users__in=[self.request.user]
        ).all()

        assistants = Assistant.objects.filter(
            organization__in=user_orgs
        ).all()

        metatempo_instances = MetaTempoConnection.objects.filter(
            board__llm_model__organization__in=user_orgs
        ).all()

        context["assistants"] = assistants
        context["metatempo_instances"] = metatempo_instances

        context["existing_connections"] = MetaTempoAssistantConnection.objects.filter(
            assistant__organization__in=user_orgs
        ).all()

        return context

    def post(self, request, *args, **kwargs):
        assistant_id = self.request.POST.get("assistant_id")
        instance_id = self.request.POST.get("instance_id")

        ##############################
        # PERMISSION CHECK FOR - CONNECT_ASSISTANTS_TO_METATEMPO
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.CONNECT_ASSISTANTS_TO_METATEMPO
        ):
            messages.error(self.request, "You do not have permission to connect an assistant to a MetaTempo tracker.")

            return self.render_to_response(self.get_context_data())
        ##############################

        assistant = Assistant.objects.get(
            id=assistant_id
        )

        metatempo_instance = MetaTempoConnection.objects.get(
            id=instance_id
        )

        try:
            MetaTempoAssistantConnection.objects.create(
                assistant=assistant,
                metatempo_instance=metatempo_instance,
                created_by_user=self.request.user
            )

        except Exception as e:
            messages.error(
                self.request,
                f"Error while connecting assistant to MetaTempo tracker: {e}"
            )

            logger.error(f"Error while connecting assistant to MetaTempo tracker: {e}")

        messages.success(self.request, "Assistant connected to MetaTempo tracker successfully.")

        return self.render_to_response(self.get_context_data())
