from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import TemplateView

from apps.dashboard.utils import DashboardStatisticsCalculator, prepare_data_for_charts
from apps.llm_core.models import LLMCore
from apps.organization.models import Organization
from web_project import TemplateLayout


class RefreshStatisticsView(LoginRequiredMixin, TemplateView):
    """
    Refreshes and displays the latest dashboard statistics for the Bimod.io platform.

    This view retrieves the latest statistics for the user's organizations and LLM models, based on the specified date range. It is designed to be accessed when the user wants to refresh the displayed statistics without changing the overall dashboard view.

    Methods:
        get_context_data(self, **kwargs): Prepares the base context for rendering the view.
        get(self, request, *args, **kwargs): Retrieves and processes the latest statistics, updating the context with the new data.
    """

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
        if days == "all":
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
