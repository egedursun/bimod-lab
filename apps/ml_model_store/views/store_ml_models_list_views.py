#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: store_ml_models_list_views.py
#  Last Modified: 2024-11-08 14:44:27
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-08 14:45:54
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from collections import defaultdict

from django.contrib import messages

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.datasource_ml_models.models import (
    DataSourceMLModelConnection
)

from apps.ml_model_store.models import (
    MLModelIntegration
)

from apps.organization.models import Organization

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import TemplateLayout


class MLModelStoreView_StoreMLModelsList(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_ML_MODEL_INTEGRATIONS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.LIST_ML_MODEL_INTEGRATIONS
        ):
            messages.error(self.request, "You do not have permission to list ML Model Integrations.")
            return context
        ##############################

        all_ml_integrations = MLModelIntegration.objects.all()

        category_groups = defaultdict(list)

        for ml_integration in all_ml_integrations:
            category_groups[
                ml_integration.get_model_category_display()
            ].append(
                ml_integration
            )

        user_orgs = Organization.objects.filter(
            users__in=[self.request.user]
        )

        ml_store_connections = DataSourceMLModelConnection.objects.filter(
            assistant__organization__in=user_orgs
        )

        context['category_groups'] = dict(category_groups)
        context['ml_store_connections'] = ml_store_connections

        return context
