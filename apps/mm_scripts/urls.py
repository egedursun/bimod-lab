from django.urls import path

from apps.mm_scripts.views import CreateCustomScriptView, ListCustomScriptsView, \
    ManageCustomScriptAssistantConnectionsView, DeleteCustomScriptView, ScriptStoreView

app_name = "mm_scripts"

urlpatterns = [
    path("create/", CreateCustomScriptView.as_view(
        template_name="mm_scripts/scripts/create_custom_script.html"
    ), name="create"),
    path("list/", ListCustomScriptsView.as_view(
        template_name="mm_scripts/scripts/list_custom_scripts.html"
    ), name="list"),
    path("delete/<int:pk>/", DeleteCustomScriptView.as_view(
        template_name="mm_scripts/scripts/confirm_delete_custom_script.html"
    ), name="delete"),

    path("connect/", ManageCustomScriptAssistantConnectionsView.as_view(
        template_name="mm_scripts/connections/manage_script_connections.html"
    ), name="connect"),

    path("store/", ScriptStoreView.as_view(
        template_name="mm_scripts/store/script_store.html"
    ), name="store"),
]
