#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: change_statistics_interval_views.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:35
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: change_statistics_interval_views.py
#  Last Modified: 2024-09-26 19:20:31
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:27:24
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from apps.dashboard.utils import MINUTES, DashboardStatisticsCalculator, prepare_data_for_charts
from apps.llm_core.models import LLMCore
from apps.organization.models import Organization
from web_project import TemplateLayout


class ChangeStatisticsDatetimeIntervalView(LoginRequiredMixin, TemplateView):
    """
    Changes the date range for the displayed dashboard statistics.

    This view allows the user to adjust the date range for the statistics displayed on the dashboard. The data is cached to improve performance, and the user can choose to display data from a specific number of days or all available data.

    Methods:
        dispatch(self, *args, **kwargs): Caches the response for 30 minutes to improve performance.
        get_context_data(self, **kwargs): Prepares the base context for rendering the view.
        get(self, request, *args, **kwargs): Retrieves and processes the statistics for the selected date range, updating the context with the new data.
    """

    @method_decorator(cache_page(30 * MINUTES))  # 30 minutes
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        user = self.request.user
        organizations = Organization.objects.filter(users__in=[user])
        llm_models = LLMCore.objects.filter(organization__in=organizations)
        context["llm_models"] = llm_models
        days = self.kwargs.get("days")

        if days == "0" or days == 0:
            days = 10_000
            context["days"] = "all"
        else:
            context["days"] = days

        # get the statistics for the specified number of days
        dashboard_manager = DashboardStatisticsCalculator(user=self.request.user, last_days=int(days))
        statistics = dashboard_manager.statistics
        last_update_datetime = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        context["last_update_datetime"] = last_update_datetime

        # prepare the data for the chart
        context = prepare_data_for_charts(statistics=statistics, context=context)
        return self.render_to_response(context)
