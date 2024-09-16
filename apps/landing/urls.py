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
