#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
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
    NoSQLDatabaseConnectionForm
)

from apps.datasource_nosql.utils import (
    NOSQL_DATABASE_CHOICES
)

from apps.organization.models import Organization

from apps.user_permissions.utils import (
    PermissionNames
)

from config.settings import (
    MAX_NOSQL_DBS_PER_ASSISTANT
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class NoSQLDatabaseView_ManagerCreate(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user

        try:
            user_orgs = Organization.objects.filter(
                users__in=[context_user]
            )

            agents = Assistant.objects.filter(
                organization__in=user_orgs
            )

            context['dbms_choices'] = NOSQL_DATABASE_CHOICES
            context['form'] = NoSQLDatabaseConnectionForm()
            context['assistants'] = agents

        except Exception as e:
            logger.error(f"User: {context_user} - NoSQL Data Source - Create Error: {e}")
            messages.error(self.request, 'An error occurred while creating NoSQL Data Source.')

            return context

        return context

    def post(self, request, *args, **kwargs):
        form = NoSQLDatabaseConnectionForm(request.POST)

        ##############################
        # PERMISSION CHECK FOR - ADD_NOSQL_DATABASES
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.ADD_NOSQL_DATABASES
        ):
            messages.error(self.request, "You do not have permission to create NoSQL Data Sources.")
            return redirect('datasource_nosql:list')
        ##############################

        if form.is_valid():

            assistant = form.cleaned_data['assistant']

            n_nosql_dbs = assistant.nosql_database_connections.count()

            if n_nosql_dbs > MAX_NOSQL_DBS_PER_ASSISTANT:
                messages.error(request,
                               f'Assistant has reached the maximum number of NOSQL database connections ({MAX_NOSQL_DBS_PER_ASSISTANT}).')

                return redirect('datasource_nosql:list')

            form.save()

            logger.info("NoSQL Data Source created.")
            messages.success(request, "NoSQL Data Source created successfully.")

            return redirect('datasource_nosql:create')

        else:
            logger.error("Error creating NoSQL Data Source.")
            messages.error(request, "Error creating NoSQL Data Source.")

            context = self.get_context_data(**kwargs)
            context['form'] = form

            return self.render_to_response(context)
