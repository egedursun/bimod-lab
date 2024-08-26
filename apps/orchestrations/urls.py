from django.urls import path

from apps.orchestrations.views import (CreateOrchestrationView, OrchestrationUpdateView, OrchestrationQueryListView, \
                                       OrchestrationListView, OrchestrationDeleteView,
                                       OrchestrationQueryDeleteView,
                                       OrchestrationQueryDetailView, OrchestrationQueryRerunView)

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
    ##############################
    path("query/<int:pk>/list/", OrchestrationQueryListView.as_view(
        template_name="orchestrations/query_list_orchestration.html"), name="query_list"),
    path("query/<int:pk>/delete/<int:query_id>/", OrchestrationQueryDeleteView.as_view(
        template_name="orchestrations/query_confirm_delete_orchestration.html"), name="query_delete"),
    path("query/<int:pk>/detail/<int:query_id>/", OrchestrationQueryDetailView.as_view(
        template_name="orchestrations/query_detail_orchestration.html"), name="query_detail"),
    path("query/<int:pk>/rerun/<int:query_id>/", OrchestrationQueryRerunView.as_view(
        template_name="orchestrations/query_detail_orchestration.html"), name="query_rerun"),
]
