from django.urls import path

from apps.export_leanmods.views import ListExportLeanmodAssistantsView, CreateExportLeanmodAssistantsView, \
    UpdateExportLeanmodAssistantsView, DeleteExportLeanmodAssistantsView, ExportLeanmodAssistantAPIView, \
    ToggleExportLeanmodAssistantServiceView

app_name = 'export_leanmods'

urlpatterns = [
    path('list/', ListExportLeanmodAssistantsView.as_view(
        template_name="export_leanmods/list_export_leanmods.html"
    ), name='list'),
    path('create/', CreateExportLeanmodAssistantsView.as_view(
        template_name="export_leanmods/create_export_leanmods.html"
    ), name='create'),
    path('update/<int:pk>/', UpdateExportLeanmodAssistantsView.as_view(
        template_name="export_leanmods/update_export_leanmods.html"
    ), name='update'),
    path('delete/<int:pk>/', DeleteExportLeanmodAssistantsView.as_view(), name='delete'),
    path('exported/<str:endpoint>/', ExportLeanmodAssistantAPIView.as_view(), name='api'),
    path('toggle_service/<int:pk>/', ToggleExportLeanmodAssistantServiceView.as_view(), name='toggle_service'),
]
