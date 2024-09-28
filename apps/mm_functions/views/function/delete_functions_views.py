from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.mm_functions.models import CustomFunction
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class DeleteCustomFunctionView(LoginRequiredMixin, TemplateView):
    """
    Handles the deletion of custom functions.

    This view allows users to delete specific custom functions, provided they have the necessary permissions.

    Methods:
        get_context_data(self, **kwargs): Prepares the context for the deletion confirmation page.
        post(self, request, *args, **kwargs): Processes the deletion of the specified custom function.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        custom_function_id = self.kwargs.get('pk')
        custom_function = CustomFunction.objects.get(id=custom_function_id)
        context['custom_function'] = custom_function
        return context

    def post(self, request, *args, **kwargs):
        custom_function_id = self.kwargs.get('pk')

        ##############################
        # PERMISSION CHECK FOR - DELETE_FUNCTIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_FUNCTIONS):
            messages.error(self.request, "You do not have permission to delete custom functions.")
            return redirect('mm_functions:list')
        ##############################

        custom_function = CustomFunction.objects.get(id=custom_function_id)
        custom_function.delete()
        messages.success(request, "Custom Function deleted successfully.")
        print('[DeleteCustomFunctionView.post] Custom Function deleted successfully.')
        return redirect('mm_functions:list')
