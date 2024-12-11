#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
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
#   For permission inquiries, please contact: admin@Bimod.io.
#

import logging

from django.contrib import messages

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.assistants.models import Assistant

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.datasource_nosql.forms import (
    CustomNoSQLQueryForm
)

from apps.datasource_nosql.models import (
    NoSQLDatabaseConnection
)

from apps.organization.models import Organization

from apps.user_permissions.utils import (
    PermissionNames
)

from config.settings import MAX_NOSQL_QUERIES_PER_DB
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class NoSQLDatabaseView_QueryCreate(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user

        try:
            user_orgs = Organization.objects.filter(
                users__in=[context_user]
            )

            db_c = NoSQLDatabaseConnection.objects.filter(
                assistant__in=Assistant.objects.filter(
                    organization__in=user_orgs
                )
            )

            context['database_connections'] = db_c
            context['form'] = CustomNoSQLQueryForm()

        except Exception as e:
            logger.error(f"User: {context_user} - NoSQL Query - Create Error: {e}")
            messages.error(self.request, 'An error occurred while creating NoSQL Query.')

            return context

        return context

    def post(self, request, *args, **kwargs):
        form = CustomNoSQLQueryForm(request.POST)

        ##############################
        # PERMISSION CHECK FOR - ADD_CUSTOM_NOSQL_QUERIES
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.ADD_CUSTOM_NOSQL_QUERIES
        ):
            messages.error(self.request, "You do not have permission to create custom NoSQL queries.")
            return redirect('datasource_nosql:list_queries')
        ##############################

        if form.is_valid():

            database_connection = form.cleaned_data['database_connection']
            n_nosql_queries = database_connection.custom_queries.count()

            if n_nosql_queries > MAX_NOSQL_QUERIES_PER_DB:
                messages.error(request,
                               f'Assistant has reached the maximum number of NOSQL queries per database connection ({MAX_NOSQL_QUERIES_PER_DB}).')

                return redirect('datasource_nosql:list_queries')

            form.save()

            logger.info("NoSQL Query created.")
            messages.success(request, "NoSQL Query created successfully.")

            return redirect('datasource_nosql:create_query')

        else:
            logger.error("Error creating NoSQL Query.")
            messages.error(request, "Error creating NoSQL Query.")

            context = self.get_context_data(**kwargs)
            context['form'] = form

            return self.render_to_response(context)
