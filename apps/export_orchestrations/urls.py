from django.urls import path

from .views import (ListExportOrchestrationsView, CreateExportOrchestrationView, UpdateExportOrchestrationView,
                    DeleteExportOrchestrationView, ExportOrchestrationAPIView, ToggleExportOrchestrationServiceView)

app_name = 'export_orchestrations'

urlpatterns = [
    path('list/', ListExportOrchestrationsView.as_view(
        template_name="export_orchestrations/list_export_orchestrations.html"
    ), name='list'),
    path('create/', CreateExportOrchestrationView.as_view(
        template_name="export_orchestrations/create_export_orchestrations.html"
    ), name='create'),
    path('update/<int:pk>/', UpdateExportOrchestrationView.as_view(
        template_name="export_orchestrations/update_export_orchestrations.html"
    ), name='update'),
    path('delete/<int:pk>/', DeleteExportOrchestrationView.as_view(), name='delete'),
    path('exported/<str:endpoint>/', ExportOrchestrationAPIView.as_view(), name='api'),
    path('toggle_service/<int:pk>/', ToggleExportOrchestrationServiceView.as_view(), name='toggle_service'),
]
