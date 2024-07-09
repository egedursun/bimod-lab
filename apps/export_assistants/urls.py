from django.urls import path

from apps.export_assistants.views import ListExportAssistantsView, CreateExportAssistantsView, \
    UpdateExportAssistantsView, DeleteExportAssistantsView, ExportAssistantAPIView, ToggleExportAssistantServiceView

app_name = 'export_assistants'


urlpatterns = [
    path('list/', ListExportAssistantsView.as_view(
        template_name="export_assistants/list_export_assistants.html"
    ), name='list'),
    path('create/', CreateExportAssistantsView.as_view(
        template_name="export_assistants/create_export_assistants.html"
    ), name='create'),
    path('update/<int:pk>/', UpdateExportAssistantsView.as_view(
        template_name="export_assistants/update_export_assistants.html"
    ), name='update'),
    path('delete/<int:pk>/', DeleteExportAssistantsView.as_view(), name='delete'),
    path('exported/<str:endpoint>/', ExportAssistantAPIView.as_view(), name='api'),
    path('toggle_service/<int:pk>/', ToggleExportAssistantServiceView.as_view(), name='toggle_service'),
]
