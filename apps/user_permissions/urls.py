from django.urls import path

from apps.user_permissions.views import UpdatePermissionsView, ListPermissionsView


app_name = "user_permissions"


urlpatterns = [
    path('update/', UpdatePermissionsView.as_view(template_name="user_permissions/update_permissions.html"),
         name="update"),
    path('list/', ListPermissionsView.as_view(template_name="user_permissions/list_permissions.html"),
         name="list"),
]
