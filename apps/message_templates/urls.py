from django.urls import path

from apps.message_templates.views import ListMessageTemplateView, CreateMessageTemplateView, UpdateMessageTemplateView, \
    DeleteMessageTemplateView

app_name = "message_templates"


# TODO: implement
urlpatterns = [
    path("list/", ListMessageTemplateView.as_view(), name="list"),
    path("create/", CreateMessageTemplateView.as_view(), name="create"),
    path("<int:pk>/update/", UpdateMessageTemplateView.as_view(), name="update"),
    path("<int:pk>/delete/", DeleteMessageTemplateView.as_view(), name="delete"),
]
