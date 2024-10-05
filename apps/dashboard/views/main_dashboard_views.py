#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
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
#   For permission inquiries, please contact: admin@br6.in.
#

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from apps._services.llms.llm_decoder import InternalLLMClient
from apps.dashboard.utils import DEFAULT_DASHBOARD_DAYS_BACK, MINUTES, prepare_data_for_charts
from apps.dashboard.utils.class_utils import DashboardStatisticsCalculator
from apps.llm_core.models import LLMCore
from apps.organization.models import Organization
from web_project import TemplateLayout


class DashboardMainView(LoginRequiredMixin, TemplateView):
    """
    Displays the main dashboard view for the br6.in platform.

    This view provides an overview of the user's organizations, LLM models, and relevant statistics. The data is cached to improve performance, and the user can request an analysis based on the selected LLM model and statistics.

    Attributes:
        template_name (str): The template used to render the dashboard view.

    Methods:
        dispatch(self, *args, **kwargs): Caches the response for 30 minutes to improve performance.
        get_context_data(self, **kwargs): Prepares the context for rendering, including organizations, LLM models, and dashboard statistics.
        post(self, request, *args, **kwargs): Handles form submissions for requesting an analysis, updating the context with the response from the LLM client.
    """

    template_name = "dashboard/dashboard_main.html"

    @method_decorator(cache_page(30 * MINUTES))  # 30 minutes
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = self.request.user
        organizations = Organization.objects.filter(users__in=[user])
        dashboard_manager = DashboardStatisticsCalculator(user=user)
        statistics = dashboard_manager.statistics
        days = DEFAULT_DASHBOARD_DAYS_BACK
        context["days"] = days

        # llm models
        llm_models = LLMCore.objects.filter(organization__in=organizations)
        context["llm_models"] = llm_models
        last_update_datetime = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        context["last_update_datetime"] = last_update_datetime

        context = prepare_data_for_charts(statistics=statistics, context=context)
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        context_user = request.user
        llm_model = request.POST.get("llm_model")
        llm = LLMCore.objects.get(id=llm_model)
        dashboard_manager = DashboardStatisticsCalculator(user=context_user)
        statistics = dashboard_manager.statistics
        response = InternalLLMClient.provide_analysis(llm_model=llm, statistics=statistics)
        context.update(response=response)
        return self.render_to_response(context)
