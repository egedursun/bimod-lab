#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:33
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.urls import path
from .views import AuthView


urlpatterns = [
    path(
        "auth/login/basic/",
        AuthView.as_view(template_name="auth_login_basic.html"),
        name="auth-login-basic",
    ),
    path(
        "auth/login/cover/",
        AuthView.as_view(template_name="auth_login_cover.html"),
        name="auth-login-cover",
    ),
    path(
        "auth/register/basic/",
        AuthView.as_view(template_name="auth_register_basic.html"),
        name="auth-register-basic",
    ),
    path(
        "auth/register/cover/",
        AuthView.as_view(template_name="auth_register_cover.html"),
        name="auth-register-cover",
    ),
    path(
        "auth/register/multisteps/",
        AuthView.as_view(template_name="auth_register_multisteps.html"),
        name="auth-register-multisteps",
    ),
    path(
        "auth/verify_email/basic/",
        AuthView.as_view(template_name="auth_verify_email_basic.html"),
        name="auth-verify-email-basic",
    ),
    path(
        "auth/verify_email/cover/",
        AuthView.as_view(template_name="auth_verify_email_cover.html"),
        name="auth-verify-email-cover",
    ),
    path(
        "auth/reset_password/basic/",
        AuthView.as_view(template_name="auth_reset_password_basic.html"),
        name="auth-reset-password-basic",
    ),
    path(
        "auth/reset_password/cover/",
        AuthView.as_view(template_name="auth_reset_password_cover.html"),
        name="auth-reset-password-cover",
    ),
    path(
        "auth/forgot_password/basic/",
        AuthView.as_view(template_name="auth_forgot_password_basic.html"),
        name="auth-forgot-password-basic",
    ),
    path(
        "auth/forgot_password/cover/",
        AuthView.as_view(template_name="auth_forgot_password_cover.html"),
        name="auth-forgot-password-cover",
    ),
    path(
        "auth/two_steps/basic/",
        AuthView.as_view(template_name="auth_two_steps_basic.html"),
        name="auth-two-steps-basic",
    ),
    path(
        "auth/two_steps/cover/",
        AuthView.as_view(template_name="auth_two_steps_cover.html"),
        name="auth-two-steps-cover",
    ),
]
