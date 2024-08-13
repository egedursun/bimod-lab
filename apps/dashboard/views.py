"""
This module contains views for managing and displaying dashboard statistics within the Bimod.io platform.

The views include displaying the main dashboard, refreshing statistics, and changing the date range for the statistics displayed. The dashboard provides insights based on data from the user's organizations and LLM models.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from apps._services.llms.llm_decoder import InternalLLMClient
from apps.dashboard.utils import DashboardStatisticsCalculator, prepare_data_for_charts
from apps.llm_core.models import LLMCore
from apps.organization.models import Organization
from web_project import TemplateLayout


MINUTES = 60
HOURS = 60 * MINUTES

DEFAULT_DASHBOARD_DAYS_BACK = 1


class DashboardMainView(TemplateView):
    """
    Displays the main dashboard view for the Bimod.io platform.

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
