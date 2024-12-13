#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-10-05 15:45:58
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 15:45:58
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

from django.contrib.auth.views import (
    LogoutView
)

from .register.views import (
    RegisterView
)

from .login.views import (
    LoginView
)

from .forgot_password.views import (
    ForgetPasswordView
)

from .reset_password.views import (
    ResetPasswordView
)

from .verify_email.views import (
    VerifyEmailTokenView,
    VerifyEmailView,
    SendVerificationView
)

urlpatterns = [
    path(
        "",
        LoginView.as_view(
            template_name="auth/login.html"
        ),
        name="login"
    ),

    path(
        "login/",
        LoginView.as_view(
            template_name="auth/login.html"
        ),
        name="login"
    ),

    path(
        "logout/",
        LogoutView.as_view(

        ),
        name="logout"
    ),

    path(
        "register/",
        RegisterView.as_view(
            template_name="auth/register.html"
        ),
        name="register"
    ),

    path(
        "verify_email/",
        VerifyEmailView.as_view(
            template_name="auth/verify_email.html"
        ),
        name="verify-email-page"
    ),

    path(
        "verify/email/<str:token>/",
        VerifyEmailTokenView.as_view(

        ),
        name="verify-email"
    ),

    path(
        "send_verification/",
        SendVerificationView.as_view(

        ),
        name="send-verification"
    ),

    path(
        "forgot_password/",
        ForgetPasswordView.as_view(
            template_name="auth/forgot_password.html"
        ),
        name="forgot-password"
    ),

    path(
        "reset_password/<str:token>/",
        ResetPasswordView.as_view(
            template_name="auth/reset_password.html"
        ),
        name="reset-password"
    ),
]
