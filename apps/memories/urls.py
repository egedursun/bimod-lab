from django.urls import path

from apps.memories.views import ListAssistantMemoryView, CreateAssistantMemoryView, DeleteAssistantMemoryView

app_name = "memories"

urlpatterns = [
    path("list/", ListAssistantMemoryView.as_view(
        template_name="memories/list_memories.html"
    ), name="list"),
    path("create/", CreateAssistantMemoryView.as_view(
        template_name="memories/create_memory.html"
    ), name="create"),
    path("delete/<int:pk>/", DeleteAssistantMemoryView.as_view(),
         name="delete"),
]
