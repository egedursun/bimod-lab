from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from web_project import TemplateLayout


class UserSettingsView(TemplateView, LoginRequiredMixin):
    """
    Displays and manages user settings.

    GET:
    - Renders the user settings page.
    - Provides necessary context data initialized by TemplateLayout.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context
