from django.urls import path

from apps.user_permissions.views import AddPermissionsView, ListPermissionsView

app_name = "user_permissions"

urlpatterns = [
    path('add/', AddPermissionsView.as_view(template_name="user_permissions/add_permissions.html"),
         name="add_permissions"),
    path('list/', ListPermissionsView.as_view(template_name="user_permissions/list_permissions.html"),
         name="list_permissions"),
]
