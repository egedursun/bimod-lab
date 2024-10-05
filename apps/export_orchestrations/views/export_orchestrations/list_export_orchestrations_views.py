#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: list_export_orchestrations_views.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:44
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: list_export_orchestrations_views.py
#  Last Modified: 2024-09-28 15:08:41
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:53:00
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.export_orchestrations.models import ExportOrchestrationAPI
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from config.settings import MAX_ORCHESTRATIONS_EXPORTS_ORGANIZATION
from web_project import TemplateLayout


class ListExportOrchestrationsView(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_EXPORT_ORCHESTRATION
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_EXPORT_ORCHESTRATION):
            messages.error(self.request, "You do not have permission to list Export Orchestration APIs.")
            return context
        ##############################

        user_context = self.request.user
        max_export_assistants = MAX_ORCHESTRATIONS_EXPORTS_ORGANIZATION
        organization_data = []
        organizations = Organization.objects.filter(users=user_context)

        for organization in organizations:
            export_assistants_count = organization.exported_orchestrations.count()
            assistants_percentage = round((export_assistants_count / max_export_assistants) * 100, 2)
            export_assistants = organization.exported_orchestrations.all()
            for assistant in export_assistants:
                assistant.usage_percentage = 100  # Set this to actual percentage if needed
            organization_data.append({
                'organization': organization, 'export_assistants_count': export_assistants_count,
                'assistants_percentage': assistants_percentage, 'export_assistants': export_assistants,
                'limit': max_export_assistants
            })
        export_assistants = ExportOrchestrationAPI.objects.filter(created_by_user=user_context)
        context["user"] = user_context
        context["organization_data"] = organization_data
        context["export_assistants"] = export_assistants
        return context
