#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: update_sql_database_views.py
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

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.assistants.models import Assistant

from apps.datasource_sql.forms import (
    SQLDatabaseConnectionForm
)

from apps.datasource_sql.models import (
    SQLDatabaseConnection
)

from apps.datasource_sql.utils import DBMS_CHOICES
from apps.organization.models import Organization

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class SQLDatabaseView_ManagerUpdate(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user

        try:
            conn = SQLDatabaseConnection.objects.get(
                id=kwargs['pk']
            )

            user_orgs = Organization.objects.filter(
                users__in=[context_user]
            )

            agents = Assistant.objects.filter(
                organization__in=user_orgs
            )

            context['dbms_choices'] = DBMS_CHOICES

            context['form'] = SQLDatabaseConnectionForm(
                instance=conn
            )

            context['assistants'] = agents
            context['connection'] = conn

        except Exception as e:
            logger.error(f"User: {context_user} - SQL Data Source - Update Error: {e}")
            messages.error(self.request, 'An error occurred while updating SQL Data Source.')
            return context

        return context

    def post(self, request, *args, **kwargs):
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - UPDATE_SQL_DATABASES
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.UPDATE_SQL_DATABASES
        ):
            messages.error(self.request, "You do not have permission to update SQL Data Sources.")
            return redirect('datasource_sql:list')
        ##############################

        conn = SQLDatabaseConnection.objects.get(
            id=kwargs['pk'],
            created_by_user=context_user
        )

        form = SQLDatabaseConnectionForm(
            request.POST,
            instance=conn
        )

        if form.is_valid():
            form.save()

            logger.info("SQL Data Source updated.")
            messages.success(request, "SQL Data Source updated successfully.")

            return redirect('datasource_sql:list')

        else:

            logger.error("Error updating SQL Data Source: " + str(form.errors))
            messages.error(request, "Error updating SQL Data Source: " + str(form.errors))
            context = self.get_context_data(**kwargs)
            context['form'] = form

            return self.render_to_response(context)
