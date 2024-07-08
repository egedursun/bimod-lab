"""
URL configuration for web_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from config import settings
from web_project.views import SystemView


urlpatterns = [
    path("", include("apps.landing.urls", namespace="landing")),
    path("admin/", admin.site.urls),
    path("app/", include("auth.urls")),
    path("app/user_profile_management/", include("apps.user_profile_management.urls",
                                                 namespace="user_profile_management")),
    path("app/user_settings/", include("apps.user_settings.urls", namespace="user_settings")),
    path("app/dashboard/", include("apps.dashboard.urls", namespace="dashboard")),
    path("app/organization/", include("apps.organization.urls", namespace="organization")),
    path("app/llm_core/", include("apps.llm_core.urls", namespace="llm_core")),
    path("app/llm_transaction/", include("apps.llm_transaction.urls", namespace="llm_transaction")),
    path("app/subscription/", include("apps.subscription.urls", namespace="subscription")),
    path("app/user_management/", include("apps.user_management.urls", namespace="user_management")),
    path("app/user_permissions/", include("apps.user_permissions.urls", namespace="user_permissions")),
    path("app/assistants/", include("apps.assistants.urls", namespace="assistants")),
    path("app/multimodal_chat/", include("apps.multimodal_chat.urls", namespace="multimodal_chat")),
    path("app/memories/", include("apps.memories.urls", namespace="memories")),
    path("app/starred_messages/", include("apps.starred_messages.urls", namespace="starred_messages")),
    path("app/message_templates/", include("apps.message_templates.urls", namespace="message_templates")),
    path("app/export_assistants/", include("apps.export_assistants.urls", namespace="export_assistants")),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = SystemView.as_view(template_name="pages_misc_error.html", status=404)
handler403 = SystemView.as_view(template_name="pages_misc_not_authorized.html", status=403)
handler400 = SystemView.as_view(template_name="pages_misc_error.html", status=400)
handler500 = SystemView.as_view(template_name="pages_misc_error.html", status=500)


# Dashboard urls
# path("", include("apps.theme.dashboards.urls")),
# layouts urls
# path("", include("apps.theme.layouts.urls")),
# FrontPages urls
# path("", include("apps.theme.front_pages.urls")),
# FrontPages urls
# path("", include("apps.theme.mail.urls")),
# Chat urls
# path("", include("apps.theme.chat.urls")),
# Calendar urls
# path("", include("apps.theme.my_calendar.urls")),
# Kanban urls
# path("", include("apps.theme.kanban.urls")),
# eCommerce urls
# path("", include("apps.theme.ecommerce.urls")),
# Academy urls
# path("", include("apps.theme.academy.urls")),
# Logistics urls
# path("", include("apps.theme.logistics.urls")),
# Invoice urls
# path("", include("apps.theme.invoice.urls")),
# User urls
# path("", include("apps.theme.users.urls")),
# Access urls
# path("", include("apps.theme.access.urls")),
# Pages urls
# path("", include("apps.theme.pages.urls")),
# Auth urls
# path("", include("apps.theme.authentication.urls")),
# Wizard urls
# path("", include("apps.theme.wizard_examples.urls")),
# ModalExample urls
# path("", include("apps.theme.modal_examples.urls")),
# Card urls
# path("", include("apps.theme.cards.urls")),
# UI urls
# path("", include("apps.theme.ui.urls")),
# Extended UI urls
# path("", include("apps.theme.extended_ui.urls")),
# Icons urls
# path("", include("apps.theme.icons.urls")),
# Forms urls
# path("", include("apps.theme.forms.urls")),
# FormLayouts urls
# path("", include("apps.theme.form_layouts.urls")),
# FormWizard urls
# path("", include("apps.theme.form_wizard.urls")),
# FormValidation urls
# path("", include("apps.theme.form_validation.urls")),
# Tables urls
# path("", include("apps.theme.tables.urls")),
# Chart urls
# path("", include("apps.theme.charts.urls")),
# Map urls
# path("", include("apps.theme.maps.urls")),
# Auth urls
# path("", include("auth.urls")),
# Transaction urls
# path("", include("apps.theme.llm_transaction.urls")),
