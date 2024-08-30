from django.urls import path

from .views import (FineTunedModelConnectionRemoveView,
                    FineTunedModelConnectionAddView, FineTunedModelConnectionsListView)

app_name = 'finetuning'


urlpatterns = [
    ############################
    path('list/', FineTunedModelConnectionsListView.as_view(
        template_name='finetuning/list_finetuned_connections.html'
    ), name='list'),
    path('add/', FineTunedModelConnectionAddView.as_view(
        template_name='finetuning/list_finetuned_connections.html'), name='add'),
    path('remove/<int:pk>/', FineTunedModelConnectionRemoveView.as_view(
        template_name='finetuning/list_finetuned_connections.html'
    ), name='remove'),
    ############################
]
