#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: create_nosql_database_views.py
#  Last Modified: 2024-10-12 13:21:03
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-12 13:21:03
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
from apps.datasource_nosql.forms import NoSQLDatabaseConnectionForm
from apps.datasource_nosql.utils import NOSQL_DATABASE_CHOICES
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class NoSQLDatabaseView_ManagerCreate(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        user_orgs = context_user.organizations.all()
        agents = Assistant.objects.filter(organization__in=user_orgs)
        context['dbms_choices'] = NOSQL_DATABASE_CHOICES
        context['form'] = NoSQLDatabaseConnectionForm()
        context['assistants'] = agents
        return context

    def post(self, request, *args, **kwargs):
        form = NoSQLDatabaseConnectionForm(request.POST)

        ##############################
        # PERMISSION CHECK FOR - ADD_NOSQL_DATABASES
        if not UserPermissionManager.is_authorized(
            user=self.request.user, operation=PermissionNames.ADD_NOSQL_DATABASES):
            messages.error(self.request, "You do not have permission to create NoSQL Data Sources.")
            return redirect('datasource_nosql:list')
        ##############################

        if form.is_valid():
            form.save()
            messages.success(request, "NoSQL Data Source created successfully.")
            return redirect('datasource_nosql:create')
        else:
            messages.error(request, "Error creating NoSQL Data Source.")
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)
