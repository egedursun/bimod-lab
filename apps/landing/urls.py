from django.urls import path

from apps.landing.views import LandingPageView, ContactFormSubmitView, DocumentationView, FAQView

app_name = "landing"


urlpatterns = [
    path("", LandingPageView.as_view(template_name="landing/index.html"), name="index"),
    path('contact-form-submit/', ContactFormSubmitView.as_view(
        template_name="landing/contact_form_submitted.html"
    ), name='contact_form_submit'),
    path('docs/', DocumentationView.as_view(
        template_name="landing/documentation.html"
    ), name="documentation"),
    path('faq/', FAQView.as_view(
        template_name="landing/faq.html"
    ), name="faq"),
]
