#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: main_dashboard_views.py
#  Last Modified: 2024-10-05 01:39:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:37
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

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import TemplateView

from apps.core.generative_ai.generative_ai_decode_manager import GenerativeAIDecodeController
from apps.dashboard.utils import INITIAL_STATISTICS_N_DAYS_BACK, build_statistics_for_graph
from apps.dashboard.utils.class_utils import TransactionStatisticsManager
from apps.llm_core.models import LLMCore
from apps.organization.models import Organization
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class DashboardView_Main(LoginRequiredMixin, TemplateView):
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = self.request.user

        try:
            orgs = Organization.objects.filter(users__in=[user])
            manager = TransactionStatisticsManager(user=user)
            data_statistics = manager.statistics
            last_n_days = INITIAL_STATISTICS_N_DAYS_BACK
            context["days"] = last_n_days
            ai_models = LLMCore.objects.filter(organization__in=orgs)
            context["llm_models"] = ai_models
            last_update_datetime = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
            context["last_update_datetime"] = last_update_datetime
            context = build_statistics_for_graph(statistics=data_statistics, context=context)
        except Exception as e:
            logger.error(f"Error getting main dashboard context data: {e}")
            return context

        logger.info(f"User: {user} - Statistics: {data_statistics}")
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        context_user = request.user

        try:
            ai_model = request.POST.get("llm_model")
            llm_core = LLMCore.objects.get(id=ai_model)
            manager = TransactionStatisticsManager(user=context_user)
            data_statistics = manager.statistics
            response = GenerativeAIDecodeController.provide_analysis(llm_model=llm_core, statistics=data_statistics)
            context.update(response=response)
        except Exception as e:
            logger.error(f"Error getting main dashboard context data: {e}")
            return context

        logger.info(f"AI Model: {llm_core.nickname} - Response: {response}")
        return self.render_to_response(context)
