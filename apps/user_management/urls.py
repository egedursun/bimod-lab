from django.urls import path

from apps.user_management.views import AddNewUserView, ListUsersView, RemoveUserView, UpdateUserStatusView, \
    AddUserToOrganizationView, RemoveUserFromOrganizationView, RemoveUserFromAllOrganizationsView

app_name = "user_management"


urlpatterns = [
    path('add/', AddNewUserView.as_view(template_name="user_management/users/add_new_user.html"), name="add"),
    path('list/', ListUsersView.as_view(template_name="user_management/users/list_users.html"), name="list"),
    path('remove/<int:pk>/', RemoveUserView.as_view(template_name="user_management/users/confirm_remove_user.html"), name="remove"),
    path('update_user_status/', UpdateUserStatusView.as_view(), name='update_user_status'),

    path('add_user_to_organization/', AddUserToOrganizationView.as_view(
        template_name="user_management/connections/add_user_to_organization.html"),
         name='add_user_to_organization'),
    path('remove_user_from_organization/<int:pk>/<int:org_id>/', RemoveUserFromOrganizationView.as_view(
        template_name="user_management/connections/confirm_remove_from_organization.html"
    ), name='remove_user_from_organization'),

    path('remove_user_from_all_organizations/<int:pk>/', RemoveUserFromAllOrganizationsView.as_view(
        template_name="user_management/connections/confirm_remove_from_all_organizations.html"
    ), name='remove_user_from_all_organizations'),
]
