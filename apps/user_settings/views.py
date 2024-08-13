"""
This module contains views related to user profile management and settings within the web project.

Views:
- `UserSettingsView`: Renders the user settings page, ensuring the user is authenticated.
- `UserProfileListView`: Displays the user's profile details, including personal information and saved credit cards, allowing updates to the profile and credit card information.
- `UserProfileResetPasswordView`: Handles the process of sending a password reset email to the user.
- `RemoveCardView`: Allows users to remove a saved credit card from their profile.

All views in this module require user authentication, enforced by the `LoginRequiredMixin`.

Note:
- These views rely on forms and utility functions from `apps.user_profile_management` for handling user-related data.
- The views make extensive use of the `TemplateLayout` for initializing and rendering templates.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from web_project import TemplateLayout


class UserSettingsView(TemplateView, LoginRequiredMixin):
    """
    Displays and manages user settings.

    GET:
    - Renders the user settings page.
    - Provides necessary context data initialized by TemplateLayout.
    """
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context
