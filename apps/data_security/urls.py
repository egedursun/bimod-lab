from django.urls import path

from apps.data_security.views import (CreateNERIntegrationView, UpdateNERIntegrationView, DeleteNERIntegrationView,
                                      ListNERIntegrationsView)

app_name = "data_security"

urlpatterns = [
    path("ner/create/", CreateNERIntegrationView.as_view(
        template_name="data_security/ner/create_ner_integration.html"
    ), name="create_ner_integration"),
    path("ner/list/", ListNERIntegrationsView.as_view(
        template_name="data_security/ner/list_ner_integrations.html"
    ), name="list_ner_integrations"),
    path("ner/update/<int:pk>/", UpdateNERIntegrationView.as_view(
        template_name="data_security/ner/update_ner_integration.html"
    ), name="update_ner_integration"),
    path("ner/delete/<int:pk>/", DeleteNERIntegrationView.as_view(
        template_name="data_security/ner/confirm_delete_ner_integration.html"
    ), name="delete_ner_integration"),
]
