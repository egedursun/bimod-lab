#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: create_sql_query_views.py
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
from apps.datasource_sql.forms import CustomSQLQueryForm
from apps.datasource_sql.models import SQLDatabaseConnection
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from config.settings import MAX_SQL_QUERIES_PER_DB
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class SQLDatabaseView_QueryCreate(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user

        try:
            user_orgs = Organization.objects.filter(users__in=[context_user])
            db_c = SQLDatabaseConnection.objects.filter(
                assistant__in=Assistant.objects.filter(organization__in=user_orgs))
            context['database_connections'] = db_c
            context['form'] = CustomSQLQueryForm()

        except Exception as e:
            logger.error(f"User: {context_user} - SQL Query - Create Error: {e}")
            messages.error(self.request, 'An error occurred while creating SQL Query.')
            return context

        return context

    def post(self, request, *args, **kwargs):
        form = CustomSQLQueryForm(request.POST)

        ##############################
        # PERMISSION CHECK FOR - ADD_CUSTOM_SQL_QUERIES
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.ADD_CUSTOM_SQL_QUERIES
        ):
            messages.error(self.request, "You do not have permission to create custom SQL queries.")
            return redirect('datasource_sql:list_queries')
        ##############################

        if form.is_valid():

            # check the number of NOSQL database connections assistant has
            database_connection = form.cleaned_data['database_connection']

            n_sql_queries = database_connection.custom_queries.count()
            if n_sql_queries > MAX_SQL_QUERIES_PER_DB:
                messages.error(request,
                               f'Assistant has reached the maximum number of SQL queries per database connection ({MAX_SQL_QUERIES_PER_DB}).')
                return redirect('datasource_sql:list_queries')

            form.save()
            logger.info("SQL Query created.")

            messages.success(request, "SQL Query created successfully.")
            return redirect('datasource_sql:create_query')

        else:
            logger.error("Error creating SQL Query.")
            messages.error(request, "Error creating SQL Query.")

            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)
