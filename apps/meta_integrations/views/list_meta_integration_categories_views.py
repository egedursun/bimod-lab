#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: list_meta_integration_categories_views.py
#  Last Modified: 2024-11-06 17:50:32
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-06 17:50:33
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.contrib import messages

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.meta_integrations.models import (
    MetaIntegrationCategory
)

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import TemplateLayout


class MetaIntegrationView_MetaIntegrationCategoryList(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_PLUG_AND_PLAY_TEAMS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.LIST_PLUG_AND_PLAY_TEAMS
        ):
            messages.error(self.request, "You do not have permission to list plug and play teams.")
            return context
        ##############################

        categories = MetaIntegrationCategory.objects.all().order_by("category_name")
        context['categories'] = categories

        total_boiler_plate_teams = 0

        for category in categories:
            total_boiler_plate_teams += category.metaintegrationteam_set.count()

        context['total_teams'] = total_boiler_plate_teams

        return context
