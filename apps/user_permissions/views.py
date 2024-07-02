from django.shortcuts import render
from django.views.generic import TemplateView

from web_project import TemplateLayout


# Create your views here.


class UpdatePermissionsView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context


class ListPermissionsView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context
