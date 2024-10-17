#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_nosql_query_views.py
#  Last Modified: 2024-10-12 22:17:26
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-17 01:17:28
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
#
#  Project: Bimod.io™
#  File: delete_nosql_query_views.py
#  Last Modified: 2024-10-12 13:22:13
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-12 13:22:13
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
from django.views.generic import DeleteView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.datasource_nosql.models import CustomNoSQLQuery
from apps.user_permissions.utils import PermissionNames


logger = logging.getLogger(__name__)


class NoSQLDatabaseView_QueryDelete(LoginRequiredMixin, DeleteView):
    model = CustomNoSQLQuery
    success_url = 'datasource_nosql:list_queries'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - DELETE_CUSTOM_NOSQL_QUERIES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_CUSTOM_NOSQL_QUERIES):
            messages.error(self.request, "You do not have permission to delete custom NoSQL queries.")
            return redirect('datasource_nosql:list_queries')
        ##############################

        self.object = self.get_object()
        self.object.delete()
        logger.info(f"NoSQL Query {self.object.name} was deleted.")
        messages.success(request, f'NoSQL Query {self.object.name} was deleted successfully.')
        return redirect(self.success_url)
