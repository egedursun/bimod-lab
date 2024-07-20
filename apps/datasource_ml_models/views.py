from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView

from web_project import TemplateLayout


# Create your views here.

class DataSourceMLModelConnectionCreateView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def post(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))


class DataSourceMLModelConnectionUpdateView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def post(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))


class DataSourceMLModelConnectionListView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context


class DataSourceMLModelConnectionDeleteView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def post(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))


######################################################################################################################


class DataSourceMLModelItemCreateView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def post(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))


class DataSourceMLModelItemUpdateView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def post(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))


class DataSourceMLModelItemListView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context


class DataSourceMLModelItemDeleteView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def post(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))
