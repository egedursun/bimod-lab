#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: list_ml_items_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:46
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
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_ml_models.models import DataSourceMLModelConnection, DataSourceMLModelItem
from apps.datasource_ml_models.utils import DELETE_ALL_ML_ITEMS_SPECIFIER
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


logger = logging.getLogger(__name__)


class MLModelView_ItemList(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_ML_MODEL_FILES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_ML_MODEL_FILES):
            messages.error(self.request, "You do not have permission to list ML Model files.")
            return context
        ##############################

        context_user = self.request.user
        conn_by_orgs = []
        orgs = context_user.organizations.all()
        for org in orgs:
            agents_data = []
            agents = Assistant.objects.filter(organization=org)
            for agent in agents:
                conns_data = []
                conns = DataSourceMLModelConnection.objects.filter(assistant=agent)
                for conn in conns:
                    items = DataSourceMLModelItem.objects.filter(ml_model_base=conn)
                    page = self.request.GET.get('page', 1)
                    paginator = Paginator(items, 5)  # Show 5 items per page
                    try:
                        paginated_items = paginator.page(page)
                    except PageNotAnInteger:
                        paginated_items = paginator.page(1)
                    except EmptyPage:
                        paginated_items = paginator.page(paginator.num_pages)
                    conns_data.append({'connection': conn, 'items': paginated_items})
                agents_data.append({'assistant': agent, 'ml_model_connections': conns_data})
            conn_by_orgs.append({'organization': org, 'assistants': agents_data})
        context['connections_by_organization'] = conn_by_orgs
        logger.info(f"ML Model Items were listed.")
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - DELETE_ML_MODEL_FILES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_ML_MODEL_FILES):
            messages.error(self.request, "You do not have permission to delete ML Model files.")
            return redirect('datasource_ml_models:item_list')
        ##############################

        mgr_id = request.POST.get('storage_id')
        chosen_insts = request.POST.getlist('selected_items')
        chosen_insts = [item for item in chosen_insts if item]
        if DELETE_ALL_ML_ITEMS_SPECIFIER in request.POST:
            DataSourceMLModelItem.objects.filter(ml_model_base__id=mgr_id).delete()
            logger.info(f"All ML models in the selected connection have been deleted.")
            messages.success(request, 'All ML models in the selected connection have been deleted.')
        elif chosen_insts:
            DataSourceMLModelItem.objects.filter(id__in=chosen_insts).delete()
            logger.info(f"Selected ML models have been deleted.")
            messages.success(request, 'Selected ML models have been deleted.')
        return redirect('datasource_ml_models:item_list')
