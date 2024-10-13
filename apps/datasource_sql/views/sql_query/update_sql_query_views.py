#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: update_sql_query_views.py
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
#   For permission inquiries, please contact: admin@br6.in.
#


from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_sql.forms import CustomSQLQueryForm
from apps.datasource_sql.models import CustomSQLQuery, SQLDatabaseConnection
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class SQLDatabaseView_QueryUpdate(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        query = get_object_or_404(CustomSQLQuery, id=kwargs['pk'])
        user_orgs = context_user.organizations.all()
        db_c = SQLDatabaseConnection.objects.filter(assistant__in=Assistant.objects.filter(organization__in=user_orgs))
        context['database_connections'] = db_c
        context['form'] = CustomSQLQueryForm(instance=query)
        context['query'] = query
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - UPDATE_CUSTOM_SQL_QUERIES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_CUSTOM_SQL_QUERIES):
            messages.error(self.request, "You do not have permission to update custom SQL queries.")
            return redirect('datasource_sql:list_queries')
        ##############################

        query = get_object_or_404(CustomSQLQuery, id=kwargs['pk'])
        form = CustomSQLQueryForm(request.POST, instance=query)
        if form.is_valid():
            form.save()
            messages.success(request, "SQL Query updated successfully.")
            return redirect('datasource_sql:list_queries')
        else:
            messages.error(request, "Error updating SQL Query: " + str(form.errors))
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)
