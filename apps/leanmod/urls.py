from django.urls import path

from apps.leanmod.views import CreateLeanAssistantView, UpdateLeanAssistantView, DeleteLeanAssistantView, \
    ListLeanAssistantsView, CreateExpertNetworkView, UpdateExpertNetworkView, DeleteExpertNetworkView, \
    ListExpertNetworksView

app_name = 'leanmod'


urlpatterns = [
    path('create/', CreateLeanAssistantView.as_view(
        template_name="leanmod/lean_assistant/create_lean_assistant.html"
    ), name='create'),
    path('update/<int:pk>/', UpdateLeanAssistantView.as_view(
        template_name="leanmod/lean_assistant/update_lean_assistant.html"
    ), name='update'),
    path('delete/<int:pk>/', DeleteLeanAssistantView.as_view(
        template_name="leanmod/lean_assistant/confirm_delete_lean_assistant.html"
    ), name='delete'),
    path('list/', ListLeanAssistantsView.as_view(
        template_name="leanmod/lean_assistant/list_lean_assistants.html"
    ), name='list'),
    #####
    path('create_expert_network/', CreateExpertNetworkView.as_view(
        template_name="leanmod/expert_network/create_expert_network.html"
    ), name='create_expert_network'),
    path('update_expert_network/<int:pk>/', UpdateExpertNetworkView.as_view(
        template_name="leanmod/expert_network/update_expert_network.html"
    ), name='update_expert_network'),
    path('delete_expert_network/<int:pk>/', DeleteExpertNetworkView.as_view(
        template_name="leanmod/expert_network/confirm_delete_expert_network.html"
    ), name='delete_expert_network'),
    path('list_expert_network/', ListExpertNetworksView.as_view(
        template_name="leanmod/expert_network/list_expert_networks.html"
    ), name='list_expert_networks'),
]
