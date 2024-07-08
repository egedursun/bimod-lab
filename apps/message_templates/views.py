from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView, DeleteView


# Create your views here.


# TODO: implement the views

class CreateMessageTemplateView(TemplateView, LoginRequiredMixin):

    def get_context_data(self, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass


class ListMessageTemplateView(TemplateView, LoginRequiredMixin):

    def get_context_data(self, **kwargs):
        pass


class UpdateMessageTemplateView(TemplateView, LoginRequiredMixin):

    def get_context_data(self, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass


class DeleteMessageTemplateView(DeleteView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass



