from django.urls import path

from apps.assistants.views import CreateAssistantView, ListAssistantView, UpdateAssistantView, DeleteAssistantView


app_name = "assistants"


urlpatterns = [
    path("create/", CreateAssistantView.as_view(template_name="assistants/create_assistant.html"),
         name="create"),
    path("list/", ListAssistantView.as_view(template_name
    ="assistants/list_assistants.html"), name="list"),
    path("update/<int:pk>/", UpdateAssistantView.as_view(template_name="assistants/update_assistant.html"),
         name="update"),
    path("delete/<int:pk>/", DeleteAssistantView.as_view(template_name="assistants/confirm_delete_assistant.html"),
         name="delete"),
]
