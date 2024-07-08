from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView

from web_project import TemplateLayout


# Create your views here.


class ListStarredMessageView(TemplateView, LoginRequiredMixin):

    def get_context_data(self, **kwargs):
        # TODO: implement the view
        pass
