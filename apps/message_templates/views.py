"""
This module provides views for managing message templates within the Bimod.io platform.

The views allow authenticated users to create, list, update, and delete their message templates. Permissions are checked to ensure that users have the appropriate rights to perform these actions.
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, DeleteView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.message_templates.forms import MessageTemplateForm
from apps.message_templates.models import MessageTemplate
from apps.user_permissions.models import UserPermission, PermissionNames
from web_project import TemplateLayout


class CreateMessageTemplateView(TemplateView, LoginRequiredMixin):
    """
    Handles the creation of new message templates.

    This view allows users to create message templates that they can use in their interactions. The view checks user permissions before allowing the creation of a new template.

    Methods:
        get_context_data(self, **kwargs): Prepares the context with the user's organizations.
        post(self, request, *args, **kwargs): Processes the form submission to create a new message template and associates it with the user.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['organizations'] = self.request.user.organizations.all()
        return context

    def post(self, request, *args, **kwargs):
        form = MessageTemplateForm(request.POST)

        ##############################
        # PERMISSION CHECK FOR - ADD_TEMPLATE_MESSAGES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_TEMPLATE_MESSAGES):
            messages.error(self.request, "You do not have permission to add template messages.")
            return redirect('message_templates:list')
        ##############################

        if form.is_valid():
            message_template = form.save(commit=False)
            message_template.user = request.user
            message_template.save()
            messages.success(request, "Message Template created successfully!")
            print('[CreateMessageTemplateView.post] Message Template created successfully.')
            return redirect("message_templates:list")
        else:
            messages.error(request, "Please correct the errors below.")
            return self.render_to_response(self.get_context_data(form=form, error_messages=form.errors))


class ListMessageTemplateView(TemplateView, LoginRequiredMixin):
    """
    Displays a list of message templates created by the user.

    This view retrieves and displays all message templates that the current user has created.

    Methods:
        get_context_data(self, **kwargs): Retrieves the user's message templates and adds them to the context.
    """

    model = MessageTemplate

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_TEMPLATE_MESSAGES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_TEMPLATE_MESSAGES):
            messages.error(self.request, "You do not have permission to list template messages.")
            return context
        ##############################

        context['message_templates'] = MessageTemplate.objects.filter(user=self.request.user)
        return context


class UpdateMessageTemplateView(TemplateView, LoginRequiredMixin):
    """
    Handles the updating of an existing message template.

    This view allows users to update the content of their existing message templates. It ensures that the user is authorized to make changes before saving them.

    Methods:
        get_context_data(self, **kwargs): Prepares the context with the user's organizations and the message template to be updated.
        post(self, request, *args, **kwargs): Processes the form submission to update the message template.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        organizations = self.request.user.organizations.all()
        message_template = get_object_or_404(MessageTemplate, pk=self.kwargs['pk'])
        context['form'] = MessageTemplateForm(instance=message_template)
        context['message_template'] = message_template
        context['organizations'] = organizations
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - UPDATE_TEMPLATE_MESSAGES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_TEMPLATE_MESSAGES):
            messages.error(self.request, "You do not have permission to update template messages.")
            return redirect('message_templates:list')
        ##############################

        message_template = get_object_or_404(MessageTemplate, pk=self.kwargs['pk'])
        form = MessageTemplateForm(request.POST, instance=message_template)
        if form.is_valid():
            form.save()
            return redirect('message_templates:list')
        return render(request, self.template_name, {'form': form, 'message_template': message_template})


class DeleteMessageTemplateView(DeleteView, LoginRequiredMixin):
    """
    Handles the deletion of a message template.

    This view allows users to delete a specific message template, provided they have the necessary permissions.

    Methods:
        get_context_data(self, **kwargs): Prepares the context for the deletion confirmation page.
        post(self, request, *args, **kwargs): Processes the deletion of the specified message template.
    """

    model = MessageTemplate
    success_url = 'message_templates:list'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - REMOVE_TEMPLATE_MESSAGES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.REMOVE_TEMPLATE_MESSAGES):
            messages.error(self.request, "You do not have permission to delete template messages.")
            return redirect('message_templates:list')
        ##############################

        starred_message = get_object_or_404(MessageTemplate, id=self.kwargs['pk'])
        starred_message.delete()
        success_message = "Message template deleted successfully."
        print('[DeleteMessageTemplateView.post] Message template deleted successfully.')
        messages.success(request, success_message)
        return redirect(self.success_url)
