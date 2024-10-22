#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: create_sql_database_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:41
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
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_sql.forms import SQLDatabaseConnectionForm
from apps.datasource_sql.utils import DBMS_CHOICES
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


logger = logging.getLogger(__name__)


class SQLDatabaseView_ManagerCreate(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        user_orgs = context_user.organizations.all()
        agents = Assistant.objects.filter(organization__in=user_orgs)
        context['dbms_choices'] = DBMS_CHOICES
        context['form'] = SQLDatabaseConnectionForm()
        context['assistants'] = agents
        return context

    def post(self, request, *args, **kwargs):
        form = SQLDatabaseConnectionForm(request.POST)

        ##############################
        # PERMISSION CHECK FOR - ADD_SQL_DATABASES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_SQL_DATABASES):
            messages.error(self.request, "You do not have permission to create SQL Data Sources.")
            return redirect('datasource_sql:list')
        ##############################

        if form.is_valid():
            form.save()
            logger.info("SQL Data Source created.")
            messages.success(request, "SQL Data Source created successfully.")
            return redirect('datasource_sql:create')
        else:
            logger.error("Error creating SQL Data Source.")
            messages.error(request, "Error creating SQL Data Source.")
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)
