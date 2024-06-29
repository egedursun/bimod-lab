from django.urls import path
from .views import (CreateOrganizationView, OrganizationListView, OrganizationUpdateView,
                    OrganizationDeleteView)

app_name = "organization"

urlpatterns = [
    path('create/',
         CreateOrganizationView.as_view(template_name="organization/create_organization.html"),
         name="create"),
    path('list/', OrganizationListView.as_view(template_name="organization/list_organizations.html"),
         name="list"),
    path('update/<int:pk>/', OrganizationUpdateView.as_view(template_name="organization/update_organization.html"),
         name="update"),
    path('delete/<int:pk>/', OrganizationDeleteView.as_view(),
         name="delete"),
]
