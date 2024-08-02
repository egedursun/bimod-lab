
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

DEFAULT_DASHBOARD_DAYS_BACK = 7


class DashboardMainView(TemplateView):
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
