from django.urls import path

from apps.user_management.views import AddNewUserView, ListUsersView, RemoveUserView, UpdateUserStatusView

app_name = "user_management"


urlpatterns = [
    path('add/', AddNewUserView.as_view(template_name="user_management/add_new_user.html"), name="add"),
    path('list/', ListUsersView.as_view(template_name="user_management/list_users.html"), name="list"),
    path('remove/<int:pk>/', RemoveUserView.as_view(template_name="user_management/confirm_remove_user.html"), name="remove"),
    path('update_user_status/', UpdateUserStatusView.as_view(), name='update_user_status'),
]
