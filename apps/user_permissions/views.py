from django.shortcuts import render
from django.views.generic import TemplateView

from apps.user_permissions.models import PermissionNames
from web_project import TemplateLayout


# Create your views here.


class UpdatePermissionsView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - PERMISSIONS/UPDATE
        ##############################
        user_permissions = context_user.permissions.all()
        if PermissionNames.MODIFY_USER_PERMISSIONS not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {
                "Permission Error": "You do not have permission to update or modify user permissions."}
            return self.render_to_response(context)
        ##############################

        return render(request, self.template_name, context)


class ListPermissionsView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - PERMISSIONS/LIST
        ##############################
        # For now, every user is able to see the list of permissions of the system
        ##############################

        return context
