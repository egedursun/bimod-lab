from django.urls import path

from apps.mm_functions.views import (CreateCustomFunctionView, ListCustomFunctionsView,
                                     ManageCustomFunctionAssistantConnectionsView, DeleteCustomFunctionView,
                                     FunctionStoreView)

app_name = "mm_functions"

urlpatterns = [
    path("create/", CreateCustomFunctionView.as_view(
        template_name="mm_functions/functions/create_custom_function.html"
    ), name="create"),
    path("list/", ListCustomFunctionsView.as_view(
        template_name="mm_functions/functions/list_custom_functions.html"
    ), name="list"),
    path("delete/<int:pk>/", DeleteCustomFunctionView.as_view(
        template_name="mm_functions/functions/confirm_delete_custom_function.html"
    ), name="delete"),

    path("connect/", ManageCustomFunctionAssistantConnectionsView.as_view(
        template_name="mm_functions/connections/manage_assistant_connections.html"
    ), name="connect"),

    path("store/", FunctionStoreView.as_view(
        template_name="mm_functions/store/function_store.html"
    ), name="store"),
]
