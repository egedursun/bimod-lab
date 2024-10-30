#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-10-05 02:13:34
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

from apps.landing.views import (LandingView_Index, LandingView_ContactFormSubmit, LandingView_FAQ,
                                LandingView_AdminNotAccredited, LandingView_Endeavours,
                                LandingView_IntegrationToOrganizations, LandingView_ElectronCopilotReleases)

app_name = "landing"

urlpatterns = [
    path("", LandingView_Index.as_view(template_name="landing/index.html"), name="index"),
    path('contact-form-submit/', LandingView_ContactFormSubmit.as_view(template_name="landing/contact_form_submitted.html"),
         name='contact_form_submit'),
    path('faq/', LandingView_FAQ.as_view(template_name="landing/faq.html"), name="faq"),
    path('not_accredited/', LandingView_AdminNotAccredited.as_view(template_name="landing/not_accredited_admin.html"),
         name='not_accredited'),
    path('bimod_endeavours/', LandingView_Endeavours.as_view(template_name="landing/bimod_endeavours.html"),
         name='bimod_endeavours'),
    path('integration_to_organizations/',
         LandingView_IntegrationToOrganizations.as_view(template_name="landing/integration_to_organizations.html"),
         name='integration_to_organizations'),
    path('electron_copilot_releases/',
            LandingView_ElectronCopilotReleases.as_view(template_name="landing/electron_copilot_releases.html"),
            name='electron_copilot_releases'),
]
