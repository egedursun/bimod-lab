#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: urls.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:30
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: urls.py
#  Last Modified: 2024-09-16 18:36:13
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:54:41
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.urls import path

from apps.landing.views import (LandingPageView, ContactFormSubmitView, DocumentationView, FAQView,
                                NotAccreditedAdminView, EndeavoursView, IntegrationToOrganizationsView)

app_name = "landing"

urlpatterns = [
    path("", LandingPageView.as_view(template_name="landing/index.html"), name="index"),
    path('contact-form-submit/', ContactFormSubmitView.as_view(template_name="landing/contact_form_submitted.html"),
         name='contact_form_submit'),
    path('docs/', DocumentationView.as_view(template_name="landing/documentation.html"), name="documentation"),
    path('faq/', FAQView.as_view(template_name="landing/faq.html"), name="faq"),
    path('not_accredited/', NotAccreditedAdminView.as_view(template_name="landing/not_accredited_admin.html"),
         name='not_accredited'),
    path('bimod_endeavours/', EndeavoursView.as_view(template_name="landing/bimod_endeavours.html"),
         name='bimod_endeavours'),
    path('integration_to_organizations/',
         IntegrationToOrganizationsView.as_view(template_name="landing/integration_to_organizations.html"),
         name='integration_to_organizations'),
]
