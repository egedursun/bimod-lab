#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: update_nosql_query_views.py
#  Last Modified: 2024-10-12 13:22:36
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-12 13:22:36
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
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps.assistants.models import Assistant

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.datasource_nosql.forms import (
    CustomNoSQLQueryForm
)

from apps.datasource_nosql.models import (
    CustomNoSQLQuery,
    NoSQLDatabaseConnection
)

from apps.organization.models import Organization

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class NoSQLDatabaseView_QueryUpdate(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user

        try:
            query = get_object_or_404(
                CustomNoSQLQuery,
                id=kwargs['pk']
            )

            user_orgs = Organization.objects.filter(
                users__in=[context_user]
            )

            db_c = NoSQLDatabaseConnection.objects.filter(
                assistant__in=Assistant.objects.filter(
                    organization__in=user_orgs
                )
            )

            context['database_connections'] = db_c

            context['form'] = CustomNoSQLQueryForm(
                instance=query
            )

            context['query'] = query

        except Exception as e:
            logger.error(f"User: {context_user} - NoSQL Query - Update Error: {e}")
            messages.error(self.request, 'An error occurred while updating NoSQL Query.')

            return context

        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - UPDATE_CUSTOM_NOSQL_QUERIES
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.UPDATE_CUSTOM_NOSQL_QUERIES
        ):
            messages.error(self.request, "You do not have permission to update custom NoSQL queries.")
            return redirect('datasource_nosql:list_queries')
        ##############################

        query = get_object_or_404(
            CustomNoSQLQuery,
            id=kwargs['pk']
        )

        form = CustomNoSQLQueryForm(
            request.POST,
            instance=query
        )

        if form.is_valid():
            form.save()
            logger.info("NoSQL Query updated.")
            messages.success(request, "NoSQL Query updated successfully.")

            return redirect('datasource_nosql:list_queries')

        else:
            logger.error("Error updating NoSQL Query: " + str(form.errors))
            messages.error(request, "Error updating NoSQL Query: " + str(form.errors))

            context = self.get_context_data(**kwargs)
            context['form'] = form

            return self.render_to_response(context)
