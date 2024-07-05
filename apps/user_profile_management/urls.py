from django.urls import path

from apps.user_profile_management.views import UserProfileListView, RemoveCardView

app_name = "user_profile_management"


urlpatterns = [
    path("profile/", UserProfileListView.as_view(
        template_name="user_profile_management/user_profile_list.html"
    ), name="list"),
    path('billing/update/', UserProfileListView.as_view(
        template_name="user_profile_management/billing.html"
    ), name='billing'),
    path('remove_card/<int:card_id>/', RemoveCardView.as_view(), name='remove_card'),
]
