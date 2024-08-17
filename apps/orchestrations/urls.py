from django.urls import path

from apps.orchestrations.views import CreateOrchestrationView, OrchestrationUpdateView, OrchestrationQueryView, \
    OrchestrationListView, OrchestrationDeleteView

app_name = "orchestrations"


urlpatterns = [
    path("create/", CreateOrchestrationView.as_view(
        template_name="orchestrations/create_orchestration.html"), name="create"),
    path("list/", OrchestrationListView.as_view(
        template_name="orchestrations/list_orchestrations.html"), name="list"),
    path("update/<int:pk>/", OrchestrationUpdateView.as_view(
        template_name="orchestrations/update_orchestration.html"), name="update"),
    path("delete/<int:pk>/", OrchestrationDeleteView.as_view(
        template_name="orchestrations/delete_orchestration.html"), name="delete"),
    path("query/<int:pk>/", OrchestrationQueryView.as_view(
        template_name="orchestrations/query_orchestration.html"), name="query"),
]
