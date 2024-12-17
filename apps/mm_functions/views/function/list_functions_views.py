#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: list_functions_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:40
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

from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.mm_functions.models import (
    CustomFunction
)

from apps.organization.models import (
    Organization
)

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class CustomFunctionView_List(LoginRequiredMixin, TemplateView):
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_FUNCTIONS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.LIST_FUNCTIONS
        ):
            messages.error(self.request, "You do not have permission to list custom functions.")

            return context
        ##############################

        context_user = self.request.user

        conn_orgs = Organization.objects.filter(
            users__in=[context_user]
        )

        users_of_conn_orgs = User.objects.filter(
            profile__user__in=[
                user for org in conn_orgs for user in org.users.all()
            ]
        )

        functions_list = CustomFunction.objects.filter(
            created_by_user__in=users_of_conn_orgs
        )

        search_query = self.request.GET.get('search', '')

        if search_query:
            functions_list = functions_list.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        paginator = Paginator(functions_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        context['functions'] = page_obj.object_list
        context['total_functions'] = CustomFunction.objects.count()

        context['public_functions'] = CustomFunction.objects.filter(
            is_public=True
        ).count()

        context['private_functions'] = CustomFunction.objects.filter(
            is_public=False
        ).count()

        context['search_query'] = search_query
        logger.info(f"User: {self.request.user.id} is listing custom functions.")

        return context
