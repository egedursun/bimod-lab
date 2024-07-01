from django.urls import path

from apps.user_management.views import CreateUserView, ListUsersView, UpdateUserView, DeleteUserView

app_name = "user_management"


urlpatterns = [
    path('create/', CreateUserView.as_view(template_name="user_management/create_user.html"), name="create"),
    path('list/', ListUsersView.as_view(template_name="user_management/list_users.html"), name="list"),
    path('update/<int:pk>/', UpdateUserView.as_view(template_name="user_management/update_user.html"), name="update"),
    path('delete/<int:pk>/', DeleteUserView.as_view(template_name="user_management/confirm_delete_user.html"), name="delete"),
]
