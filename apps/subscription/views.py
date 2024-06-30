from audioop import reverse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DeleteView

from apps.organization.models import Organization
from apps.subscription.forms import SubscriptionForm
from web_project import TemplateLayout


# Create your views here.

class CreateSubscriptionView(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = self.request.user
        organizations = Organization.objects.filter(user=user)
        context['organizations'] = organizations
        context['form'] = SubscriptionForm()
        return context

    def post(self, request, *args, **kwargs):
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.user = request.user
            subscription.save()
            return redirect(reverse('subscription:list'))
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)


class ListSubscriptionView(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context


class UpdateSubscriptionView(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context


class DeleteSubscriptionView(DeleteView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context
