#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: refresh_dashboard_views.py
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
from django.views.generic import TemplateView

from apps.dashboard.utils import TransactionStatisticsManager, build_statistics_for_graph
from apps.llm_core.models import LLMCore
from apps.organization.models import Organization
from web_project import TemplateLayout


class DashboardView_Refresh(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        user = self.request.user
        orgs = Organization.objects.filter(users__in=[user])
        ai_models = LLMCore.objects.filter(organization__in=orgs)
        context["llm_models"] = ai_models
        last_n_days = self.kwargs.get("days")
        if last_n_days == "all":
            last_n_days = 10_000
            context["days"] = "all"
        else:
            context["days"] = last_n_days

        manager = TransactionStatisticsManager(user=self.request.user, last_days=int(last_n_days))
        data_statistics = manager.statistics
        last_update_datetime = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        context["last_update_datetime"] = last_update_datetime
        context = build_statistics_for_graph(statistics=data_statistics, context=context)
        return self.render_to_response(context)
