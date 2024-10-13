#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: create_nosql_query_views.py
#  Last Modified: 2024-10-12 13:22:01
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-12 13:22:01
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.assistants.models import Assistant
from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.datasource_nosql.forms import CustomNoSQLQueryForm
from apps.datasource_nosql.models import NoSQLDatabaseConnection
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class NoSQLDatabaseView_QueryCreate(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        user_orgs = context_user.organizations.all()
        db_c = NoSQLDatabaseConnection.objects.filter(assistant__in=Assistant.objects.filter(organization__in=user_orgs))
        context['database_connections'] = db_c
        context['form'] = CustomNoSQLQueryForm()
        return context

    def post(self, request, *args, **kwargs):
        form = CustomNoSQLQueryForm(request.POST)

        ##############################
        # PERMISSION CHECK FOR - ADD_CUSTOM_NOSQL_QUERIES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_CUSTOM_NOSQL_QUERIES):
            messages.error(self.request, "You do not have permission to create custom NoSQL queries.")
            return redirect('datasource_nosql:list_queries')
        ##############################

        if form.is_valid():
            form.save()
            messages.success(request, "NoSQL Query created successfully.")
            return redirect('datasource_nosql:create_query')
        else:
            messages.error(request, "Error creating NoSQL Query.")
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)
