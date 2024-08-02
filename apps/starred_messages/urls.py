from django.urls import path

from apps.starred_messages.views import ListStarredMessageView, DeleteStarredMessageView

app_name = "starred_messages"

urlpatterns = [
    path("list/", ListStarredMessageView.as_view(
        template_name="starred_messages/list_starred_messages.html"
    ), name="list"),
    path("delete/<int:pk>/", DeleteStarredMessageView.as_view(), name="delete"),
]
