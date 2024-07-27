from django.urls import path

from apps.mm_apis.views import CreateCustomAPIView, ListCustomAPIsView, DeleteCustomAPIView, APIStoreView, \
    ManageCustomAPIAssistantConnectionsView

app_name = "mm_apis"


urlpatterns = [
    path("create/", CreateCustomAPIView.as_view(
        template_name="mm_apis/create_custom_api.html"
    ), name="create"),
    path("list/", ListCustomAPIsView.as_view(
        template_name="mm_apis/list_custom_apis.html"
    ), name="list"),
    path("connect/", ManageCustomAPIAssistantConnectionsView.as_view(
        template_name="mm_apis/manage_api_connections.html"
    ), name="connect"),
    path("delete/<int:pk>/", DeleteCustomAPIView.as_view(
        template_name="mm_apis/confirm_delete_custom_api.html"
    ), name="delete"),

    path("store/", APIStoreView.as_view(
        template_name="mm_apis/api_store.html"
    ), name="store"),
]
