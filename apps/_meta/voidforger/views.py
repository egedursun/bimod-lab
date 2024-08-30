import asyncio

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from config.consumers import VoidForgeOperationLogsConsumer
from web_project import TemplateLayout, TemplateHelper


class VoidForgerDashboardView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context.update(
            {
                "layout_path": TemplateHelper.set_layout("layout_blank.html", context),
            }
        )

        return context


