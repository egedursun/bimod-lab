from django.urls import path

from apps.user_profile_management.views import UserProfileListView, RemoveCardView, UserProfileResetPasswordView

app_name = "user_profile_management"

urlpatterns = [
    path("profile/", UserProfileListView.as_view(
        template_name="user_profile_management/profiles/user_profile_list.html"
    ), name="list"),
    path("reset_password/<int:pk>", UserProfileResetPasswordView.as_view(
        template_name="user_profile_management/profiles/user_profile_list.html"
    ), name="reset_password"),

    path('billing/update/', UserProfileListView.as_view(
        template_name="user_profile_management/billings/billing.html"
    ), name='billing'),
    path('remove_card/<int:card_id>/', RemoveCardView.as_view(), name='remove_card'),
]
