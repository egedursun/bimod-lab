from django.views.generic import TemplateView

from auth.countries import COUNTRIES
from web_project import TemplateLayout
from web_project.template_helpers.theme import TemplateHelper

"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to auth/urls.py file for more pages.
"""


class AuthView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        # Update the context
        context.update(
            {
                "layout_path": TemplateHelper.set_layout("layout_blank.html", context), "countries": COUNTRIES,
            }
        )
        return context
