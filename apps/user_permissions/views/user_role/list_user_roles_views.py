#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: list_user_roles_views.py
#  Last Modified: 2024-09-29 16:43:52
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-29 16:50:56
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.views.generic import TemplateView

from apps.organization.models import Organization
from apps.user_permissions.models import UserRole
from web_project import TemplateLayout


class ListUserRolesView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Fetch user roles from the database (you can filter by organization, etc.)
        user_organizations = Organization.objects.filter(
            users__in=[self.request.user]
        )
        user_roles = UserRole.objects.filter(
            organization__in=user_organizations
        )

        # Set up pagination
        paginator = Paginator(user_roles, 9)  # Show 9 roles per page
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context
