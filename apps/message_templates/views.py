from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, DeleteView, UpdateView

from apps.message_templates.forms import MessageTemplateForm
from apps.message_templates.models import MessageTemplate
from apps.user_permissions.models import UserPermission, PermissionNames
from web_project import TemplateLayout


# Create your views here.


class CreateMessageTemplateView(TemplateView, LoginRequiredMixin):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['organizations'] = self.request.user.organizations.all()
        return context

    def post(self, request, *args, **kwargs):
        form = MessageTemplateForm(request.POST)
        context_user = request.user

        ##############################
        # PERMISSION CHECK FOR - TEMPLATE MESSAGE/CREATE
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.ADD_TEMPLATE_MESSAGES not in user_permissions:
            messages.error(request, "You do not have permission to create message templates.")
            return redirect('message_templates:list')
        ##############################

        if form.is_valid():
            message_template = form.save(commit=False)
            message_template.user = request.user
            message_template.save()
            messages.success(request, "Message Template created successfully!")
            return redirect("message_templates:list")
        else:
            messages.error(request, "Please correct the errors below.")
            return self.render_to_response(self.get_context_data(form=form, error_messages=form.errors))


class ListMessageTemplateView(TemplateView, LoginRequiredMixin):
    model = MessageTemplate

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        organizations = self.request.user.organizations.all()
        context['message_templates'] = MessageTemplate.objects.filter(user=self.request.user)
        return context


class UpdateMessageTemplateView(TemplateView, LoginRequiredMixin):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        organizations = self.request.user.organizations.all()
        message_template = get_object_or_404(MessageTemplate, pk=self.kwargs['pk'])
        context['form'] = MessageTemplateForm(instance=message_template)
        context['message_template'] = message_template
        context['organizations'] = organizations
        return context

    def post(self, request, *args, **kwargs):
        message_template = get_object_or_404(MessageTemplate, pk=self.kwargs['pk'])
        form = MessageTemplateForm(request.POST, instance=message_template)
        if form.is_valid():
            form.save()
            return redirect('message_templates:list')
        return render(request, self.template_name, {'form': form, 'message_template': message_template})


class DeleteMessageTemplateView(DeleteView, LoginRequiredMixin):
    model = MessageTemplate
    success_url = 'message_templates:list'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        context_user = request.user
        starred_message = get_object_or_404(MessageTemplate, id=self.kwargs['pk'])

        ##############################
        # PERMISSION CHECK FOR - TEMPLATE MESSAGE/DELETION
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.REMOVE_TEMPLATE_MESSAGES not in user_permissions:
            messages.error(request, "You do not have permission to delete message templates.")
            return redirect('message_templates:list')
        ##############################

        starred_message.delete()
        success_message = "Message template deleted successfully."

        messages.success(request, success_message)
        return redirect(self.success_url)



